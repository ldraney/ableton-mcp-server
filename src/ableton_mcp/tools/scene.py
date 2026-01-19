"""Scene tools for the Ableton MCP server.

Covers scene-level operations like firing, naming, and tempo/time signature settings.
"""

from typing import Annotated

from pydantic import Field

from ableton_mcp.connection import get_client
from abletonosc_client import Scene


def register_scene_tools(mcp):
    """Register all scene tools with the MCP server."""

    # =============================================================================
    # Name
    # =============================================================================

    @mcp.tool()
    def scene_get_name(
        scene_index: Annotated[int, Field(description="Scene index (0-based)", ge=0)]
    ) -> str:
        """Get the name of a scene.

        Args:
            scene_index: Scene index (0-based)

        Returns:
            Scene name
        """
        scene = Scene(get_client())
        return scene.get_name(scene_index)

    @mcp.tool()
    def scene_set_name(
        scene_index: Annotated[int, Field(description="Scene index (0-based)", ge=0)],
        name: Annotated[str, Field(description="New scene name")]
    ) -> str:
        """Set the name of a scene.

        Args:
            scene_index: Scene index (0-based)
            name: New scene name

        Returns:
            Confirmation message
        """
        scene = Scene(get_client())
        scene.set_name(scene_index, name)
        return f"Scene {scene_index} renamed to '{name}'"

    # =============================================================================
    # Fire
    # =============================================================================

    @mcp.tool()
    def scene_fire(
        scene_index: Annotated[int, Field(description="Scene index (0-based)", ge=0)]
    ) -> str:
        """Fire (launch) a scene.

        This launches all clips in the scene row.

        Args:
            scene_index: Scene index (0-based)

        Returns:
            Confirmation message
        """
        scene = Scene(get_client())
        scene.fire(scene_index)
        return f"Scene {scene_index} fired"

    @mcp.tool()
    def scene_fire_as_selected(
        scene_index: Annotated[int, Field(description="Scene index (0-based)", ge=0)]
    ) -> str:
        """Fire a scene and make it the selected scene.

        Args:
            scene_index: Scene index (0-based)

        Returns:
            Confirmation message
        """
        scene = Scene(get_client())
        scene.fire_as_selected(scene_index)
        return f"Scene {scene_index} fired and selected"

    @mcp.tool()
    def scene_fire_selected() -> str:
        """Fire the currently selected scene.

        This fires whichever scene is currently selected in the UI.

        Returns:
            Confirmation message
        """
        scene = Scene(get_client())
        scene.fire_selected()
        return "Selected scene fired"

    # =============================================================================
    # Color
    # =============================================================================

    @mcp.tool()
    def scene_get_color(
        scene_index: Annotated[int, Field(description="Scene index (0-based)", ge=0)]
    ) -> int:
        """Get the color of a scene.

        Args:
            scene_index: Scene index (0-based)

        Returns:
            Color as integer
        """
        scene = Scene(get_client())
        return scene.get_color(scene_index)

    @mcp.tool()
    def scene_set_color(
        scene_index: Annotated[int, Field(description="Scene index (0-based)", ge=0)],
        color: Annotated[int, Field(description="Color as integer")]
    ) -> str:
        """Set the color of a scene.

        Args:
            scene_index: Scene index (0-based)
            color: Color as integer

        Returns:
            Confirmation message
        """
        scene = Scene(get_client())
        scene.set_color(scene_index, color)
        return f"Scene {scene_index} color set to {color}"

    @mcp.tool()
    def scene_get_color_index(
        scene_index: Annotated[int, Field(description="Scene index (0-based)", ge=0)]
    ) -> int:
        """Get the color index of a scene.

        Args:
            scene_index: Scene index (0-based)

        Returns:
            Color index (0-69)
        """
        scene = Scene(get_client())
        return scene.get_color_index(scene_index)

    @mcp.tool()
    def scene_set_color_index(
        scene_index: Annotated[int, Field(description="Scene index (0-based)", ge=0)],
        color_index: Annotated[int, Field(description="Color index (0-69)", ge=0, le=69)]
    ) -> str:
        """Set the color index of a scene.

        Args:
            scene_index: Scene index (0-based)
            color_index: Color index (0-69)

        Returns:
            Confirmation message
        """
        scene = Scene(get_client())
        scene.set_color_index(scene_index, color_index)
        return f"Scene {scene_index} color index set to {color_index}"

    # =============================================================================
    # Tempo
    # =============================================================================

    @mcp.tool()
    def scene_get_tempo(
        scene_index: Annotated[int, Field(description="Scene index (0-based)", ge=0)]
    ) -> float:
        """Get the tempo of a scene (if set).

        Args:
            scene_index: Scene index (0-based)

        Returns:
            Scene tempo in BPM, or 0 if not set
        """
        scene = Scene(get_client())
        return scene.get_tempo(scene_index)

    @mcp.tool()
    def scene_set_tempo(
        scene_index: Annotated[int, Field(description="Scene index (0-based)", ge=0)],
        tempo: Annotated[float, Field(description="Tempo in BPM", ge=20, le=999)]
    ) -> str:
        """Set the tempo of a scene.

        Args:
            scene_index: Scene index (0-based)
            tempo: Tempo in BPM

        Returns:
            Confirmation message
        """
        scene = Scene(get_client())
        scene.set_tempo(scene_index, tempo)
        return f"Scene {scene_index} tempo set to {tempo} BPM"

    @mcp.tool()
    def scene_get_tempo_enabled(
        scene_index: Annotated[int, Field(description="Scene index (0-based)", ge=0)]
    ) -> bool:
        """Check if scene tempo is enabled.

        When enabled, launching this scene will change the song tempo
        to the scene's tempo value.

        Args:
            scene_index: Scene index (0-based)

        Returns:
            True if scene tempo is enabled
        """
        scene = Scene(get_client())
        return scene.get_tempo_enabled(scene_index)

    @mcp.tool()
    def scene_set_tempo_enabled(
        scene_index: Annotated[int, Field(description="Scene index (0-based)", ge=0)],
        enabled: Annotated[bool, Field(description="True to enable scene tempo")]
    ) -> str:
        """Enable or disable scene tempo.

        Args:
            scene_index: Scene index (0-based)
            enabled: True to enable scene tempo

        Returns:
            Confirmation message
        """
        scene = Scene(get_client())
        scene.set_tempo_enabled(scene_index, enabled)
        state = "enabled" if enabled else "disabled"
        return f"Scene {scene_index} tempo {state}"

    # =============================================================================
    # Time Signature
    # =============================================================================

    @mcp.tool()
    def scene_get_time_signature_numerator(
        scene_index: Annotated[int, Field(description="Scene index (0-based)", ge=0)]
    ) -> int:
        """Get the time signature numerator for a scene.

        Args:
            scene_index: Scene index (0-based)

        Returns:
            Time signature numerator (e.g., 4 for 4/4)
        """
        scene = Scene(get_client())
        return scene.get_time_signature_numerator(scene_index)

    @mcp.tool()
    def scene_set_time_signature_numerator(
        scene_index: Annotated[int, Field(description="Scene index (0-based)", ge=0)],
        numerator: Annotated[int, Field(description="Time signature numerator", ge=1)]
    ) -> str:
        """Set the time signature numerator for a scene.

        Args:
            scene_index: Scene index (0-based)
            numerator: Time signature numerator

        Returns:
            Confirmation message
        """
        scene = Scene(get_client())
        scene.set_time_signature_numerator(scene_index, numerator)
        return f"Scene {scene_index} time signature numerator set to {numerator}"

    @mcp.tool()
    def scene_get_time_signature_denominator(
        scene_index: Annotated[int, Field(description="Scene index (0-based)", ge=0)]
    ) -> int:
        """Get the time signature denominator for a scene.

        Args:
            scene_index: Scene index (0-based)

        Returns:
            Time signature denominator (e.g., 4 for 4/4)
        """
        scene = Scene(get_client())
        return scene.get_time_signature_denominator(scene_index)

    @mcp.tool()
    def scene_set_time_signature_denominator(
        scene_index: Annotated[int, Field(description="Scene index (0-based)", ge=0)],
        denominator: Annotated[int, Field(description="Time signature denominator", ge=1)]
    ) -> str:
        """Set the time signature denominator for a scene.

        Args:
            scene_index: Scene index (0-based)
            denominator: Time signature denominator

        Returns:
            Confirmation message
        """
        scene = Scene(get_client())
        scene.set_time_signature_denominator(scene_index, denominator)
        return f"Scene {scene_index} time signature denominator set to {denominator}"

    @mcp.tool()
    def scene_get_time_signature_enabled(
        scene_index: Annotated[int, Field(description="Scene index (0-based)", ge=0)]
    ) -> bool:
        """Check if scene time signature is enabled.

        When enabled, launching this scene will change the song time signature
        to the scene's time signature value.

        Args:
            scene_index: Scene index (0-based)

        Returns:
            True if scene time signature is enabled
        """
        scene = Scene(get_client())
        return scene.get_time_signature_enabled(scene_index)

    @mcp.tool()
    def scene_set_time_signature_enabled(
        scene_index: Annotated[int, Field(description="Scene index (0-based)", ge=0)],
        enabled: Annotated[bool, Field(description="True to enable scene time signature")]
    ) -> str:
        """Enable or disable scene time signature.

        Args:
            scene_index: Scene index (0-based)
            enabled: True to enable scene time signature

        Returns:
            Confirmation message
        """
        scene = Scene(get_client())
        scene.set_time_signature_enabled(scene_index, enabled)
        state = "enabled" if enabled else "disabled"
        return f"Scene {scene_index} time signature {state}"

    # =============================================================================
    # State
    # =============================================================================

    @mcp.tool()
    def scene_get_is_triggered(
        scene_index: Annotated[int, Field(description="Scene index (0-based)", ge=0)]
    ) -> bool:
        """Check if a scene is triggered (about to play).

        Args:
            scene_index: Scene index (0-based)

        Returns:
            True if triggered
        """
        scene = Scene(get_client())
        return scene.get_is_triggered(scene_index)

    @mcp.tool()
    def scene_get_is_empty(
        scene_index: Annotated[int, Field(description="Scene index (0-based)", ge=0)]
    ) -> bool:
        """Check if a scene is empty (has no clips).

        Args:
            scene_index: Scene index (0-based)

        Returns:
            True if scene has no clips
        """
        scene = Scene(get_client())
        return scene.get_is_empty(scene_index)
