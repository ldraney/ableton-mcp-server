"""MIDI mapping tools for the Ableton MCP server.

Covers MIDI mapping operations for controlling Live parameters via MIDI CC.
"""

from typing import Annotated

from pydantic import Field

from ableton_mcp.connection import get_client
from abletonosc_client import MidiMap


def register_midimap_tools(mcp):
    """Register all MIDI mapping tools with the MCP server."""

    @mcp.tool()
    def midimap_map_cc(
        track_index: Annotated[int, Field(description="Track index (0-based)", ge=0)],
        device_index: Annotated[int, Field(description="Device index on track (0-based)", ge=0)],
        parameter_index: Annotated[int, Field(description="Parameter index within device (0-based)", ge=0)],
        midi_channel: Annotated[int, Field(description="MIDI channel (0-15)", ge=0, le=15)],
        cc_number: Annotated[int, Field(description="MIDI CC number (0-127)", ge=0, le=127)]
    ) -> str:
        """Map a MIDI CC to a device parameter.

        Creates a MIDI mapping so that sending CC messages will control
        the specified device parameter.

        Args:
            track_index: Track index (0-based)
            device_index: Device index on track (0-based)
            parameter_index: Parameter index within device (0-based)
            midi_channel: MIDI channel (0-15)
            cc_number: MIDI CC number (0-127)

        Returns:
            Confirmation message
        """
        midimap = MidiMap(get_client())
        midimap.map_cc(track_index, device_index, parameter_index, midi_channel, cc_number)
        return f"CC {cc_number} on channel {midi_channel} mapped to parameter {parameter_index} on device {device_index} (track {track_index})"
