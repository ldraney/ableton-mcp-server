"""Clip slot tools for the Ableton MCP server.

Covers clip slot operations like creating, deleting, and managing clips in slots.
"""

from typing import Annotated

from pydantic import Field

from ableton_mcp.connection import get_client
from abletonosc_client import ClipSlot


def register_clip_slot_tools(mcp):
    """Register all clip slot tools with the MCP server."""

    @mcp.tool()
    def clip_slot_has_clip(
        track_index: Annotated[int, Field(description="Track index (0-based)", ge=0)],
        scene_index: Annotated[int, Field(description="Scene index (0-based)", ge=0)]
    ) -> bool:
        """Check if a clip slot contains a clip.

        Args:
            track_index: Track index (0-based)
            scene_index: Scene index (0-based)

        Returns:
            True if the slot contains a clip
        """
        clip_slot = ClipSlot(get_client())
        return clip_slot.has_clip(track_index, scene_index)

    @mcp.tool()
    def clip_slot_create_clip(
        track_index: Annotated[int, Field(description="Track index (0-based)", ge=0)],
        scene_index: Annotated[int, Field(description="Scene index (0-based)", ge=0)],
        length: Annotated[float, Field(description="Clip length in beats", gt=0)] = 4.0
    ) -> str:
        """Create a new MIDI clip in a clip slot.

        Args:
            track_index: Track index (0-based)
            scene_index: Scene index (0-based)
            length: Clip length in beats (default 4.0 = 1 bar at 4/4)

        Returns:
            Confirmation message
        """
        clip_slot = ClipSlot(get_client())
        clip_slot.create_clip(track_index, scene_index, length)
        return f"Clip created at track {track_index}, scene {scene_index} with length {length} beats"

    @mcp.tool()
    def clip_slot_delete_clip(
        track_index: Annotated[int, Field(description="Track index (0-based)", ge=0)],
        scene_index: Annotated[int, Field(description="Scene index (0-based)", ge=0)]
    ) -> str:
        """Delete a clip from a clip slot.

        Args:
            track_index: Track index (0-based)
            scene_index: Scene index (0-based)

        Returns:
            Confirmation message
        """
        clip_slot = ClipSlot(get_client())
        clip_slot.delete_clip(track_index, scene_index)
        return f"Clip deleted from track {track_index}, scene {scene_index}"

    @mcp.tool()
    def clip_slot_fire(
        track_index: Annotated[int, Field(description="Track index (0-based)", ge=0)],
        scene_index: Annotated[int, Field(description="Scene index (0-based)", ge=0)]
    ) -> str:
        """Fire (launch) the clip in a clip slot.

        Args:
            track_index: Track index (0-based)
            scene_index: Scene index (0-based)

        Returns:
            Confirmation message
        """
        clip_slot = ClipSlot(get_client())
        clip_slot.fire(track_index, scene_index)
        return f"Clip slot fired at track {track_index}, scene {scene_index}"

    @mcp.tool()
    def clip_slot_stop(
        track_index: Annotated[int, Field(description="Track index (0-based)", ge=0)],
        scene_index: Annotated[int, Field(description="Scene index (0-based)", ge=0)]
    ) -> str:
        """Stop the clip in a clip slot.

        Args:
            track_index: Track index (0-based)
            scene_index: Scene index (0-based)

        Returns:
            Confirmation message
        """
        clip_slot = ClipSlot(get_client())
        clip_slot.stop(track_index, scene_index)
        return f"Clip slot stopped at track {track_index}, scene {scene_index}"

    @mcp.tool()
    def clip_slot_get_is_playing(
        track_index: Annotated[int, Field(description="Track index (0-based)", ge=0)],
        scene_index: Annotated[int, Field(description="Scene index (0-based)", ge=0)]
    ) -> bool:
        """Check if the clip in a clip slot is playing.

        Args:
            track_index: Track index (0-based)
            scene_index: Scene index (0-based)

        Returns:
            True if playing
        """
        clip_slot = ClipSlot(get_client())
        return clip_slot.get_is_playing(track_index, scene_index)

    @mcp.tool()
    def clip_slot_get_is_triggered(
        track_index: Annotated[int, Field(description="Track index (0-based)", ge=0)],
        scene_index: Annotated[int, Field(description="Scene index (0-based)", ge=0)]
    ) -> bool:
        """Check if a clip slot is triggered (about to play).

        Args:
            track_index: Track index (0-based)
            scene_index: Scene index (0-based)

        Returns:
            True if triggered
        """
        clip_slot = ClipSlot(get_client())
        return clip_slot.get_is_triggered(track_index, scene_index)

    @mcp.tool()
    def clip_slot_get_is_recording(
        track_index: Annotated[int, Field(description="Track index (0-based)", ge=0)],
        scene_index: Annotated[int, Field(description="Scene index (0-based)", ge=0)]
    ) -> bool:
        """Check if a clip slot is recording.

        Args:
            track_index: Track index (0-based)
            scene_index: Scene index (0-based)

        Returns:
            True if recording
        """
        clip_slot = ClipSlot(get_client())
        return clip_slot.get_is_recording(track_index, scene_index)

    @mcp.tool()
    def clip_slot_get_has_stop_button(
        track_index: Annotated[int, Field(description="Track index (0-based)", ge=0)],
        scene_index: Annotated[int, Field(description="Scene index (0-based)", ge=0)]
    ) -> bool:
        """Check if a clip slot has a stop button.

        Args:
            track_index: Track index (0-based)
            scene_index: Scene index (0-based)

        Returns:
            True if slot has a stop button
        """
        clip_slot = ClipSlot(get_client())
        return clip_slot.get_has_stop_button(track_index, scene_index)

    @mcp.tool()
    def clip_slot_set_has_stop_button(
        track_index: Annotated[int, Field(description="Track index (0-based)", ge=0)],
        scene_index: Annotated[int, Field(description="Scene index (0-based)", ge=0)],
        has_button: Annotated[bool, Field(description="True to show stop button")]
    ) -> str:
        """Set whether a clip slot has a stop button.

        Args:
            track_index: Track index (0-based)
            scene_index: Scene index (0-based)
            has_button: True to show stop button

        Returns:
            Confirmation message
        """
        clip_slot = ClipSlot(get_client())
        clip_slot.set_has_stop_button(track_index, scene_index, has_button)
        state = "shown" if has_button else "hidden"
        return f"Clip slot stop button {state} at track {track_index}, scene {scene_index}"

    @mcp.tool()
    def clip_slot_duplicate_clip_to(
        track_index: Annotated[int, Field(description="Source track index (0-based)", ge=0)],
        scene_index: Annotated[int, Field(description="Source scene index (0-based)", ge=0)],
        dest_track_index: Annotated[int, Field(description="Destination track index (0-based)", ge=0)],
        dest_scene_index: Annotated[int, Field(description="Destination scene index (0-based)", ge=0)]
    ) -> str:
        """Duplicate a clip to another slot.

        Args:
            track_index: Source track index (0-based)
            scene_index: Source scene index (0-based)
            dest_track_index: Destination track index (0-based)
            dest_scene_index: Destination scene index (0-based)

        Returns:
            Confirmation message
        """
        clip_slot = ClipSlot(get_client())
        clip_slot.duplicate_clip_to(track_index, scene_index, dest_track_index, dest_scene_index)
        return f"Clip duplicated from ({track_index}, {scene_index}) to ({dest_track_index}, {dest_scene_index})"
