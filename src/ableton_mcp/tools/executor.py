"""Executor tools for the Ableton MCP server.

Execute song-schema JSON files with proper timing for recording to arrangement view.
"""

import json
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Annotated, Optional

from pydantic import Field

from ableton_mcp.connection import get_client
from abletonosc_client import Song, Scene


@dataclass
class SectionTiming:
    """Timing information for a song section."""
    name: str
    scene_index: int
    start_beat: float
    duration_beats: float
    bars: int


def _load_song_schema(song_path: str) -> dict:
    """Load and parse a song-schema JSON file."""
    with open(song_path) as f:
        return json.load(f)


def _calculate_timings(song_data: dict) -> list[SectionTiming]:
    """Calculate timing for each section."""
    timings = []
    current_beat = 0.0

    # Get time signature for beats per bar
    ts = song_data.get("metadata", {}).get("time_signature", {})
    beats_per_bar = ts.get("numerator", 4)

    sections = song_data.get("structure", {}).get("sections", [])

    for i, section in enumerate(sections):
        bars = section.get("bars", 4)
        duration_beats = bars * beats_per_bar

        timing = SectionTiming(
            name=section.get("name", f"section_{i}"),
            scene_index=i,
            start_beat=current_beat,
            duration_beats=duration_beats,
            bars=bars
        )
        timings.append(timing)
        current_beat += duration_beats

    return timings


def _beat_to_seconds(beat: float, tempo: float) -> float:
    """Convert beats to seconds at given tempo."""
    return beat * (60.0 / tempo)


def register_executor_tools(mcp):
    """Register all executor tools with the MCP server."""

    @mcp.tool()
    def song_execute(
        song_path: Annotated[str, Field(description="Path to the song-schema JSON file")],
        record: Annotated[bool, Field(description="Enable arrangement recording")] = True,
        dry_run: Annotated[bool, Field(description="Just print timing, don't execute")] = False
    ) -> str:
        """Execute a song-schema JSON file with proper timing.

        Fires scenes in sequence according to the structure.sections,
        waiting the appropriate duration for each section.
        Optionally records to arrangement view.

        Args:
            song_path: Path to the song.json file
            record: Whether to enable arrangement recording (default: True)
            dry_run: If True, just return timing info without executing

        Returns:
            Execution summary with timing details
        """
        # Load song data
        path = Path(song_path).expanduser()
        if not path.exists():
            return f"Error: File not found: {song_path}"

        song_data = _load_song_schema(str(path))
        timings = _calculate_timings(song_data)

        # Get metadata
        tempo = song_data.get("metadata", {}).get("tempo", 120)
        ts = song_data.get("metadata", {}).get("time_signature", {})
        ts_num = ts.get("numerator", 4)
        ts_denom = ts.get("denominator", 4)

        # Calculate totals
        total_beats = sum(t.duration_beats for t in timings)
        total_seconds = _beat_to_seconds(total_beats, tempo)

        # Build info string
        lines = [
            f"Song: {path.name}",
            f"Tempo: {tempo} BPM, Time Signature: {ts_num}/{ts_denom}",
            f"Total: {len(timings)} sections, {total_beats:.0f} beats, {total_seconds:.1f} seconds",
            "",
            "Sections:"
        ]

        for t in timings:
            dur_sec = _beat_to_seconds(t.duration_beats, tempo)
            lines.append(f"  {t.scene_index}: {t.name} ({t.bars} bars, {dur_sec:.1f}s)")

        if dry_run:
            lines.append("")
            lines.append("[DRY RUN] No execution performed")
            return "\n".join(lines)

        # Get Ableton controllers
        client = get_client()
        song = Song(client)
        scene = Scene(client)

        # Set tempo and time signature
        song.set_tempo(tempo)
        song.set_signature_numerator(ts_num)
        song.set_signature_denominator(ts_denom)
        song.set_current_song_time(0)

        # Enable recording if requested
        if record:
            song.set_record_mode(True)

        lines.append("")
        lines.append("Executing...")

        # Execute each section
        for i, timing in enumerate(timings):
            wait_time = _beat_to_seconds(timing.duration_beats, tempo)

            lines.append(f"  [{i+1}/{len(timings)}] {timing.name}: firing scene {timing.scene_index}")
            scene.fire(timing.scene_index)

            # Start playback on first scene
            if i == 0:
                time.sleep(0.1)
                song.start_playing()

            time.sleep(wait_time)

        # Stop playback
        song.stop_playing()

        if record:
            song.set_record_mode(False)

        lines.append("")
        lines.append(f"Complete! Recorded {total_seconds:.1f} seconds to arrangement view.")

        return "\n".join(lines)

    @mcp.tool()
    def song_execute_info(
        song_path: Annotated[str, Field(description="Path to the song-schema JSON file")]
    ) -> str:
        """Get timing info for a song-schema file without executing.

        Args:
            song_path: Path to the song.json file

        Returns:
            Song structure and timing information
        """
        return song_execute(song_path, record=False, dry_run=True)
