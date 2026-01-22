"""Export tools for the Ableton MCP server.

Provides audio export functionality by recording Ableton's audio output using FFmpeg.
Since Ableton's Live Object Model doesn't expose export functionality, this uses
system audio capture as a workaround.
"""

import os
import platform
import shutil
import subprocess
import time
from typing import Annotated, Optional

from pydantic import Field

from ableton_mcp.connection import get_client
from abletonosc_client import Song


def _is_wsl() -> bool:
    """Check if running in WSL."""
    try:
        with open("/proc/version", "r") as f:
            return "microsoft" in f.read().lower()
    except Exception:
        return False


def _find_ffmpeg() -> str:
    """Find FFmpeg executable path.

    Returns:
        Path to ffmpeg executable

    Raises:
        FileNotFoundError: If FFmpeg is not found
    """
    # Check Linux PATH first
    ffmpeg = shutil.which("ffmpeg")
    if ffmpeg:
        return ffmpeg

    # On WSL, try Windows FFmpeg
    if _is_wsl():
        # Try common Windows FFmpeg locations via cmd.exe
        try:
            result = subprocess.run(
                ["cmd.exe", "/c", "where", "ffmpeg"],
                capture_output=True, text=True, timeout=5
            )
            if result.returncode == 0 and result.stdout.strip():
                return result.stdout.strip().split("\n")[0]
        except Exception:
            pass

    raise FileNotFoundError(
        "FFmpeg not found. Install it with:\n"
        "  Linux: sudo apt install ffmpeg\n"
        "  Windows: winget install ffmpeg"
    )


def _get_default_audio_device() -> tuple[str, str, dict]:
    """Get default audio capture device and format for the current platform.

    Returns:
        Tuple of (device_name, input_format, env_vars)

    Raises:
        RuntimeError: If no suitable device is found
    """
    system = platform.system()
    env_vars = {}

    if system == "Linux" or _is_wsl():
        # For WSL2, we need to capture Windows audio
        # This is tricky - WSL2 doesn't have direct audio access
        # Options: 1) Use PulseAudio with WSLg, 2) Call Windows FFmpeg

        # Check for PulseAudio (WSLg)
        if os.path.exists("/mnt/wslg/PulseServer"):
            # WSLg available - use PulseAudio with correct socket
            env_vars["PULSE_SERVER"] = "/mnt/wslg/PulseServer"
            return ("default", "pulse", env_vars)

        # Fallback: try ALSA
        return ("default", "alsa", env_vars)

    elif system == "Darwin":
        # macOS - need BlackHole or similar virtual audio device
        return ("BlackHole 2ch", "avfoundation", env_vars)

    elif system == "Windows":
        # Windows - Stereo Mix or virtual audio cable
        return ("Stereo Mix (Realtek(R) Audio)", "dshow", env_vars)

    raise RuntimeError(f"Unsupported platform: {system}")


def _list_audio_devices_linux() -> list[dict]:
    """List audio devices on Linux."""
    devices = []

    # Check for WSLg PulseAudio
    if os.path.exists("/mnt/wslg/PulseServer"):
        devices.append({
            "name": "default",
            "format": "pulse",
            "type": "wslg",
            "note": "WSLg PulseAudio - captures Windows audio"
        })

    # Try PulseAudio with pactl (if available)
    pulse_env = os.environ.copy()
    if os.path.exists("/mnt/wslg/PulseServer"):
        pulse_env["PULSE_SERVER"] = "/mnt/wslg/PulseServer"

    try:
        result = subprocess.run(
            ["pactl", "list", "sources", "short"],
            capture_output=True, text=True, timeout=5,
            env=pulse_env
        )
        if result.returncode == 0:
            for line in result.stdout.strip().split("\n"):
                if line:
                    parts = line.split("\t")
                    if len(parts) >= 2:
                        devices.append({
                            "name": parts[1],
                            "format": "pulse",
                            "type": "monitor" if "monitor" in parts[1].lower() else "input"
                        })
    except FileNotFoundError:
        # pactl not installed - that's OK if we have WSLg
        pass
    except Exception:
        pass

    # Try ALSA
    try:
        result = subprocess.run(
            ["arecord", "-l"],
            capture_output=True, text=True, timeout=5
        )
        if result.returncode == 0:
            for line in result.stdout.split("\n"):
                if line.startswith("card"):
                    # Parse: "card 0: PCH [HDA Intel PCH], device 0: ALC..."
                    devices.append({
                        "name": line,
                        "format": "alsa",
                        "type": "hardware"
                    })
    except Exception:
        pass

    return devices


def _list_audio_devices_windows() -> list[dict]:
    """List audio devices on Windows (or via WSL cmd.exe)."""
    devices = []

    try:
        if _is_wsl():
            # Call Windows FFmpeg from WSL
            result = subprocess.run(
                ["cmd.exe", "/c", "ffmpeg", "-list_devices", "true", "-f", "dshow", "-i", "dummy"],
                capture_output=True, text=True, timeout=10
            )
        else:
            result = subprocess.run(
                ["ffmpeg", "-list_devices", "true", "-f", "dshow", "-i", "dummy"],
                capture_output=True, text=True, timeout=10
            )

        # FFmpeg outputs device list to stderr
        output = result.stderr
        in_audio_section = False

        for line in output.split("\n"):
            if "DirectShow audio devices" in line:
                in_audio_section = True
                continue
            if "DirectShow video devices" in line:
                in_audio_section = False
                continue
            if in_audio_section and '"' in line:
                # Parse: [dshow @ ...] "Device Name"
                start = line.find('"') + 1
                end = line.rfind('"')
                if start > 0 and end > start:
                    device_name = line[start:end]
                    devices.append({
                        "name": device_name,
                        "format": "dshow",
                        "type": "audio"
                    })
    except Exception as e:
        devices.append({"error": str(e)})

    return devices


def register_export_tools(mcp):
    """Register all export tools with the MCP server."""

    @mcp.tool()
    def export_list_audio_devices() -> list[dict]:
        """List available audio capture devices.

        Returns devices that can be used with song_export_audio().
        On Linux, shows PulseAudio and ALSA devices.
        On Windows/WSL, shows DirectShow devices (Stereo Mix, etc).

        Returns:
            List of device dictionaries with name, format, and type
        """
        system = platform.system()
        is_wsl = _is_wsl()

        all_devices = []

        # Linux/WSL - get Linux devices
        if system == "Linux":
            all_devices.extend(_list_audio_devices_linux())

        # WSL or Windows - get Windows devices
        if is_wsl or system == "Windows":
            all_devices.extend(_list_audio_devices_windows())

        if not all_devices:
            return [{"error": "No audio devices found", "platform": system, "is_wsl": is_wsl}]

        return all_devices

    @mcp.tool()
    def song_get_duration_seconds() -> float:
        """Get the song duration in seconds.

        Calculates duration from song length (beats) and tempo (BPM).

        Returns:
            Song duration in seconds
        """
        song = Song(get_client())
        length_beats = song.get_song_length()
        tempo = song.get_tempo()

        # beats / (beats per minute) * 60 = seconds
        duration_seconds = (length_beats / tempo) * 60
        return duration_seconds

    @mcp.tool()
    def song_export_audio(
        output_file: Annotated[str, Field(description="Output file path (e.g., '/path/to/song.mp3' or 'song.wav')")],
        duration_seconds: Annotated[Optional[float], Field(description="Recording duration in seconds. If not specified, uses song length.")] = None,
        audio_device: Annotated[Optional[str], Field(description="Audio capture device name. Use export_list_audio_devices() to see options.")] = None,
        start_playback: Annotated[bool, Field(description="Whether to start Ableton playback automatically")] = True,
        sample_rate: Annotated[int, Field(description="Audio sample rate (default: 44100)")] = 44100,
        audio_format: Annotated[Optional[str], Field(description="Input format (pulse, alsa, dshow). Auto-detected if not specified.")] = None
    ) -> str:
        """Export the current song to an audio file by recording Ableton's output.

        This tool records system audio while Ableton plays, then saves to MP3/WAV.

        Prerequisites:
        - FFmpeg must be installed
        - Audio loopback device must be available:
          - Linux: PulseAudio monitor or ALSA loopback
          - Windows: Stereo Mix enabled, or VB-Cable installed
          - WSL2: Requires WSLg for audio, or call Windows FFmpeg

        Args:
            output_file: Where to save the audio (supports .mp3, .wav, .flac, .ogg)
            duration_seconds: How long to record. Auto-calculated from song if omitted.
            audio_device: Capture device (auto-detected if not specified)
            start_playback: Start Ableton playback automatically (default: True)
            sample_rate: Sample rate in Hz (default: 44100)
            audio_format: FFmpeg input format (auto-detected if not specified)

        Returns:
            Success message with output file path, or error details
        """
        # Find FFmpeg
        try:
            ffmpeg_path = _find_ffmpeg()
        except FileNotFoundError as e:
            return str(e)

        # Get song for playback control
        song = Song(get_client())

        # Calculate duration if not specified
        if duration_seconds is None:
            length_beats = song.get_song_length()
            tempo = song.get_tempo()
            duration_seconds = (length_beats / tempo) * 60
            # Add a small buffer for safety
            duration_seconds += 2.0

        # Get audio device settings
        env_vars = {}
        if audio_device is None or audio_format is None:
            default_device, default_format, env_vars = _get_default_audio_device()
            audio_device = audio_device or default_device
            audio_format = audio_format or default_format

        # Determine output format from file extension
        output_ext = os.path.splitext(output_file)[1].lower()
        if output_ext not in [".mp3", ".wav", ".flac", ".ogg", ".m4a"]:
            return f"Unsupported output format: {output_ext}. Use .mp3, .wav, .flac, .ogg, or .m4a"

        # Build FFmpeg command
        cmd = [
            ffmpeg_path,
            "-y",  # Overwrite output
            "-f", audio_format,
        ]

        # Add device-specific input options
        if audio_format == "pulse":
            cmd.extend(["-i", audio_device])
        elif audio_format == "alsa":
            cmd.extend(["-i", f"hw:{audio_device}"])
        elif audio_format == "dshow":
            cmd.extend(["-i", f"audio={audio_device}"])
        elif audio_format == "avfoundation":
            cmd.extend(["-i", f":{audio_device}"])
        else:
            cmd.extend(["-i", audio_device])

        # Add duration and output settings
        cmd.extend([
            "-t", str(duration_seconds),
            "-ar", str(sample_rate),
            "-ac", "2",  # Stereo
        ])

        # Add codec settings based on output format
        if output_ext == ".mp3":
            cmd.extend(["-codec:a", "libmp3lame", "-q:a", "2"])
        elif output_ext == ".flac":
            cmd.extend(["-codec:a", "flac"])
        elif output_ext == ".ogg":
            cmd.extend(["-codec:a", "libvorbis", "-q:a", "6"])
        elif output_ext == ".m4a":
            cmd.extend(["-codec:a", "aac", "-b:a", "256k"])
        # WAV uses default PCM codec

        cmd.append(output_file)

        # Start FFmpeg recording
        try:
            # Merge environment variables with current environment
            run_env = os.environ.copy()
            run_env.update(env_vars)

            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                env=run_env
            )
        except Exception as e:
            return f"Failed to start FFmpeg: {e}\nCommand: {' '.join(cmd)}"

        # Give FFmpeg a moment to initialize
        time.sleep(0.5)

        # Start Ableton playback if requested
        if start_playback:
            # Reset to beginning
            song.set_current_song_time(0)
            time.sleep(0.1)
            song.play()

        # Wait for FFmpeg to complete
        try:
            stdout, stderr = process.communicate(timeout=duration_seconds + 30)
        except subprocess.TimeoutExpired:
            process.kill()
            return f"FFmpeg timed out after {duration_seconds + 30} seconds"

        # Stop Ableton playback
        if start_playback:
            song.stop()

        # Check result
        if process.returncode != 0:
            error_msg = stderr.decode() if stderr else "Unknown error"
            return f"FFmpeg failed (exit code {process.returncode}):\n{error_msg}\nCommand: {' '.join(cmd)}"

        # Verify output file exists
        if os.path.exists(output_file):
            file_size = os.path.getsize(output_file)
            return f"Successfully exported to {output_file} ({file_size / 1024:.1f} KB, {duration_seconds:.1f}s)"
        else:
            return f"FFmpeg completed but output file not found: {output_file}"

    @mcp.tool()
    def export_test_audio_capture(
        output_file: Annotated[str, Field(description="Output file path for test recording")],
        duration_seconds: Annotated[float, Field(description="Test recording duration")] = 5.0,
        audio_device: Annotated[Optional[str], Field(description="Audio device to test")] = None
    ) -> str:
        """Test audio capture without Ableton playback.

        Records system audio for a short duration to verify FFmpeg
        and audio device configuration are working correctly.

        Args:
            output_file: Where to save the test recording
            duration_seconds: How long to record (default: 5 seconds)
            audio_device: Device to test (auto-detected if not specified)

        Returns:
            Success message or error details
        """
        return song_export_audio(
            output_file=output_file,
            duration_seconds=duration_seconds,
            audio_device=audio_device,
            start_playback=False
        )
