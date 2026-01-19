"""Clip tools for the Ableton MCP server.

Covers clip-level operations like notes, playback, loop settings, and audio properties.
"""

from typing import Annotated

from pydantic import Field

from ableton_mcp.connection import get_client
from abletonosc_client import Clip
from abletonosc_client.clip import Note


def register_clip_tools(mcp):
    """Register all clip tools with the MCP server."""

    # =============================================================================
    # Name
    # =============================================================================

    @mcp.tool()
    def clip_get_name(
        track_index: Annotated[int, Field(description="Track index (0-based)", ge=0)],
        clip_index: Annotated[int, Field(description="Clip/scene index (0-based)", ge=0)]
    ) -> str:
        """Get the name of a clip.

        Args:
            track_index: Track index (0-based)
            clip_index: Clip/scene index (0-based)

        Returns:
            Clip name
        """
        clip = Clip(get_client())
        return clip.get_name(track_index, clip_index)

    @mcp.tool()
    def clip_set_name(
        track_index: Annotated[int, Field(description="Track index (0-based)", ge=0)],
        clip_index: Annotated[int, Field(description="Clip/scene index (0-based)", ge=0)],
        name: Annotated[str, Field(description="New clip name")]
    ) -> str:
        """Set the name of a clip.

        Args:
            track_index: Track index (0-based)
            clip_index: Clip/scene index (0-based)
            name: New clip name

        Returns:
            Confirmation message
        """
        clip = Clip(get_client())
        clip.set_name(track_index, clip_index, name)
        return f"Clip at track {track_index}, scene {clip_index} renamed to '{name}'"

    # =============================================================================
    # Playback
    # =============================================================================

    @mcp.tool()
    def clip_fire(
        track_index: Annotated[int, Field(description="Track index (0-based)", ge=0)],
        clip_index: Annotated[int, Field(description="Clip/scene index (0-based)", ge=0)]
    ) -> str:
        """Launch (fire) a clip.

        Args:
            track_index: Track index (0-based)
            clip_index: Clip/scene index (0-based)

        Returns:
            Confirmation message
        """
        clip = Clip(get_client())
        clip.fire(track_index, clip_index)
        return f"Clip fired at track {track_index}, scene {clip_index}"

    @mcp.tool()
    def clip_stop(
        track_index: Annotated[int, Field(description="Track index (0-based)", ge=0)],
        clip_index: Annotated[int, Field(description="Clip/scene index (0-based)", ge=0)]
    ) -> str:
        """Stop a clip.

        Args:
            track_index: Track index (0-based)
            clip_index: Clip/scene index (0-based)

        Returns:
            Confirmation message
        """
        clip = Clip(get_client())
        clip.stop(track_index, clip_index)
        return f"Clip stopped at track {track_index}, scene {clip_index}"

    # =============================================================================
    # Clip Properties
    # =============================================================================

    @mcp.tool()
    def clip_get_length(
        track_index: Annotated[int, Field(description="Track index (0-based)", ge=0)],
        clip_index: Annotated[int, Field(description="Clip/scene index (0-based)", ge=0)]
    ) -> float:
        """Get the clip length in beats.

        Args:
            track_index: Track index (0-based)
            clip_index: Clip/scene index (0-based)

        Returns:
            Clip length in beats
        """
        clip = Clip(get_client())
        return clip.get_length(track_index, clip_index)

    @mcp.tool()
    def clip_get_is_midi_clip(
        track_index: Annotated[int, Field(description="Track index (0-based)", ge=0)],
        clip_index: Annotated[int, Field(description="Clip/scene index (0-based)", ge=0)]
    ) -> bool:
        """Check if clip is a MIDI clip.

        Args:
            track_index: Track index (0-based)
            clip_index: Clip/scene index (0-based)

        Returns:
            True if MIDI clip, False if audio clip
        """
        clip = Clip(get_client())
        return clip.get_is_midi_clip(track_index, clip_index)

    @mcp.tool()
    def clip_get_is_audio_clip(
        track_index: Annotated[int, Field(description="Track index (0-based)", ge=0)],
        clip_index: Annotated[int, Field(description="Clip/scene index (0-based)", ge=0)]
    ) -> bool:
        """Check if clip is an audio clip.

        Args:
            track_index: Track index (0-based)
            clip_index: Clip/scene index (0-based)

        Returns:
            True if audio clip, False if MIDI clip
        """
        clip = Clip(get_client())
        return clip.get_is_audio_clip(track_index, clip_index)

    @mcp.tool()
    def clip_get_is_playing(
        track_index: Annotated[int, Field(description="Track index (0-based)", ge=0)],
        clip_index: Annotated[int, Field(description="Clip/scene index (0-based)", ge=0)]
    ) -> bool:
        """Check if clip is currently playing.

        Args:
            track_index: Track index (0-based)
            clip_index: Clip/scene index (0-based)

        Returns:
            True if playing
        """
        clip = Clip(get_client())
        return clip.get_is_playing(track_index, clip_index)

    @mcp.tool()
    def clip_get_playing_position(
        track_index: Annotated[int, Field(description="Track index (0-based)", ge=0)],
        clip_index: Annotated[int, Field(description="Clip/scene index (0-based)", ge=0)]
    ) -> float:
        """Get the current playhead position in the clip.

        Args:
            track_index: Track index (0-based)
            clip_index: Clip/scene index (0-based)

        Returns:
            Playhead position in beats
        """
        clip = Clip(get_client())
        return clip.get_playing_position(track_index, clip_index)

    # =============================================================================
    # Color
    # =============================================================================

    @mcp.tool()
    def clip_get_color(
        track_index: Annotated[int, Field(description="Track index (0-based)", ge=0)],
        clip_index: Annotated[int, Field(description="Clip/scene index (0-based)", ge=0)]
    ) -> int:
        """Get the clip color.

        Args:
            track_index: Track index (0-based)
            clip_index: Clip/scene index (0-based)

        Returns:
            Color as integer
        """
        clip = Clip(get_client())
        return clip.get_color(track_index, clip_index)

    @mcp.tool()
    def clip_set_color(
        track_index: Annotated[int, Field(description="Track index (0-based)", ge=0)],
        clip_index: Annotated[int, Field(description="Clip/scene index (0-based)", ge=0)],
        color: Annotated[int, Field(description="Color as integer")]
    ) -> str:
        """Set the clip color.

        Args:
            track_index: Track index (0-based)
            clip_index: Clip/scene index (0-based)
            color: Color as integer

        Returns:
            Confirmation message
        """
        clip = Clip(get_client())
        clip.set_color(track_index, clip_index, color)
        return f"Clip at track {track_index}, scene {clip_index} color set to {color}"

    @mcp.tool()
    def clip_get_color_index(
        track_index: Annotated[int, Field(description="Track index (0-based)", ge=0)],
        clip_index: Annotated[int, Field(description="Clip/scene index (0-based)", ge=0)]
    ) -> int:
        """Get the color index of a clip.

        Args:
            track_index: Track index (0-based)
            clip_index: Clip/scene index (0-based)

        Returns:
            Color index (0-69)
        """
        clip = Clip(get_client())
        return clip.get_color_index(track_index, clip_index)

    @mcp.tool()
    def clip_set_color_index(
        track_index: Annotated[int, Field(description="Track index (0-based)", ge=0)],
        clip_index: Annotated[int, Field(description="Clip/scene index (0-based)", ge=0)],
        color_index: Annotated[int, Field(description="Color index (0-69)", ge=0, le=69)]
    ) -> str:
        """Set the color index of a clip.

        Args:
            track_index: Track index (0-based)
            clip_index: Clip/scene index (0-based)
            color_index: Color index (0-69)

        Returns:
            Confirmation message
        """
        clip = Clip(get_client())
        clip.set_color_index(track_index, clip_index, color_index)
        return f"Clip at track {track_index}, scene {clip_index} color index set to {color_index}"

    # =============================================================================
    # Notes (MIDI clips)
    # =============================================================================

    @mcp.tool()
    def clip_get_notes(
        track_index: Annotated[int, Field(description="Track index (0-based)", ge=0)],
        clip_index: Annotated[int, Field(description="Clip/scene index (0-based)", ge=0)]
    ) -> list[dict]:
        """Get all notes from a MIDI clip.

        Args:
            track_index: Track index (0-based)
            clip_index: Clip/scene index (0-based)

        Returns:
            List of notes, each with pitch, start_time, duration, velocity, mute
        """
        clip = Clip(get_client())
        notes = clip.get_notes(track_index, clip_index)
        return [
            {
                "pitch": n.pitch,
                "start_time": n.start_time,
                "duration": n.duration,
                "velocity": n.velocity,
                "mute": n.mute
            }
            for n in notes
        ]

    @mcp.tool()
    def clip_add_notes(
        track_index: Annotated[int, Field(description="Track index (0-based)", ge=0)],
        clip_index: Annotated[int, Field(description="Clip/scene index (0-based)", ge=0)],
        notes: Annotated[list[dict], Field(
            description="List of notes, each with pitch (0-127), start_time (beats), duration (beats), velocity (0-127)"
        )]
    ) -> str:
        """Add MIDI notes to a clip.

        Args:
            track_index: Track index (0-based)
            clip_index: Clip/scene index (0-based)
            notes: List of notes, each dict with: pitch (0-127), start_time (beats), duration (beats), velocity (0-127)

        Returns:
            Confirmation message

        Example notes:
            [
                {"pitch": 60, "start_time": 0.0, "duration": 0.5, "velocity": 100},
                {"pitch": 64, "start_time": 0.5, "duration": 0.5, "velocity": 100}
            ]
        """
        clip = Clip(get_client())
        note_objects = [
            Note(
                pitch=n["pitch"],
                start_time=n["start_time"],
                duration=n["duration"],
                velocity=n["velocity"],
                mute=n.get("mute", False)
            )
            for n in notes
        ]
        clip.add_notes(track_index, clip_index, note_objects)
        return f"Added {len(notes)} notes to clip at track {track_index}, scene {clip_index}"

    @mcp.tool()
    def clip_remove_notes(
        track_index: Annotated[int, Field(description="Track index (0-based)", ge=0)],
        clip_index: Annotated[int, Field(description="Clip/scene index (0-based)", ge=0)],
        start_time: Annotated[float, Field(description="Start of time range in beats", ge=0)] = 0.0,
        end_time: Annotated[float, Field(description="End of time range in beats")] = 128.0,
        pitch_start: Annotated[int, Field(description="Lowest pitch to remove", ge=0, le=127)] = 0,
        pitch_end: Annotated[int, Field(description="Highest pitch to remove", ge=0, le=127)] = 127
    ) -> str:
        """Remove notes from a MIDI clip within a range.

        Args:
            track_index: Track index (0-based)
            clip_index: Clip/scene index (0-based)
            start_time: Start of time range in beats (default: 0)
            end_time: End of time range in beats (default: 128)
            pitch_start: Lowest pitch to remove (default: 0)
            pitch_end: Highest pitch to remove (default: 127)

        Returns:
            Confirmation message
        """
        clip = Clip(get_client())
        clip.remove_notes(track_index, clip_index, start_time, end_time, pitch_start, pitch_end)
        return f"Notes removed from clip at track {track_index}, scene {clip_index}"

    # =============================================================================
    # Loop Settings
    # =============================================================================

    @mcp.tool()
    def clip_get_loop_start(
        track_index: Annotated[int, Field(description="Track index (0-based)", ge=0)],
        clip_index: Annotated[int, Field(description="Clip/scene index (0-based)", ge=0)]
    ) -> float:
        """Get the loop start position in beats.

        Args:
            track_index: Track index (0-based)
            clip_index: Clip/scene index (0-based)

        Returns:
            Loop start position in beats
        """
        clip = Clip(get_client())
        return clip.get_loop_start(track_index, clip_index)

    @mcp.tool()
    def clip_set_loop_start(
        track_index: Annotated[int, Field(description="Track index (0-based)", ge=0)],
        clip_index: Annotated[int, Field(description="Clip/scene index (0-based)", ge=0)],
        start: Annotated[float, Field(description="Loop start in beats", ge=0)]
    ) -> str:
        """Set the loop start position.

        Args:
            track_index: Track index (0-based)
            clip_index: Clip/scene index (0-based)
            start: Loop start in beats

        Returns:
            Confirmation message
        """
        clip = Clip(get_client())
        clip.set_loop_start(track_index, clip_index, start)
        return f"Clip loop start set to {start} beats"

    @mcp.tool()
    def clip_get_loop_end(
        track_index: Annotated[int, Field(description="Track index (0-based)", ge=0)],
        clip_index: Annotated[int, Field(description="Clip/scene index (0-based)", ge=0)]
    ) -> float:
        """Get the loop end position in beats.

        Args:
            track_index: Track index (0-based)
            clip_index: Clip/scene index (0-based)

        Returns:
            Loop end position in beats
        """
        clip = Clip(get_client())
        return clip.get_loop_end(track_index, clip_index)

    @mcp.tool()
    def clip_set_loop_end(
        track_index: Annotated[int, Field(description="Track index (0-based)", ge=0)],
        clip_index: Annotated[int, Field(description="Clip/scene index (0-based)", ge=0)],
        end: Annotated[float, Field(description="Loop end in beats")]
    ) -> str:
        """Set the loop end position.

        Args:
            track_index: Track index (0-based)
            clip_index: Clip/scene index (0-based)
            end: Loop end in beats

        Returns:
            Confirmation message
        """
        clip = Clip(get_client())
        clip.set_loop_end(track_index, clip_index, end)
        return f"Clip loop end set to {end} beats"

    @mcp.tool()
    def clip_get_looping(
        track_index: Annotated[int, Field(description="Track index (0-based)", ge=0)],
        clip_index: Annotated[int, Field(description="Clip/scene index (0-based)", ge=0)]
    ) -> bool:
        """Check if clip looping is enabled.

        Args:
            track_index: Track index (0-based)
            clip_index: Clip/scene index (0-based)

        Returns:
            True if looping is enabled
        """
        clip = Clip(get_client())
        return clip.get_looping(track_index, clip_index)

    @mcp.tool()
    def clip_set_looping(
        track_index: Annotated[int, Field(description="Track index (0-based)", ge=0)],
        clip_index: Annotated[int, Field(description="Clip/scene index (0-based)", ge=0)],
        enabled: Annotated[bool, Field(description="True to enable looping")]
    ) -> str:
        """Enable or disable clip looping.

        Args:
            track_index: Track index (0-based)
            clip_index: Clip/scene index (0-based)
            enabled: True to enable looping

        Returns:
            Confirmation message
        """
        clip = Clip(get_client())
        clip.set_looping(track_index, clip_index, enabled)
        state = "enabled" if enabled else "disabled"
        return f"Clip looping {state}"

    @mcp.tool()
    def clip_duplicate_loop(
        track_index: Annotated[int, Field(description="Track index (0-based)", ge=0)],
        clip_index: Annotated[int, Field(description="Clip/scene index (0-based)", ge=0)]
    ) -> str:
        """Duplicate the loop content of a clip.

        Args:
            track_index: Track index (0-based)
            clip_index: Clip/scene index (0-based)

        Returns:
            Confirmation message
        """
        clip = Clip(get_client())
        clip.duplicate_loop(track_index, clip_index)
        return f"Clip loop duplicated at track {track_index}, scene {clip_index}"

    # =============================================================================
    # Start/End Time
    # =============================================================================

    @mcp.tool()
    def clip_get_start_time(
        track_index: Annotated[int, Field(description="Track index (0-based)", ge=0)],
        clip_index: Annotated[int, Field(description="Clip/scene index (0-based)", ge=0)]
    ) -> float:
        """Get the clip start time in beats.

        Args:
            track_index: Track index (0-based)
            clip_index: Clip/scene index (0-based)

        Returns:
            Start time in beats
        """
        clip = Clip(get_client())
        return clip.get_start_time(track_index, clip_index)

    @mcp.tool()
    def clip_set_start_time(
        track_index: Annotated[int, Field(description="Track index (0-based)", ge=0)],
        clip_index: Annotated[int, Field(description="Clip/scene index (0-based)", ge=0)],
        time: Annotated[float, Field(description="Start time in beats")]
    ) -> str:
        """Set the clip start time.

        Args:
            track_index: Track index (0-based)
            clip_index: Clip/scene index (0-based)
            time: Start time in beats

        Returns:
            Confirmation message
        """
        clip = Clip(get_client())
        clip.set_start_time(track_index, clip_index, time)
        return f"Clip start time set to {time} beats"

    @mcp.tool()
    def clip_get_end_time(
        track_index: Annotated[int, Field(description="Track index (0-based)", ge=0)],
        clip_index: Annotated[int, Field(description="Clip/scene index (0-based)", ge=0)]
    ) -> float:
        """Get the clip end time in beats.

        Args:
            track_index: Track index (0-based)
            clip_index: Clip/scene index (0-based)

        Returns:
            End time in beats
        """
        clip = Clip(get_client())
        return clip.get_end_time(track_index, clip_index)

    @mcp.tool()
    def clip_set_end_time(
        track_index: Annotated[int, Field(description="Track index (0-based)", ge=0)],
        clip_index: Annotated[int, Field(description="Clip/scene index (0-based)", ge=0)],
        time: Annotated[float, Field(description="End time in beats")]
    ) -> str:
        """Set the clip end time.

        Args:
            track_index: Track index (0-based)
            clip_index: Clip/scene index (0-based)
            time: End time in beats

        Returns:
            Confirmation message
        """
        clip = Clip(get_client())
        clip.set_end_time(track_index, clip_index, time)
        return f"Clip end time set to {time} beats"

    # =============================================================================
    # Markers
    # =============================================================================

    @mcp.tool()
    def clip_get_start_marker(
        track_index: Annotated[int, Field(description="Track index (0-based)", ge=0)],
        clip_index: Annotated[int, Field(description="Clip/scene index (0-based)", ge=0)]
    ) -> float:
        """Get the start marker position.

        Args:
            track_index: Track index (0-based)
            clip_index: Clip/scene index (0-based)

        Returns:
            Start marker position in beats
        """
        clip = Clip(get_client())
        return clip.get_start_marker(track_index, clip_index)

    @mcp.tool()
    def clip_set_start_marker(
        track_index: Annotated[int, Field(description="Track index (0-based)", ge=0)],
        clip_index: Annotated[int, Field(description="Clip/scene index (0-based)", ge=0)],
        position: Annotated[float, Field(description="Start marker position in beats")]
    ) -> str:
        """Set the start marker position.

        Args:
            track_index: Track index (0-based)
            clip_index: Clip/scene index (0-based)
            position: Start marker position in beats

        Returns:
            Confirmation message
        """
        clip = Clip(get_client())
        clip.set_start_marker(track_index, clip_index, position)
        return f"Clip start marker set to {position} beats"

    @mcp.tool()
    def clip_get_end_marker(
        track_index: Annotated[int, Field(description="Track index (0-based)", ge=0)],
        clip_index: Annotated[int, Field(description="Clip/scene index (0-based)", ge=0)]
    ) -> float:
        """Get the end marker position.

        Args:
            track_index: Track index (0-based)
            clip_index: Clip/scene index (0-based)

        Returns:
            End marker position in beats
        """
        clip = Clip(get_client())
        return clip.get_end_marker(track_index, clip_index)

    @mcp.tool()
    def clip_set_end_marker(
        track_index: Annotated[int, Field(description="Track index (0-based)", ge=0)],
        clip_index: Annotated[int, Field(description="Clip/scene index (0-based)", ge=0)],
        position: Annotated[float, Field(description="End marker position in beats")]
    ) -> str:
        """Set the end marker position.

        Args:
            track_index: Track index (0-based)
            clip_index: Clip/scene index (0-based)
            position: End marker position in beats

        Returns:
            Confirmation message
        """
        clip = Clip(get_client())
        clip.set_end_marker(track_index, clip_index, position)
        return f"Clip end marker set to {position} beats"

    # =============================================================================
    # Mute
    # =============================================================================

    @mcp.tool()
    def clip_get_muted(
        track_index: Annotated[int, Field(description="Track index (0-based)", ge=0)],
        clip_index: Annotated[int, Field(description="Clip/scene index (0-based)", ge=0)]
    ) -> bool:
        """Check if clip is muted.

        Args:
            track_index: Track index (0-based)
            clip_index: Clip/scene index (0-based)

        Returns:
            True if clip is muted
        """
        clip = Clip(get_client())
        return clip.get_muted(track_index, clip_index)

    @mcp.tool()
    def clip_set_muted(
        track_index: Annotated[int, Field(description="Track index (0-based)", ge=0)],
        clip_index: Annotated[int, Field(description="Clip/scene index (0-based)", ge=0)],
        muted: Annotated[bool, Field(description="True to mute the clip")]
    ) -> str:
        """Mute or unmute a clip.

        Args:
            track_index: Track index (0-based)
            clip_index: Clip/scene index (0-based)
            muted: True to mute the clip

        Returns:
            Confirmation message
        """
        clip = Clip(get_client())
        clip.set_muted(track_index, clip_index, muted)
        state = "muted" if muted else "unmuted"
        return f"Clip at track {track_index}, scene {clip_index} {state}"

    # =============================================================================
    # Launch Mode
    # =============================================================================

    @mcp.tool()
    def clip_get_launch_mode(
        track_index: Annotated[int, Field(description="Track index (0-based)", ge=0)],
        clip_index: Annotated[int, Field(description="Clip/scene index (0-based)", ge=0)]
    ) -> int:
        """Get the launch mode of a clip.

        Args:
            track_index: Track index (0-based)
            clip_index: Clip/scene index (0-based)

        Returns:
            Launch mode (0=Trigger, 1=Gate, 2=Toggle, 3=Repeat)
        """
        clip = Clip(get_client())
        return clip.get_launch_mode(track_index, clip_index)

    @mcp.tool()
    def clip_set_launch_mode(
        track_index: Annotated[int, Field(description="Track index (0-based)", ge=0)],
        clip_index: Annotated[int, Field(description="Clip/scene index (0-based)", ge=0)],
        mode: Annotated[int, Field(description="Launch mode (0=Trigger, 1=Gate, 2=Toggle, 3=Repeat)", ge=0, le=3)]
    ) -> str:
        """Set the launch mode of a clip.

        Args:
            track_index: Track index (0-based)
            clip_index: Clip/scene index (0-based)
            mode: Launch mode (0=Trigger, 1=Gate, 2=Toggle, 3=Repeat)

        Returns:
            Confirmation message
        """
        clip = Clip(get_client())
        clip.set_launch_mode(track_index, clip_index, mode)
        mode_names = ["Trigger", "Gate", "Toggle", "Repeat"]
        return f"Clip launch mode set to {mode_names[mode]}"

    @mcp.tool()
    def clip_get_launch_quantization(
        track_index: Annotated[int, Field(description="Track index (0-based)", ge=0)],
        clip_index: Annotated[int, Field(description="Clip/scene index (0-based)", ge=0)]
    ) -> int:
        """Get the launch quantization of a clip.

        Args:
            track_index: Track index (0-based)
            clip_index: Clip/scene index (0-based)

        Returns:
            Launch quantization value
        """
        clip = Clip(get_client())
        return clip.get_launch_quantization(track_index, clip_index)

    @mcp.tool()
    def clip_set_launch_quantization(
        track_index: Annotated[int, Field(description="Track index (0-based)", ge=0)],
        clip_index: Annotated[int, Field(description="Clip/scene index (0-based)", ge=0)],
        quantization: Annotated[int, Field(description="Launch quantization value", ge=0)]
    ) -> str:
        """Set the launch quantization of a clip.

        Args:
            track_index: Track index (0-based)
            clip_index: Clip/scene index (0-based)
            quantization: Launch quantization value

        Returns:
            Confirmation message
        """
        clip = Clip(get_client())
        clip.set_launch_quantization(track_index, clip_index, quantization)
        return f"Clip launch quantization set to {quantization}"

    # =============================================================================
    # Position
    # =============================================================================

    @mcp.tool()
    def clip_get_position(
        track_index: Annotated[int, Field(description="Track index (0-based)", ge=0)],
        clip_index: Annotated[int, Field(description="Clip/scene index (0-based)", ge=0)]
    ) -> float:
        """Get the loop position of a clip.

        Args:
            track_index: Track index (0-based)
            clip_index: Clip/scene index (0-based)

        Returns:
            Position in beats
        """
        clip = Clip(get_client())
        return clip.get_position(track_index, clip_index)

    @mcp.tool()
    def clip_set_position(
        track_index: Annotated[int, Field(description="Track index (0-based)", ge=0)],
        clip_index: Annotated[int, Field(description="Clip/scene index (0-based)", ge=0)],
        position: Annotated[float, Field(description="Position in beats")]
    ) -> str:
        """Set the loop position of a clip.

        Args:
            track_index: Track index (0-based)
            clip_index: Clip/scene index (0-based)
            position: Position in beats

        Returns:
            Confirmation message
        """
        clip = Clip(get_client())
        clip.set_position(track_index, clip_index, position)
        return f"Clip position set to {position} beats"

    # =============================================================================
    # Audio Clip Properties
    # =============================================================================

    @mcp.tool()
    def clip_get_warp_mode(
        track_index: Annotated[int, Field(description="Track index (0-based)", ge=0)],
        clip_index: Annotated[int, Field(description="Clip/scene index (0-based)", ge=0)]
    ) -> int:
        """Get the warp mode for an audio clip.

        Args:
            track_index: Track index (0-based)
            clip_index: Clip/scene index (0-based)

        Returns:
            Warp mode (0=Beats, 1=Tones, 2=Texture, 3=Re-Pitch, 4=Complex, 5=Complex Pro)
        """
        clip = Clip(get_client())
        return clip.get_warp_mode(track_index, clip_index)

    @mcp.tool()
    def clip_set_warp_mode(
        track_index: Annotated[int, Field(description="Track index (0-based)", ge=0)],
        clip_index: Annotated[int, Field(description="Clip/scene index (0-based)", ge=0)],
        mode: Annotated[int, Field(description="Warp mode (0=Beats, 1=Tones, 2=Texture, 3=Re-Pitch, 4=Complex, 5=Complex Pro)", ge=0, le=5)]
    ) -> str:
        """Set the warp mode for an audio clip.

        Args:
            track_index: Track index (0-based)
            clip_index: Clip/scene index (0-based)
            mode: Warp mode (0=Beats, 1=Tones, 2=Texture, 3=Re-Pitch, 4=Complex, 5=Complex Pro)

        Returns:
            Confirmation message
        """
        clip = Clip(get_client())
        clip.set_warp_mode(track_index, clip_index, mode)
        mode_names = ["Beats", "Tones", "Texture", "Re-Pitch", "Complex", "Complex Pro"]
        return f"Clip warp mode set to {mode_names[mode]}"

    @mcp.tool()
    def clip_get_warping(
        track_index: Annotated[int, Field(description="Track index (0-based)", ge=0)],
        clip_index: Annotated[int, Field(description="Clip/scene index (0-based)", ge=0)]
    ) -> bool:
        """Check if warping is enabled for an audio clip.

        Args:
            track_index: Track index (0-based)
            clip_index: Clip/scene index (0-based)

        Returns:
            True if warping is enabled
        """
        clip = Clip(get_client())
        return clip.get_warping(track_index, clip_index)

    @mcp.tool()
    def clip_set_warping(
        track_index: Annotated[int, Field(description="Track index (0-based)", ge=0)],
        clip_index: Annotated[int, Field(description="Clip/scene index (0-based)", ge=0)],
        enabled: Annotated[bool, Field(description="True to enable warping")]
    ) -> str:
        """Enable or disable warping for an audio clip.

        Args:
            track_index: Track index (0-based)
            clip_index: Clip/scene index (0-based)
            enabled: True to enable warping

        Returns:
            Confirmation message
        """
        clip = Clip(get_client())
        clip.set_warping(track_index, clip_index, enabled)
        state = "enabled" if enabled else "disabled"
        return f"Clip warping {state}"

    @mcp.tool()
    def clip_get_pitch_coarse(
        track_index: Annotated[int, Field(description="Track index (0-based)", ge=0)],
        clip_index: Annotated[int, Field(description="Clip/scene index (0-based)", ge=0)]
    ) -> int:
        """Get the coarse pitch adjustment for a clip (audio clips only).

        Args:
            track_index: Track index (0-based)
            clip_index: Clip/scene index (0-based)

        Returns:
            Pitch adjustment in semitones (-48 to +48)
        """
        clip = Clip(get_client())
        return clip.get_pitch_coarse(track_index, clip_index)

    @mcp.tool()
    def clip_set_pitch_coarse(
        track_index: Annotated[int, Field(description="Track index (0-based)", ge=0)],
        clip_index: Annotated[int, Field(description="Clip/scene index (0-based)", ge=0)],
        pitch: Annotated[int, Field(description="Pitch adjustment in semitones (-48 to +48)", ge=-48, le=48)]
    ) -> str:
        """Set the coarse pitch adjustment for a clip.

        Args:
            track_index: Track index (0-based)
            clip_index: Clip/scene index (0-based)
            pitch: Pitch adjustment in semitones (-48 to +48)

        Returns:
            Confirmation message
        """
        clip = Clip(get_client())
        clip.set_pitch_coarse(track_index, clip_index, pitch)
        return f"Clip pitch coarse set to {pitch} semitones"

    @mcp.tool()
    def clip_get_pitch_fine(
        track_index: Annotated[int, Field(description="Track index (0-based)", ge=0)],
        clip_index: Annotated[int, Field(description="Clip/scene index (0-based)", ge=0)]
    ) -> float:
        """Get the fine pitch adjustment for a clip (audio clips only).

        Args:
            track_index: Track index (0-based)
            clip_index: Clip/scene index (0-based)

        Returns:
            Fine pitch adjustment in cents (-50 to +50)
        """
        clip = Clip(get_client())
        return clip.get_pitch_fine(track_index, clip_index)

    @mcp.tool()
    def clip_set_pitch_fine(
        track_index: Annotated[int, Field(description="Track index (0-based)", ge=0)],
        clip_index: Annotated[int, Field(description="Clip/scene index (0-based)", ge=0)],
        cents: Annotated[float, Field(description="Fine pitch adjustment in cents (-50 to +50)", ge=-50, le=50)]
    ) -> str:
        """Set the fine pitch adjustment for a clip.

        Args:
            track_index: Track index (0-based)
            clip_index: Clip/scene index (0-based)
            cents: Fine pitch adjustment in cents (-50 to +50)

        Returns:
            Confirmation message
        """
        clip = Clip(get_client())
        clip.set_pitch_fine(track_index, clip_index, cents)
        return f"Clip pitch fine set to {cents} cents"

    @mcp.tool()
    def clip_get_gain(
        track_index: Annotated[int, Field(description="Track index (0-based)", ge=0)],
        clip_index: Annotated[int, Field(description="Clip/scene index (0-based)", ge=0)]
    ) -> float:
        """Get the gain for an audio clip.

        Args:
            track_index: Track index (0-based)
            clip_index: Clip/scene index (0-based)

        Returns:
            Gain level (typically 0.0-1.0, where 1.0 is unity gain)
        """
        clip = Clip(get_client())
        return clip.get_gain(track_index, clip_index)

    @mcp.tool()
    def clip_set_gain(
        track_index: Annotated[int, Field(description="Track index (0-based)", ge=0)],
        clip_index: Annotated[int, Field(description="Clip/scene index (0-based)", ge=0)],
        gain: Annotated[float, Field(description="Gain level", ge=0)]
    ) -> str:
        """Set the gain for an audio clip.

        Args:
            track_index: Track index (0-based)
            clip_index: Clip/scene index (0-based)
            gain: Gain level (typically 0.0-1.0)

        Returns:
            Confirmation message
        """
        clip = Clip(get_client())
        clip.set_gain(track_index, clip_index, gain)
        return f"Clip gain set to {gain}"

    @mcp.tool()
    def clip_get_sample_length(
        track_index: Annotated[int, Field(description="Track index (0-based)", ge=0)],
        clip_index: Annotated[int, Field(description="Clip/scene index (0-based)", ge=0)]
    ) -> float:
        """Get the sample length of an audio clip.

        Args:
            track_index: Track index (0-based)
            clip_index: Clip/scene index (0-based)

        Returns:
            Sample length in samples
        """
        clip = Clip(get_client())
        return clip.get_sample_length(track_index, clip_index)

    @mcp.tool()
    def clip_get_file_path(
        track_index: Annotated[int, Field(description="Track index (0-based)", ge=0)],
        clip_index: Annotated[int, Field(description="Clip/scene index (0-based)", ge=0)]
    ) -> str:
        """Get the file path of an audio clip.

        Args:
            track_index: Track index (0-based)
            clip_index: Clip/scene index (0-based)

        Returns:
            File path string, or empty string for MIDI clips
        """
        clip = Clip(get_client())
        return clip.get_file_path(track_index, clip_index)

    @mcp.tool()
    def clip_get_ram_mode(
        track_index: Annotated[int, Field(description="Track index (0-based)", ge=0)],
        clip_index: Annotated[int, Field(description="Clip/scene index (0-based)", ge=0)]
    ) -> bool:
        """Check if RAM mode is enabled for an audio clip.

        When RAM mode is enabled, the entire clip is loaded into RAM.

        Args:
            track_index: Track index (0-based)
            clip_index: Clip/scene index (0-based)

        Returns:
            True if RAM mode is enabled
        """
        clip = Clip(get_client())
        return clip.get_ram_mode(track_index, clip_index)

    @mcp.tool()
    def clip_set_ram_mode(
        track_index: Annotated[int, Field(description="Track index (0-based)", ge=0)],
        clip_index: Annotated[int, Field(description="Clip/scene index (0-based)", ge=0)],
        enabled: Annotated[bool, Field(description="True to load clip into RAM")]
    ) -> str:
        """Enable or disable RAM mode for an audio clip.

        Args:
            track_index: Track index (0-based)
            clip_index: Clip/scene index (0-based)
            enabled: True to load clip into RAM

        Returns:
            Confirmation message
        """
        clip = Clip(get_client())
        clip.set_ram_mode(track_index, clip_index, enabled)
        state = "enabled" if enabled else "disabled"
        return f"Clip RAM mode {state}"

    # =============================================================================
    # MIDI Clip Properties
    # =============================================================================

    @mcp.tool()
    def clip_get_velocity_amount(
        track_index: Annotated[int, Field(description="Track index (0-based)", ge=0)],
        clip_index: Annotated[int, Field(description="Clip/scene index (0-based)", ge=0)]
    ) -> float:
        """Get the velocity amount scaling for a MIDI clip.

        Args:
            track_index: Track index (0-based)
            clip_index: Clip/scene index (0-based)

        Returns:
            Velocity amount (0.0-1.0)
        """
        clip = Clip(get_client())
        return clip.get_velocity_amount(track_index, clip_index)

    @mcp.tool()
    def clip_set_velocity_amount(
        track_index: Annotated[int, Field(description="Track index (0-based)", ge=0)],
        clip_index: Annotated[int, Field(description="Clip/scene index (0-based)", ge=0)],
        amount: Annotated[float, Field(description="Velocity amount (0.0-1.0)", ge=0, le=1)]
    ) -> str:
        """Set the velocity amount scaling for a MIDI clip.

        Args:
            track_index: Track index (0-based)
            clip_index: Clip/scene index (0-based)
            amount: Velocity amount (0.0-1.0)

        Returns:
            Confirmation message
        """
        clip = Clip(get_client())
        clip.set_velocity_amount(track_index, clip_index, amount)
        return f"Clip velocity amount set to {amount}"

    @mcp.tool()
    def clip_get_legato(
        track_index: Annotated[int, Field(description="Track index (0-based)", ge=0)],
        clip_index: Annotated[int, Field(description="Clip/scene index (0-based)", ge=0)]
    ) -> bool:
        """Check if legato mode is enabled for a MIDI clip.

        Args:
            track_index: Track index (0-based)
            clip_index: Clip/scene index (0-based)

        Returns:
            True if legato is enabled
        """
        clip = Clip(get_client())
        return clip.get_legato(track_index, clip_index)

    @mcp.tool()
    def clip_set_legato(
        track_index: Annotated[int, Field(description="Track index (0-based)", ge=0)],
        clip_index: Annotated[int, Field(description="Clip/scene index (0-based)", ge=0)],
        enabled: Annotated[bool, Field(description="True to enable legato")]
    ) -> str:
        """Enable or disable legato mode for a MIDI clip.

        Args:
            track_index: Track index (0-based)
            clip_index: Clip/scene index (0-based)
            enabled: True to enable legato

        Returns:
            Confirmation message
        """
        clip = Clip(get_client())
        clip.set_legato(track_index, clip_index, enabled)
        state = "enabled" if enabled else "disabled"
        return f"Clip legato {state}"

    # =============================================================================
    # Recording State
    # =============================================================================

    @mcp.tool()
    def clip_get_is_recording(
        track_index: Annotated[int, Field(description="Track index (0-based)", ge=0)],
        clip_index: Annotated[int, Field(description="Clip/scene index (0-based)", ge=0)]
    ) -> bool:
        """Check if clip is currently recording.

        Args:
            track_index: Track index (0-based)
            clip_index: Clip/scene index (0-based)

        Returns:
            True if recording
        """
        clip = Clip(get_client())
        return clip.get_is_recording(track_index, clip_index)

    @mcp.tool()
    def clip_get_is_overdubbing(
        track_index: Annotated[int, Field(description="Track index (0-based)", ge=0)],
        clip_index: Annotated[int, Field(description="Clip/scene index (0-based)", ge=0)]
    ) -> bool:
        """Check if clip is currently overdubbing.

        Args:
            track_index: Track index (0-based)
            clip_index: Clip/scene index (0-based)

        Returns:
            True if overdubbing
        """
        clip = Clip(get_client())
        return clip.get_is_overdubbing(track_index, clip_index)

    @mcp.tool()
    def clip_get_will_record_on_start(
        track_index: Annotated[int, Field(description="Track index (0-based)", ge=0)],
        clip_index: Annotated[int, Field(description="Clip/scene index (0-based)", ge=0)]
    ) -> bool:
        """Check if clip will start recording when launched.

        Args:
            track_index: Track index (0-based)
            clip_index: Clip/scene index (0-based)

        Returns:
            True if will record on start
        """
        clip = Clip(get_client())
        return clip.get_will_record_on_start(track_index, clip_index)

    @mcp.tool()
    def clip_get_has_groove(
        track_index: Annotated[int, Field(description="Track index (0-based)", ge=0)],
        clip_index: Annotated[int, Field(description="Clip/scene index (0-based)", ge=0)]
    ) -> bool:
        """Check if clip has a groove applied.

        Args:
            track_index: Track index (0-based)
            clip_index: Clip/scene index (0-based)

        Returns:
            True if clip has a groove
        """
        clip = Clip(get_client())
        return clip.get_has_groove(track_index, clip_index)
