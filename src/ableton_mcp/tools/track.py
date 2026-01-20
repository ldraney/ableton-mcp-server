"""Track tools for the Ableton MCP server.

Covers track-level operations like volume, pan, mute, solo, devices, and routing.
"""

import os
import time
from typing import Annotated

from pydantic import Field

from ableton_mcp.connection import get_client
from abletonosc_client import Track, View, Browser


def register_track_tools(mcp):
    """Register all track tools with the MCP server."""

    # =============================================================================
    # Name
    # =============================================================================

    @mcp.tool()
    def track_get_name(
        track_index: Annotated[int, Field(description="Track index (0-based)", ge=0)]
    ) -> str:
        """Get the name of a track.

        Args:
            track_index: Track index (0-based)

        Returns:
            Track name
        """
        track = Track(get_client())
        return track.get_name(track_index)

    @mcp.tool()
    def track_set_name(
        track_index: Annotated[int, Field(description="Track index (0-based)", ge=0)],
        name: Annotated[str, Field(description="New track name")]
    ) -> str:
        """Set the name of a track.

        Args:
            track_index: Track index (0-based)
            name: New track name

        Returns:
            Confirmation message
        """
        track = Track(get_client())
        track.set_name(track_index, name)
        return f"Track {track_index} renamed to '{name}'"

    # =============================================================================
    # Volume
    # =============================================================================

    @mcp.tool()
    def track_get_volume(
        track_index: Annotated[int, Field(description="Track index (0-based)", ge=0)]
    ) -> float:
        """Get the volume of a track.

        Args:
            track_index: Track index (0-based)

        Returns:
            Volume level (0.0-1.0, where 0.85 is 0dB)
        """
        track = Track(get_client())
        return track.get_volume(track_index)

    @mcp.tool()
    def track_set_volume(
        track_index: Annotated[int, Field(description="Track index (0-based)", ge=0)],
        volume: Annotated[float, Field(description="Volume level (0.0-1.0, where 0.85 is 0dB)", ge=0, le=1)]
    ) -> str:
        """Set the volume of a track.

        Args:
            track_index: Track index (0-based)
            volume: Volume level (0.0-1.0, where 0.85 is 0dB)

        Returns:
            Confirmation message
        """
        track = Track(get_client())
        track.set_volume(track_index, volume)
        return f"Track {track_index} volume set to {volume}"

    # =============================================================================
    # Panning
    # =============================================================================

    @mcp.tool()
    def track_get_panning(
        track_index: Annotated[int, Field(description="Track index (0-based)", ge=0)]
    ) -> float:
        """Get the pan position of a track.

        Args:
            track_index: Track index (0-based)

        Returns:
            Pan position (-1.0 left to 1.0 right, 0.0 center)
        """
        track = Track(get_client())
        return track.get_panning(track_index)

    @mcp.tool()
    def track_set_panning(
        track_index: Annotated[int, Field(description="Track index (0-based)", ge=0)],
        pan: Annotated[float, Field(description="Pan position (-1.0 left to 1.0 right, 0.0 center)", ge=-1, le=1)]
    ) -> str:
        """Set the pan position of a track.

        Args:
            track_index: Track index (0-based)
            pan: Pan position (-1.0 left to 1.0 right, 0.0 center)

        Returns:
            Confirmation message
        """
        track = Track(get_client())
        track.set_panning(track_index, pan)
        return f"Track {track_index} pan set to {pan}"

    # =============================================================================
    # Mute
    # =============================================================================

    @mcp.tool()
    def track_get_mute(
        track_index: Annotated[int, Field(description="Track index (0-based)", ge=0)]
    ) -> bool:
        """Check if a track is muted.

        Args:
            track_index: Track index (0-based)

        Returns:
            True if muted
        """
        track = Track(get_client())
        return track.get_mute(track_index)

    @mcp.tool()
    def track_set_mute(
        track_index: Annotated[int, Field(description="Track index (0-based)", ge=0)],
        muted: Annotated[bool, Field(description="True to mute, False to unmute")]
    ) -> str:
        """Mute or unmute a track.

        Args:
            track_index: Track index (0-based)
            muted: True to mute, False to unmute

        Returns:
            Confirmation message
        """
        track = Track(get_client())
        track.set_mute(track_index, muted)
        state = "muted" if muted else "unmuted"
        return f"Track {track_index} {state}"

    # =============================================================================
    # Solo
    # =============================================================================

    @mcp.tool()
    def track_get_solo(
        track_index: Annotated[int, Field(description="Track index (0-based)", ge=0)]
    ) -> bool:
        """Check if a track is soloed.

        Args:
            track_index: Track index (0-based)

        Returns:
            True if soloed
        """
        track = Track(get_client())
        return track.get_solo(track_index)

    @mcp.tool()
    def track_set_solo(
        track_index: Annotated[int, Field(description="Track index (0-based)", ge=0)],
        soloed: Annotated[bool, Field(description="True to solo, False to unsolo")]
    ) -> str:
        """Solo or unsolo a track.

        Args:
            track_index: Track index (0-based)
            soloed: True to solo, False to unsolo

        Returns:
            Confirmation message
        """
        track = Track(get_client())
        track.set_solo(track_index, soloed)
        state = "soloed" if soloed else "unsoloed"
        return f"Track {track_index} {state}"

    # =============================================================================
    # Arm
    # =============================================================================

    @mcp.tool()
    def track_get_arm(
        track_index: Annotated[int, Field(description="Track index (0-based)", ge=0)]
    ) -> bool:
        """Check if a track is armed for recording.

        Args:
            track_index: Track index (0-based)

        Returns:
            True if armed
        """
        track = Track(get_client())
        return track.get_arm(track_index)

    @mcp.tool()
    def track_set_arm(
        track_index: Annotated[int, Field(description="Track index (0-based)", ge=0)],
        armed: Annotated[bool, Field(description="True to arm, False to disarm")]
    ) -> str:
        """Arm or disarm a track for recording.

        Args:
            track_index: Track index (0-based)
            armed: True to arm, False to disarm

        Returns:
            Confirmation message
        """
        track = Track(get_client())
        track.set_arm(track_index, armed)
        state = "armed" if armed else "disarmed"
        return f"Track {track_index} {state}"

    # =============================================================================
    # Color
    # =============================================================================

    @mcp.tool()
    def track_get_color(
        track_index: Annotated[int, Field(description="Track index (0-based)", ge=0)]
    ) -> int:
        """Get the color of a track.

        Args:
            track_index: Track index (0-based)

        Returns:
            Color as integer
        """
        track = Track(get_client())
        return track.get_color(track_index)

    @mcp.tool()
    def track_set_color(
        track_index: Annotated[int, Field(description="Track index (0-based)", ge=0)],
        color: Annotated[int, Field(description="Color as integer")]
    ) -> str:
        """Set the color of a track.

        Args:
            track_index: Track index (0-based)
            color: Color as integer

        Returns:
            Confirmation message
        """
        track = Track(get_client())
        track.set_color(track_index, color)
        return f"Track {track_index} color set to {color}"

    @mcp.tool()
    def track_get_color_index(
        track_index: Annotated[int, Field(description="Track index (0-based)", ge=0)]
    ) -> int:
        """Get the color index of a track.

        Args:
            track_index: Track index (0-based)

        Returns:
            Color index (0-69)
        """
        track = Track(get_client())
        return track.get_color_index(track_index)

    @mcp.tool()
    def track_set_color_index(
        track_index: Annotated[int, Field(description="Track index (0-based)", ge=0)],
        color_index: Annotated[int, Field(description="Color index (0-69)", ge=0, le=69)]
    ) -> str:
        """Set the color index of a track.

        Args:
            track_index: Track index (0-based)
            color_index: Color index (0-69)

        Returns:
            Confirmation message
        """
        track = Track(get_client())
        track.set_color_index(track_index, color_index)
        return f"Track {track_index} color index set to {color_index}"

    # =============================================================================
    # Devices
    # =============================================================================

    @mcp.tool()
    def track_get_num_devices(
        track_index: Annotated[int, Field(description="Track index (0-based)", ge=0)]
    ) -> int:
        """Get the number of devices on a track.

        Args:
            track_index: Track index (0-based)

        Returns:
            Number of devices
        """
        track = Track(get_client())
        return track.get_num_devices(track_index)

    @mcp.tool()
    def track_get_device_names(
        track_index: Annotated[int, Field(description="Track index (0-based)", ge=0)]
    ) -> list[str]:
        """Get names of all devices on a track.

        Args:
            track_index: Track index (0-based)

        Returns:
            List of device names
        """
        track = Track(get_client())
        return list(track.get_device_names(track_index))

    @mcp.tool()
    def track_get_device_types(
        track_index: Annotated[int, Field(description="Track index (0-based)", ge=0)]
    ) -> list[int]:
        """Get types of all devices on a track.

        Device types: 0 = audio_effect, 1 = instrument, 2 = midi_effect

        Args:
            track_index: Track index (0-based)

        Returns:
            List of device types (integers)
        """
        track = Track(get_client())
        return list(track.get_device_types(track_index))

    @mcp.tool()
    def track_get_devices_class_names(
        track_index: Annotated[int, Field(description="Track index (0-based)", ge=0)]
    ) -> list[str]:
        """Get class names (types) of all devices on a track.

        Args:
            track_index: Track index (0-based)

        Returns:
            List of device class names (e.g., "Compressor", "Reverb")
        """
        track = Track(get_client())
        return list(track.get_devices_class_names(track_index))

    @mcp.tool()
    def track_insert_device(
        track_index: Annotated[int, Field(description="Track index (0-based)", ge=0)],
        device_name: Annotated[str, Field(description="Name of the device to load (e.g., 'Drum Rack', 'Wavetable', 'Reverb')")],
        device_index: Annotated[int, Field(description="Position to insert device (-1 = end of chain)")] = -1,
        device_type: Annotated[str, Field(description="Optional: filter to specific category - 'instrument', 'audio_effect', 'midi_effect', or 'drums'")] = None
    ) -> str:
        """Insert a device onto a track by name.

        Searches instruments, audio effects, midi effects, drums, and sounds
        for a matching device name and loads it onto the track.

        IMPORTANT: You must select the track first with view_set_selected_track
        before calling this, as devices load to the currently selected track.

        Use device_type to constrain the search to a specific category.
        This prevents issues like searching for "Pad" and getting a drum kit
        instead of a synth pad.

        Args:
            track_index: Track index (0-based)
            device_name: Name of the device to load (e.g., "Drum Rack", "Wavetable", "Reverb")
            device_index: Position to insert device (-1 = end of chain)
            device_type: Optional filter - only search this category:
                         'instrument', 'audio_effect', 'midi_effect', 'drums'

        Returns:
            Confirmation message with device index, or error if not found
        """
        view = View(get_client())
        track = Track(get_client())
        browser = Browser(get_client())

        # Critical: select track first (see TROUBLESHOOTING.md)
        view.set_selected_track(track_index)
        time.sleep(0.1)

        # If device_type specified, search only that category
        if device_type:
            valid_types = ['instrument', 'audio_effect', 'midi_effect', 'drums']
            if device_type not in valid_types:
                return f"Invalid device_type: '{device_type}'. Must be one of: {valid_types}"

            # Get items from the specified category
            if device_type == 'instrument':
                items = browser.list_instruments()
            elif device_type == 'audio_effect':
                items = browser.list_audio_effects()
            elif device_type == 'midi_effect':
                items = browser.list_midi_effects()
            elif device_type == 'drums':
                items = browser.list_drums()

            # Find fuzzy match (case-insensitive)
            query_lower = device_name.lower()
            matches = [item for item in items if query_lower in item.lower()]

            if not matches:
                return f"No {device_type} found matching '{device_name}'. Available: {items[:10]}..."

            # Load the first match using track.insert_device
            # (browser.load_item expects a full path, not a name)
            best_match = matches[0]
            result = track.insert_device(track_index, best_match, device_index)
            time.sleep(0.3)

            if result != -1:
                return f"Loaded {device_type} '{best_match}' on track {track_index} at index {result}"
            else:
                return f"Found '{best_match}' but failed to load it"

        # Default behavior: search all categories (existing behavior)
        result = track.insert_device(track_index, device_name, device_index)
        time.sleep(0.3)

        if result == -1:
            return f"Device '{device_name}' not found"
        return f"Device '{device_name}' inserted at index {result} on track {track_index}"

    @mcp.tool()
    def track_delete_device(
        track_index: Annotated[int, Field(description="Track index (0-based)", ge=0)],
        device_index: Annotated[int, Field(description="Device index to delete (0-based)", ge=0)]
    ) -> str:
        """Delete a device from a track.

        Args:
            track_index: Track index (0-based)
            device_index: Device index to delete (0-based)

        Returns:
            Confirmation message
        """
        track = Track(get_client())
        track.delete_device(track_index, device_index)
        return f"Device {device_index} deleted from track {track_index}"

    # =============================================================================
    # Sends
    # =============================================================================

    @mcp.tool()
    def track_get_send(
        track_index: Annotated[int, Field(description="Track index (0-based)", ge=0)],
        send_index: Annotated[int, Field(description="Send index (0-based)", ge=0)]
    ) -> float:
        """Get the send level for a track.

        Args:
            track_index: Track index (0-based)
            send_index: Send index (0-based, corresponds to return track order)

        Returns:
            Send level (0.0-1.0)
        """
        track = Track(get_client())
        return track.get_send(track_index, send_index)

    @mcp.tool()
    def track_set_send(
        track_index: Annotated[int, Field(description="Track index (0-based)", ge=0)],
        send_index: Annotated[int, Field(description="Send index (0-based)", ge=0)],
        level: Annotated[float, Field(description="Send level (0.0-1.0)", ge=0, le=1)]
    ) -> str:
        """Set the send level for a track.

        Args:
            track_index: Track index (0-based)
            send_index: Send index (0-based, corresponds to return track order)
            level: Send level (0.0-1.0)

        Returns:
            Confirmation message
        """
        track = Track(get_client())
        track.set_send(track_index, send_index, level)
        return f"Track {track_index} send {send_index} set to {level}"

    # =============================================================================
    # Routing
    # =============================================================================

    @mcp.tool()
    def track_get_input_routing_type(
        track_index: Annotated[int, Field(description="Track index (0-based)", ge=0)]
    ) -> str:
        """Get the input routing type for a track.

        Args:
            track_index: Track index (0-based)

        Returns:
            Input routing type name (e.g., "Ext. In", "No Input")
        """
        track = Track(get_client())
        return track.get_input_routing_type(track_index)

    @mcp.tool()
    def track_set_input_routing_type(
        track_index: Annotated[int, Field(description="Track index (0-based)", ge=0)],
        routing_type: Annotated[str, Field(description="Input routing type name")]
    ) -> str:
        """Set the input routing type for a track.

        Args:
            track_index: Track index (0-based)
            routing_type: Input routing type name

        Returns:
            Confirmation message
        """
        track = Track(get_client())
        track.set_input_routing_type(track_index, routing_type)
        return f"Track {track_index} input routing type set to '{routing_type}'"

    @mcp.tool()
    def track_get_input_routing_channel(
        track_index: Annotated[int, Field(description="Track index (0-based)", ge=0)]
    ) -> str:
        """Get the input routing channel for a track.

        Args:
            track_index: Track index (0-based)

        Returns:
            Input routing channel name
        """
        track = Track(get_client())
        return track.get_input_routing_channel(track_index)

    @mcp.tool()
    def track_set_input_routing_channel(
        track_index: Annotated[int, Field(description="Track index (0-based)", ge=0)],
        channel: Annotated[str, Field(description="Input routing channel name")]
    ) -> str:
        """Set the input routing channel for a track.

        Args:
            track_index: Track index (0-based)
            channel: Input routing channel name

        Returns:
            Confirmation message
        """
        track = Track(get_client())
        track.set_input_routing_channel(track_index, channel)
        return f"Track {track_index} input routing channel set to '{channel}'"

    @mcp.tool()
    def track_get_output_routing_type(
        track_index: Annotated[int, Field(description="Track index (0-based)", ge=0)]
    ) -> str:
        """Get the output routing type for a track.

        Args:
            track_index: Track index (0-based)

        Returns:
            Output routing type name (e.g., "Master", "Sends Only")
        """
        track = Track(get_client())
        return track.get_output_routing_type(track_index)

    @mcp.tool()
    def track_set_output_routing_type(
        track_index: Annotated[int, Field(description="Track index (0-based)", ge=0)],
        routing_type: Annotated[str, Field(description="Output routing type name")]
    ) -> str:
        """Set the output routing type for a track.

        Args:
            track_index: Track index (0-based)
            routing_type: Output routing type name

        Returns:
            Confirmation message
        """
        track = Track(get_client())
        track.set_output_routing_type(track_index, routing_type)
        return f"Track {track_index} output routing type set to '{routing_type}'"

    @mcp.tool()
    def track_get_output_routing_channel(
        track_index: Annotated[int, Field(description="Track index (0-based)", ge=0)]
    ) -> str:
        """Get the output routing channel for a track.

        Args:
            track_index: Track index (0-based)

        Returns:
            Output routing channel name
        """
        track = Track(get_client())
        return track.get_output_routing_channel(track_index)

    @mcp.tool()
    def track_set_output_routing_channel(
        track_index: Annotated[int, Field(description="Track index (0-based)", ge=0)],
        channel: Annotated[str, Field(description="Output routing channel name")]
    ) -> str:
        """Set the output routing channel for a track.

        Args:
            track_index: Track index (0-based)
            channel: Output routing channel name

        Returns:
            Confirmation message
        """
        track = Track(get_client())
        track.set_output_routing_channel(track_index, channel)
        return f"Track {track_index} output routing channel set to '{channel}'"

    @mcp.tool()
    def track_get_available_input_routing_types(
        track_index: Annotated[int, Field(description="Track index (0-based)", ge=0)]
    ) -> list[str]:
        """Get available input routing types for a track.

        Args:
            track_index: Track index (0-based)

        Returns:
            List of available input routing type names
        """
        track = Track(get_client())
        return list(track.get_available_input_routing_types(track_index))

    @mcp.tool()
    def track_get_available_output_routing_types(
        track_index: Annotated[int, Field(description="Track index (0-based)", ge=0)]
    ) -> list[str]:
        """Get available output routing types for a track.

        Args:
            track_index: Track index (0-based)

        Returns:
            List of available output routing type names
        """
        track = Track(get_client())
        return list(track.get_available_output_routing_types(track_index))

    @mcp.tool()
    def track_get_available_input_routing_channels(
        track_index: Annotated[int, Field(description="Track index (0-based)", ge=0)]
    ) -> list[str]:
        """Get available input routing channels for a track.

        Args:
            track_index: Track index (0-based)

        Returns:
            List of available input routing channel names
        """
        track = Track(get_client())
        return list(track.get_available_input_routing_channels(track_index))

    @mcp.tool()
    def track_get_available_output_routing_channels(
        track_index: Annotated[int, Field(description="Track index (0-based)", ge=0)]
    ) -> list[str]:
        """Get available output routing channels for a track.

        Args:
            track_index: Track index (0-based)

        Returns:
            List of available output routing channel names
        """
        track = Track(get_client())
        return list(track.get_available_output_routing_channels(track_index))

    # =============================================================================
    # Monitoring
    # =============================================================================

    @mcp.tool()
    def track_get_current_monitoring_state(
        track_index: Annotated[int, Field(description="Track index (0-based)", ge=0)]
    ) -> int:
        """Get the current monitoring state for a track.

        Args:
            track_index: Track index (0-based)

        Returns:
            Monitoring state (0=In, 1=Auto, 2=Off)
        """
        track = Track(get_client())
        return track.get_current_monitoring_state(track_index)

    @mcp.tool()
    def track_set_current_monitoring_state(
        track_index: Annotated[int, Field(description="Track index (0-based)", ge=0)],
        state: Annotated[int, Field(description="Monitoring state (0=In, 1=Auto, 2=Off)", ge=0, le=2)]
    ) -> str:
        """Set the current monitoring state for a track.

        Args:
            track_index: Track index (0-based)
            state: Monitoring state (0=In, 1=Auto, 2=Off)

        Returns:
            Confirmation message
        """
        track = Track(get_client())
        track.set_current_monitoring_state(track_index, state)
        state_names = ["In", "Auto", "Off"]
        return f"Track {track_index} monitoring set to {state_names[state]}"

    # =============================================================================
    # Track Info
    # =============================================================================

    @mcp.tool()
    def track_get_is_foldable(
        track_index: Annotated[int, Field(description="Track index (0-based)", ge=0)]
    ) -> bool:
        """Check if a track is a group track (foldable).

        Args:
            track_index: Track index (0-based)

        Returns:
            True if track is a group
        """
        track = Track(get_client())
        return track.get_is_foldable(track_index)

    @mcp.tool()
    def track_get_is_grouped(
        track_index: Annotated[int, Field(description="Track index (0-based)", ge=0)]
    ) -> bool:
        """Check if a track is inside a group.

        Args:
            track_index: Track index (0-based)

        Returns:
            True if track is in a group
        """
        track = Track(get_client())
        return track.get_is_grouped(track_index)

    @mcp.tool()
    def track_get_is_visible(
        track_index: Annotated[int, Field(description="Track index (0-based)", ge=0)]
    ) -> bool:
        """Check if a track is visible.

        Args:
            track_index: Track index (0-based)

        Returns:
            True if track is visible
        """
        track = Track(get_client())
        return track.get_is_visible(track_index)

    @mcp.tool()
    def track_get_can_be_armed(
        track_index: Annotated[int, Field(description="Track index (0-based)", ge=0)]
    ) -> bool:
        """Check if a track can be armed for recording.

        Args:
            track_index: Track index (0-based)

        Returns:
            True if track can be armed
        """
        track = Track(get_client())
        return track.get_can_be_armed(track_index)

    @mcp.tool()
    def track_get_has_midi_input(
        track_index: Annotated[int, Field(description="Track index (0-based)", ge=0)]
    ) -> bool:
        """Check if a track has MIDI input.

        Args:
            track_index: Track index (0-based)

        Returns:
            True if track has MIDI input
        """
        track = Track(get_client())
        return track.get_has_midi_input(track_index)

    @mcp.tool()
    def track_get_has_midi_output(
        track_index: Annotated[int, Field(description="Track index (0-based)", ge=0)]
    ) -> bool:
        """Check if a track has MIDI output.

        Args:
            track_index: Track index (0-based)

        Returns:
            True if track has MIDI output
        """
        track = Track(get_client())
        return track.get_has_midi_output(track_index)

    @mcp.tool()
    def track_get_has_audio_input(
        track_index: Annotated[int, Field(description="Track index (0-based)", ge=0)]
    ) -> bool:
        """Check if a track has audio input.

        Args:
            track_index: Track index (0-based)

        Returns:
            True if track has audio input
        """
        track = Track(get_client())
        return track.get_has_audio_input(track_index)

    @mcp.tool()
    def track_get_has_audio_output(
        track_index: Annotated[int, Field(description="Track index (0-based)", ge=0)]
    ) -> bool:
        """Check if a track has audio output.

        Args:
            track_index: Track index (0-based)

        Returns:
            True if track has audio output
        """
        track = Track(get_client())
        return track.get_has_audio_output(track_index)

    # =============================================================================
    # Group Tracks
    # =============================================================================

    @mcp.tool()
    def track_get_fold_state(
        track_index: Annotated[int, Field(description="Track index (0-based)", ge=0)]
    ) -> bool:
        """Get the fold state of a group track.

        Args:
            track_index: Track index (0-based)

        Returns:
            True if track is folded (collapsed)
        """
        track = Track(get_client())
        return track.get_fold_state(track_index)

    @mcp.tool()
    def track_set_fold_state(
        track_index: Annotated[int, Field(description="Track index (0-based)", ge=0)],
        folded: Annotated[bool, Field(description="True to fold (collapse) the group")]
    ) -> str:
        """Set the fold state of a group track.

        Args:
            track_index: Track index (0-based)
            folded: True to fold (collapse) the group

        Returns:
            Confirmation message
        """
        track = Track(get_client())
        track.set_fold_state(track_index, folded)
        state = "folded" if folded else "unfolded"
        return f"Track {track_index} {state}"

    # =============================================================================
    # Slot State
    # =============================================================================

    @mcp.tool()
    def track_get_fired_slot_index(
        track_index: Annotated[int, Field(description="Track index (0-based)", ge=0)]
    ) -> int:
        """Get the index of the clip slot that was fired (triggered).

        Args:
            track_index: Track index (0-based)

        Returns:
            Fired slot index, or -1 if none
        """
        track = Track(get_client())
        return track.get_fired_slot_index(track_index)

    @mcp.tool()
    def track_get_playing_slot_index(
        track_index: Annotated[int, Field(description="Track index (0-based)", ge=0)]
    ) -> int:
        """Get the index of the currently playing clip slot.

        Args:
            track_index: Track index (0-based)

        Returns:
            Playing slot index, or -1 if none
        """
        track = Track(get_client())
        return track.get_playing_slot_index(track_index)

    # =============================================================================
    # Meters
    # =============================================================================

    @mcp.tool()
    def track_get_output_meter_level(
        track_index: Annotated[int, Field(description="Track index (0-based)", ge=0)]
    ) -> float:
        """Get the output meter level for a track.

        Args:
            track_index: Track index (0-based)

        Returns:
            Output meter level (0.0-1.0)
        """
        track = Track(get_client())
        return track.get_output_meter_level(track_index)

    @mcp.tool()
    def track_get_output_meter_left(
        track_index: Annotated[int, Field(description="Track index (0-based)", ge=0)]
    ) -> float:
        """Get the left channel output meter level for a track.

        Args:
            track_index: Track index (0-based)

        Returns:
            Left channel meter level (0.0-1.0)
        """
        track = Track(get_client())
        return track.get_output_meter_left(track_index)

    @mcp.tool()
    def track_get_output_meter_right(
        track_index: Annotated[int, Field(description="Track index (0-based)", ge=0)]
    ) -> float:
        """Get the right channel output meter level for a track.

        Args:
            track_index: Track index (0-based)

        Returns:
            Right channel meter level (0.0-1.0)
        """
        track = Track(get_client())
        return track.get_output_meter_right(track_index)

    # =============================================================================
    # Clip Control
    # =============================================================================

    @mcp.tool()
    def track_stop_all_clips(
        track_index: Annotated[int, Field(description="Track index (0-based)", ge=0)]
    ) -> str:
        """Stop all playing clips on this track.

        Args:
            track_index: Track index (0-based)

        Returns:
            Confirmation message
        """
        track = Track(get_client())
        track.stop_all_clips(track_index)
        return f"All clips stopped on track {track_index}"

    # =============================================================================
    # Bulk Clip Queries
    # =============================================================================

    @mcp.tool()
    def track_get_clips_names(
        track_index: Annotated[int, Field(description="Track index (0-based)", ge=0)]
    ) -> list[str]:
        """Get names of all clips on a track.

        Args:
            track_index: Track index (0-based)

        Returns:
            List of clip names (empty string for empty slots)
        """
        track = Track(get_client())
        return list(track.get_clips_names(track_index))

    @mcp.tool()
    def track_get_clips_lengths(
        track_index: Annotated[int, Field(description="Track index (0-based)", ge=0)]
    ) -> list[float]:
        """Get lengths of all clips on a track.

        Args:
            track_index: Track index (0-based)

        Returns:
            List of clip lengths in beats (0 for empty slots)
        """
        track = Track(get_client())
        return list(track.get_clips_lengths(track_index))

    @mcp.tool()
    def track_get_clips_colors(
        track_index: Annotated[int, Field(description="Track index (0-based)", ge=0)]
    ) -> list[int]:
        """Get colors of all clips on a track.

        Args:
            track_index: Track index (0-based)

        Returns:
            List of clip colors as integers
        """
        track = Track(get_client())
        return list(track.get_clips_colors(track_index))

    # =============================================================================
    # Pack-Filtered Device Loading
    # =============================================================================

    @mcp.tool()
    def track_insert_device_from_pack(
        track_index: Annotated[int, Field(description="Track index (0-based)", ge=0)],
        device_name: Annotated[str, Field(description="Name to search for (fuzzy match)")],
        pack_name: Annotated[str, Field(description="Pack to search in (fuzzy match on pack name)")],
        device_index: Annotated[int, Field(description="Position in device chain (-1 = end)")] = -1
    ) -> str:
        """Load a device from a specific pack only.

        Uses filesystem scan to find .adg files in the pack,
        then loads the matching device. This is useful for loading
        presets from specific packs like "Electric Keyboards" or
        "Golden Era Hip-Hop Drums".

        Args:
            track_index: Track index (0-based)
            device_name: Name to search for (fuzzy match, case-insensitive)
            pack_name: Pack to search in (fuzzy match on pack name)
            device_index: Position in device chain (-1 = end)

        Returns:
            Confirmation message with loaded device, or error if not found
        """
        view = View(get_client())
        browser = Browser(get_client())

        # Critical: select track first (see TROUBLESHOOTING.md)
        view.set_selected_track(track_index)
        time.sleep(0.1)

        # Scan packs from disk
        pack_root = os.path.expanduser("~/Music/Ableton/Factory Packs")
        if not os.path.isdir(pack_root):
            return f"Pack directory not found: {pack_root}"

        # Find matching pack
        matching_pack = None
        pack_name_lower = pack_name.lower()
        for pack in os.listdir(pack_root):
            pack_path = os.path.join(pack_root, pack)
            if os.path.isdir(pack_path) and pack_name_lower in pack.lower():
                matching_pack = pack
                break

        if not matching_pack:
            available_packs = [p for p in os.listdir(pack_root)
                              if os.path.isdir(os.path.join(pack_root, p))]
            return f"Pack not found: '{pack_name}'. Available packs: {available_packs}"

        # Find .adg files in pack
        pack_path = os.path.join(pack_root, matching_pack)
        device_name_lower = device_name.lower()
        matches = []

        for root, dirs, files in os.walk(pack_path):
            for f in files:
                if f.endswith('.adg') and device_name_lower in f.lower():
                    rel_path = os.path.relpath(os.path.join(root, f), pack_path)
                    matches.append((f, rel_path))

        if not matches:
            # List available .adg files to help user
            all_adg = []
            for root, dirs, files in os.walk(pack_path):
                for f in files:
                    if f.endswith('.adg'):
                        all_adg.append(f)
            return (f"No device matching '{device_name}' in pack '{matching_pack}'. "
                    f"Available devices: {all_adg[:15]}...")

        # Load the first match
        best_match_name, best_match_path = matches[0]
        full_path = f"{matching_pack}/{best_match_path}"

        # Try to load via browser
        success = browser.load_item(best_match_name[:-4])  # Try without .adg extension
        if not success:
            success = browser.load_item(best_match_name)  # Try with extension
        if not success:
            success = browser.load_item(full_path)  # Try full path

        time.sleep(0.3)

        if success:
            return f"Loaded '{best_match_name}' from pack '{matching_pack}' on track {track_index}"
        else:
            # Even if browser.load_item reports failure, the device might have loaded
            # Check if there are any devices on the track now
            track_obj = Track(get_client())
            device_names = list(track_obj.get_device_names(track_index))
            if device_names:
                return (f"Attempted to load '{best_match_name}' from '{matching_pack}'. "
                        f"Track {track_index} now has devices: {device_names}")
            return (f"Found '{best_match_name}' in '{matching_pack}' but failed to load. "
                    f"Try using track_insert_device with the exact name.")
