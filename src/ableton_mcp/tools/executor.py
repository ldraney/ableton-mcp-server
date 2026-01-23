"""Executor tools for the Ableton MCP server.

Execute song-schema JSON files with proper timing for recording to arrangement view.
Delegates to the song-executor package for execution logic.
"""

from pathlib import Path
from typing import Annotated

from pydantic import Field

from ableton_mcp.connection import get_client
from song_executor import SongExecutor


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
        # Expand path and validate
        path = Path(song_path).expanduser()
        if not path.exists():
            return f"Error: File not found: {song_path}"

        # Create executor with shared MCP client
        client = get_client()
        executor = SongExecutor(str(path), client=client)
        executor.load()

        # Build info string
        lines = [
            f"Song: {path.name}",
            f"Tempo: {executor.tempo} BPM, Time Signature: {executor.time_signature[0]}/{executor.time_signature[1]}",
            f"Total: {len(executor.sections)} sections, {executor.total_beats:.0f} beats, {executor.total_duration_seconds:.1f} seconds",
            "",
            "Sections:"
        ]

        for i, section in enumerate(executor.sections):
            bars = section.get("bars", 4)
            dur_sec = bars * executor.beats_per_bar * (60.0 / executor.tempo)
            name = section.get("name", f"section_{i}")
            lines.append(f"  {i}: {name} ({bars} bars, {dur_sec:.1f}s)")

        if dry_run:
            lines.append("")
            lines.append("[DRY RUN] No execution performed")
            return "\n".join(lines)

        lines.append("")
        lines.append("Executing...")

        # Execute via song-executor
        executor.execute(record=record, dry_run=False)

        lines.append("")
        lines.append(f"Complete! Recorded {executor.total_duration_seconds:.1f} seconds to arrangement view.")

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
