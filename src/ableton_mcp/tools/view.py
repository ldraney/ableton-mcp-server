"""View tools for the Ableton MCP server.

Covers view operations like track/scene/clip/device selection and navigation.
"""

from typing import Annotated

from pydantic import Field

from ableton_mcp.connection import get_client
from abletonosc_client import View


def register_view_tools(mcp):
    """Register all view tools with the MCP server."""

    # =============================================================================
    # Track Selection
    # =============================================================================

    @mcp.tool()
    def view_get_selected_track() -> int:
        """Get the currently selected track index.

        Returns:
            Selected track index (0-based)
        """
        view = View(get_client())
        return view.get_selected_track()

    @mcp.tool()
    def view_set_selected_track(
        track_index: Annotated[int, Field(description="Track index (0-based)", ge=0)]
    ) -> str:
        """Select a track in the view.

        Args:
            track_index: Track index (0-based)

        Returns:
            Confirmation message
        """
        view = View(get_client())
        view.set_selected_track(track_index)
        return f"Track {track_index} selected"

    # =============================================================================
    # Scene Selection
    # =============================================================================

    @mcp.tool()
    def view_get_selected_scene() -> int:
        """Get the currently selected scene index.

        Returns:
            Selected scene index (0-based)
        """
        view = View(get_client())
        return view.get_selected_scene()

    @mcp.tool()
    def view_set_selected_scene(
        scene_index: Annotated[int, Field(description="Scene index (0-based)", ge=0)]
    ) -> str:
        """Select a scene in the view.

        Args:
            scene_index: Scene index (0-based)

        Returns:
            Confirmation message
        """
        view = View(get_client())
        view.set_selected_scene(scene_index)
        return f"Scene {scene_index} selected"

    # =============================================================================
    # Clip Selection
    # =============================================================================

    @mcp.tool()
    def view_get_selected_clip() -> dict:
        """Get the currently selected clip.

        Returns:
            Dict with track_index and clip_index, or both -1 if none selected
        """
        view = View(get_client())
        track_index, clip_index = view.get_selected_clip()
        return {"track_index": track_index, "clip_index": clip_index}

    @mcp.tool()
    def view_set_selected_clip(
        track_index: Annotated[int, Field(description="Track index (0-based)", ge=0)],
        clip_index: Annotated[int, Field(description="Clip/scene index (0-based)", ge=0)]
    ) -> str:
        """Set the selected clip.

        Args:
            track_index: Track index (0-based)
            clip_index: Clip/scene index (0-based)

        Returns:
            Confirmation message
        """
        view = View(get_client())
        view.set_selected_clip(track_index, clip_index)
        return f"Clip at track {track_index}, scene {clip_index} selected"

    # =============================================================================
    # Device Selection
    # =============================================================================

    @mcp.tool()
    def view_get_selected_device() -> dict:
        """Get the currently selected device.

        Returns:
            Dict with track_index and device_index, or both -1 if none selected
        """
        view = View(get_client())
        track_index, device_index = view.get_selected_device()
        return {"track_index": track_index, "device_index": device_index}

    @mcp.tool()
    def view_set_selected_device(
        track_index: Annotated[int, Field(description="Track index (0-based)", ge=0)],
        device_index: Annotated[int, Field(description="Device index (0-based)", ge=0)]
    ) -> str:
        """Set the selected device.

        Args:
            track_index: Track index (0-based)
            device_index: Device index (0-based)

        Returns:
            Confirmation message
        """
        view = View(get_client())
        view.set_selected_device(track_index, device_index)
        return f"Device {device_index} on track {track_index} selected"

    # =============================================================================
    # Detail Clip
    # =============================================================================

    @mcp.tool()
    def view_get_detail_clip() -> dict:
        """Get the track and clip index of the clip shown in detail view.

        Returns:
            Dict with track_index and clip_index
        """
        view = View(get_client())
        track_index, clip_index = view.get_detail_clip()
        return {"track_index": track_index, "clip_index": clip_index}

    @mcp.tool()
    def view_set_detail_clip(
        track_index: Annotated[int, Field(description="Track index (0-based)", ge=0)],
        clip_index: Annotated[int, Field(description="Clip/scene index (0-based)", ge=0)]
    ) -> str:
        """Set which clip is shown in detail view.

        Args:
            track_index: Track index (0-based)
            clip_index: Clip/scene index (0-based)

        Returns:
            Confirmation message
        """
        view = View(get_client())
        view.set_detail_clip(track_index, clip_index)
        return f"Detail view showing clip at track {track_index}, scene {clip_index}"

    # =============================================================================
    # View Visibility
    # =============================================================================

    @mcp.tool()
    def view_get_is_view_visible(
        view_name: Annotated[str, Field(description="View name (e.g., 'Session', 'Arranger', 'Detail', 'Browser')")]
    ) -> bool:
        """Check if a view is visible.

        Args:
            view_name: View name (e.g., "Session", "Arranger", "Detail", "Browser")

        Returns:
            True if visible
        """
        view = View(get_client())
        return view.get_is_view_visible(view_name)

    @mcp.tool()
    def view_focus_view(
        view_name: Annotated[str, Field(description="View name (e.g., 'Session', 'Arranger', 'Detail', 'Browser')")]
    ) -> str:
        """Focus a specific view.

        Args:
            view_name: View name (e.g., "Session", "Arranger", "Detail", "Browser")

        Returns:
            Confirmation message
        """
        view = View(get_client())
        view.focus_view(view_name)
        return f"Focused {view_name} view"
