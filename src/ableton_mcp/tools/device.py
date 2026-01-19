"""Device tools for the Ableton MCP server.

Covers device-level operations like parameters, activation, and bulk operations.
"""

from typing import Annotated

from pydantic import Field

from ableton_mcp.connection import get_client
from abletonosc_client import Device


def register_device_tools(mcp):
    """Register all device tools with the MCP server."""

    # =============================================================================
    # Device Info
    # =============================================================================

    @mcp.tool()
    def device_get_name(
        track_index: Annotated[int, Field(description="Track index (0-based)", ge=0)],
        device_index: Annotated[int, Field(description="Device index (0-based)", ge=0)]
    ) -> str:
        """Get the name of a device.

        Args:
            track_index: Track index (0-based)
            device_index: Device index on track (0-based)

        Returns:
            Device name
        """
        device = Device(get_client())
        return device.get_name(track_index, device_index)

    @mcp.tool()
    def device_get_class_name(
        track_index: Annotated[int, Field(description="Track index (0-based)", ge=0)],
        device_index: Annotated[int, Field(description="Device index (0-based)", ge=0)]
    ) -> str:
        """Get the device class name (type).

        Args:
            track_index: Track index (0-based)
            device_index: Device index on track (0-based)

        Returns:
            Device class name (e.g., "Compressor", "Reverb")
        """
        device = Device(get_client())
        return device.get_class_name(track_index, device_index)

    @mcp.tool()
    def device_get_type(
        track_index: Annotated[int, Field(description="Track index (0-based)", ge=0)],
        device_index: Annotated[int, Field(description="Device index (0-based)", ge=0)]
    ) -> int:
        """Get the device type.

        Args:
            track_index: Track index (0-based)
            device_index: Device index on track (0-based)

        Returns:
            Device type (0=audio_effect, 1=instrument, 2=midi_effect)
        """
        device = Device(get_client())
        return device.get_type(track_index, device_index)

    # =============================================================================
    # Activation
    # =============================================================================

    @mcp.tool()
    def device_get_is_active(
        track_index: Annotated[int, Field(description="Track index (0-based)", ge=0)],
        device_index: Annotated[int, Field(description="Device index (0-based)", ge=0)]
    ) -> bool:
        """Check if a device is active (enabled).

        Args:
            track_index: Track index (0-based)
            device_index: Device index on track (0-based)

        Returns:
            True if device is active
        """
        device = Device(get_client())
        return device.get_is_active(track_index, device_index)

    @mcp.tool()
    def device_set_is_active(
        track_index: Annotated[int, Field(description="Track index (0-based)", ge=0)],
        device_index: Annotated[int, Field(description="Device index (0-based)", ge=0)],
        active: Annotated[bool, Field(description="True to enable, False to bypass")]
    ) -> str:
        """Enable or disable (bypass) a device.

        Args:
            track_index: Track index (0-based)
            device_index: Device index on track (0-based)
            active: True to enable, False to bypass

        Returns:
            Confirmation message
        """
        device = Device(get_client())
        device.set_is_active(track_index, device_index, active)
        state = "enabled" if active else "bypassed"
        return f"Device {device_index} on track {track_index} {state}"

    @mcp.tool()
    def device_set_enabled(
        track_index: Annotated[int, Field(description="Track index (0-based)", ge=0)],
        device_index: Annotated[int, Field(description="Device index (0-based)", ge=0)],
        enabled: Annotated[bool, Field(description="True to enable, False to bypass")]
    ) -> str:
        """Enable or disable (bypass) a device.

        Alias for device_set_is_active for backwards compatibility.

        Args:
            track_index: Track index (0-based)
            device_index: Device index on track (0-based)
            enabled: True to enable, False to bypass

        Returns:
            Confirmation message
        """
        device = Device(get_client())
        device.set_is_active(track_index, device_index, enabled)
        state = "enabled" if enabled else "bypassed"
        return f"Device {device_index} on track {track_index} {state}"

    # =============================================================================
    # Parameter Count
    # =============================================================================

    @mcp.tool()
    def device_get_num_parameters(
        track_index: Annotated[int, Field(description="Track index (0-based)", ge=0)],
        device_index: Annotated[int, Field(description="Device index (0-based)", ge=0)]
    ) -> int:
        """Get the number of parameters on a device.

        Args:
            track_index: Track index (0-based)
            device_index: Device index on track (0-based)

        Returns:
            Number of parameters
        """
        device = Device(get_client())
        return device.get_num_parameters(track_index, device_index)

    # =============================================================================
    # Individual Parameters
    # =============================================================================

    @mcp.tool()
    def device_get_parameter_value(
        track_index: Annotated[int, Field(description="Track index (0-based)", ge=0)],
        device_index: Annotated[int, Field(description="Device index (0-based)", ge=0)],
        parameter_index: Annotated[int, Field(description="Parameter index (0-based)", ge=0)]
    ) -> float:
        """Get a parameter value.

        Args:
            track_index: Track index (0-based)
            device_index: Device index on track (0-based)
            parameter_index: Parameter index (0-based)

        Returns:
            Current parameter value
        """
        device = Device(get_client())
        return device.get_parameter_value(track_index, device_index, parameter_index)

    @mcp.tool()
    def device_set_parameter_value(
        track_index: Annotated[int, Field(description="Track index (0-based)", ge=0)],
        device_index: Annotated[int, Field(description="Device index (0-based)", ge=0)],
        parameter_index: Annotated[int, Field(description="Parameter index (0-based)", ge=0)],
        value: Annotated[float, Field(description="New parameter value")]
    ) -> str:
        """Set a parameter value.

        Args:
            track_index: Track index (0-based)
            device_index: Device index on track (0-based)
            parameter_index: Parameter index (0-based)
            value: New parameter value

        Returns:
            Confirmation message
        """
        device = Device(get_client())
        device.set_parameter_value(track_index, device_index, parameter_index, value)
        return f"Parameter {parameter_index} on device {device_index} (track {track_index}) set to {value}"

    @mcp.tool()
    def device_set_parameter(
        track_index: Annotated[int, Field(description="Track index (0-based)", ge=0)],
        device_index: Annotated[int, Field(description="Device index (0-based)", ge=0)],
        parameter_index: Annotated[int, Field(description="Parameter index (0-based)", ge=0)],
        value: Annotated[float, Field(description="New parameter value")]
    ) -> str:
        """Set a device parameter value.

        Alias for device_set_parameter_value for backwards compatibility.

        Args:
            track_index: Track index (0-based)
            device_index: Device index on track (0-based)
            parameter_index: Parameter index (0-based)
            value: New parameter value

        Returns:
            Confirmation message
        """
        device = Device(get_client())
        device.set_parameter_value(track_index, device_index, parameter_index, value)
        return f"Parameter {parameter_index} on device {device_index} (track {track_index}) set to {value}"

    @mcp.tool()
    def device_get_parameter_name(
        track_index: Annotated[int, Field(description="Track index (0-based)", ge=0)],
        device_index: Annotated[int, Field(description="Device index (0-based)", ge=0)],
        parameter_index: Annotated[int, Field(description="Parameter index (0-based)", ge=0)]
    ) -> str:
        """Get a parameter name.

        Args:
            track_index: Track index (0-based)
            device_index: Device index on track (0-based)
            parameter_index: Parameter index (0-based)

        Returns:
            Parameter name
        """
        device = Device(get_client())
        return device.get_parameter_name(track_index, device_index, parameter_index)

    @mcp.tool()
    def device_get_parameter_min(
        track_index: Annotated[int, Field(description="Track index (0-based)", ge=0)],
        device_index: Annotated[int, Field(description="Device index (0-based)", ge=0)],
        parameter_index: Annotated[int, Field(description="Parameter index (0-based)", ge=0)]
    ) -> float:
        """Get a parameter's minimum value.

        Args:
            track_index: Track index (0-based)
            device_index: Device index on track (0-based)
            parameter_index: Parameter index (0-based)

        Returns:
            Minimum parameter value
        """
        device = Device(get_client())
        return device.get_parameter_min(track_index, device_index, parameter_index)

    @mcp.tool()
    def device_get_parameter_max(
        track_index: Annotated[int, Field(description="Track index (0-based)", ge=0)],
        device_index: Annotated[int, Field(description="Device index (0-based)", ge=0)],
        parameter_index: Annotated[int, Field(description="Parameter index (0-based)", ge=0)]
    ) -> float:
        """Get a parameter's maximum value.

        Args:
            track_index: Track index (0-based)
            device_index: Device index on track (0-based)
            parameter_index: Parameter index (0-based)

        Returns:
            Maximum parameter value
        """
        device = Device(get_client())
        return device.get_parameter_max(track_index, device_index, parameter_index)

    @mcp.tool()
    def device_get_parameter_value_string(
        track_index: Annotated[int, Field(description="Track index (0-based)", ge=0)],
        device_index: Annotated[int, Field(description="Device index (0-based)", ge=0)],
        parameter_index: Annotated[int, Field(description="Parameter index (0-based)", ge=0)]
    ) -> str:
        """Get a parameter's display string (formatted value with units).

        Args:
            track_index: Track index (0-based)
            device_index: Device index on track (0-based)
            parameter_index: Parameter index (0-based)

        Returns:
            Formatted parameter value string (e.g., "440 Hz", "-12 dB")
        """
        device = Device(get_client())
        return device.get_parameter_value_string(track_index, device_index, parameter_index)

    # =============================================================================
    # Bulk Parameters
    # =============================================================================

    @mcp.tool()
    def device_get_parameters(
        track_index: Annotated[int, Field(description="Track index (0-based)", ge=0)],
        device_index: Annotated[int, Field(description="Device index (0-based)", ge=0)]
    ) -> list[dict]:
        """Get all parameters for a device.

        Args:
            track_index: Track index (0-based)
            device_index: Device index on track (0-based)

        Returns:
            List of parameters, each with index, name, value, min, max
        """
        device = Device(get_client())
        params = device.get_parameters(track_index, device_index)
        return [
            {
                "index": p.index,
                "name": p.name,
                "value": p.value,
                "min": p.min,
                "max": p.max
            }
            for p in params
        ]

    @mcp.tool()
    def device_get_parameters_names(
        track_index: Annotated[int, Field(description="Track index (0-based)", ge=0)],
        device_index: Annotated[int, Field(description="Device index (0-based)", ge=0)]
    ) -> list[str]:
        """Get all parameter names for a device in a single query.

        Args:
            track_index: Track index (0-based)
            device_index: Device index on track (0-based)

        Returns:
            List of parameter names
        """
        device = Device(get_client())
        return list(device.get_parameters_names(track_index, device_index))

    @mcp.tool()
    def device_get_parameters_values(
        track_index: Annotated[int, Field(description="Track index (0-based)", ge=0)],
        device_index: Annotated[int, Field(description="Device index (0-based)", ge=0)]
    ) -> list[float]:
        """Get all parameter values for a device in a single query.

        Args:
            track_index: Track index (0-based)
            device_index: Device index on track (0-based)

        Returns:
            List of parameter values
        """
        device = Device(get_client())
        return list(device.get_parameters_values(track_index, device_index))

    @mcp.tool()
    def device_set_parameters_values(
        track_index: Annotated[int, Field(description="Track index (0-based)", ge=0)],
        device_index: Annotated[int, Field(description="Device index (0-based)", ge=0)],
        values: Annotated[list[float], Field(description="List of parameter values (one per parameter)")]
    ) -> str:
        """Set all parameter values for a device in a single call.

        Args:
            track_index: Track index (0-based)
            device_index: Device index on track (0-based)
            values: List of parameter values (one per parameter)

        Returns:
            Confirmation message
        """
        device = Device(get_client())
        device.set_parameters_values(track_index, device_index, values)
        return f"Set {len(values)} parameter values on device {device_index} (track {track_index})"

    @mcp.tool()
    def device_get_parameters_mins(
        track_index: Annotated[int, Field(description="Track index (0-based)", ge=0)],
        device_index: Annotated[int, Field(description="Device index (0-based)", ge=0)]
    ) -> list[float]:
        """Get all parameter minimum values for a device.

        Args:
            track_index: Track index (0-based)
            device_index: Device index on track (0-based)

        Returns:
            List of minimum values
        """
        device = Device(get_client())
        return list(device.get_parameters_mins(track_index, device_index))

    @mcp.tool()
    def device_get_parameters_maxs(
        track_index: Annotated[int, Field(description="Track index (0-based)", ge=0)],
        device_index: Annotated[int, Field(description="Device index (0-based)", ge=0)]
    ) -> list[float]:
        """Get all parameter maximum values for a device.

        Args:
            track_index: Track index (0-based)
            device_index: Device index on track (0-based)

        Returns:
            List of maximum values
        """
        device = Device(get_client())
        return list(device.get_parameters_maxs(track_index, device_index))

    @mcp.tool()
    def device_get_parameters_is_quantized(
        track_index: Annotated[int, Field(description="Track index (0-based)", ge=0)],
        device_index: Annotated[int, Field(description="Device index (0-based)", ge=0)]
    ) -> list[bool]:
        """Get which parameters are quantized (stepped) for a device.

        Args:
            track_index: Track index (0-based)
            device_index: Device index on track (0-based)

        Returns:
            List of booleans indicating if each parameter is quantized
        """
        device = Device(get_client())
        return list(device.get_parameters_is_quantized(track_index, device_index))
