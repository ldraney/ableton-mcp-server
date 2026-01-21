"""Tool modules for the Ableton MCP server.

Tools are organized by domain:
- song: Song-level operations (tempo, transport, scenes, loop, quantization, etc.)
- track: Track operations (volume, pan, mute, solo, devices, routing, etc.)
- clip: Clip operations (notes, properties, launch, loop, audio settings, etc.)
- clip_slot: Clip slot operations (create, delete, fire, stop, duplicate)
- scene: Scene operations (fire, name, color, tempo, time signature)
- device: Device operations (parameters, activation, bulk operations)
- view: View operations (selection, navigation, visibility)
- application: Application operations (version, testing, messaging)
- midimap: MIDI mapping operations (CC mapping)
- browser: Browser operations (pack exploration, search, device loading)
- export: Audio export operations (record to MP3/WAV via FFmpeg)
- executor: Song-schema execution (play songs with timing, record to arrangement)
"""

from ableton_mcp.tools.song import register_song_tools
from ableton_mcp.tools.executor import register_executor_tools
from ableton_mcp.tools.track import register_track_tools
from ableton_mcp.tools.clip import register_clip_tools
from ableton_mcp.tools.clip_slot import register_clip_slot_tools
from ableton_mcp.tools.scene import register_scene_tools
from ableton_mcp.tools.device import register_device_tools
from ableton_mcp.tools.view import register_view_tools
from ableton_mcp.tools.application import register_application_tools
from ableton_mcp.tools.midimap import register_midimap_tools
from ableton_mcp.tools.browser import register_browser_tools
from ableton_mcp.tools.export import register_export_tools


def register_all_tools(mcp):
    """Register all tools with the MCP server.

    Args:
        mcp: FastMCP server instance
    """
    register_song_tools(mcp)
    register_track_tools(mcp)
    register_clip_tools(mcp)
    register_clip_slot_tools(mcp)
    register_scene_tools(mcp)
    register_device_tools(mcp)
    register_view_tools(mcp)
    register_application_tools(mcp)
    register_midimap_tools(mcp)
    register_browser_tools(mcp)
    register_export_tools(mcp)
    register_executor_tools(mcp)


__all__ = [
    "register_all_tools",
    "register_song_tools",
    "register_track_tools",
    "register_clip_tools",
    "register_clip_slot_tools",
    "register_scene_tools",
    "register_device_tools",
    "register_view_tools",
    "register_application_tools",
    "register_midimap_tools",
    "register_browser_tools",
    "register_export_tools",
    "register_executor_tools",
]
