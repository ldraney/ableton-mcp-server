# Ableton MCP Server

## Vision
MCP server that exposes Ableton Live control to Claude Code. Users interact with Ableton through natural conversation while watching changes happen in real-time.

## Architecture

```
Claude Code
    ↓ MCP protocol (stdio)
ableton-mcp-server (this project)
    ↓ Python imports
ableton-osc-client (pip install from ../ableton-music-development)
    ↓ UDP ports 11000/11001
AbletonOSC (MIDI Remote Script in Ableton)
    ↓ Live Object Model
Ableton Live
```

## Prerequisites
- Ableton Live 12 with AbletonOSC installed and enabled
- The `ableton-osc-client` package from `ldraney/ableton-music-development`

## Tool Organization

Tools are organized by domain, matching the OSC client structure:

### Song Tools
- `song_get_tempo` / `song_set_tempo` - BPM control
- `song_play` / `song_stop` - Transport
- `song_get_time_signature` / `song_set_time_signature`
- `song_get_num_tracks` / `song_get_num_scenes`

### Track Tools
- `track_get_volume` / `track_set_volume`
- `track_get_pan` / `track_set_pan`
- `track_mute` / `track_unmute` / `track_solo` / `track_unsolo`
- `track_get_name` / `track_set_name`

### Clip Tools
- `clip_fire` / `clip_stop`
- `clip_get_notes` / `clip_add_notes` / `clip_remove_notes`
- `clip_get_name` / `clip_set_name`

### Clip Slot Tools
- `clip_slot_create_clip` / `clip_slot_delete_clip`
- `clip_slot_has_clip`

### Scene Tools
- `scene_fire`
- `scene_get_name` / `scene_set_name`

### Device Tools
- `device_get_parameters`
- `device_set_parameter`
- `device_enable` / `device_disable`

### View Tools
- `view_select_track` / `view_select_scene`

## Project Structure

```
ableton-mcp-server/
├── pyproject.toml
├── src/
│   └── ableton_mcp/
│       ├── __init__.py
│       ├── server.py          # MCP server entry point
│       ├── tools/
│       │   ├── __init__.py
│       │   ├── song.py
│       │   ├── track.py
│       │   ├── clip.py
│       │   ├── scene.py
│       │   ├── device.py
│       │   └── view.py
│       └── connection.py      # OSC client singleton
└── tests/
    └── ...
```

## Implementation Notes

### Connection Management
- Single OSC client instance shared across all tools
- Lazy connection on first tool call
- Handle connection errors gracefully with clear messages

### Tool Design
- Each tool should be self-contained and atomic
- Return structured data that Claude can understand
- Include helpful error messages for common issues (e.g., "track index out of range")

### Testing Strategy
- Unit tests can mock the OSC client
- Integration tests require Ableton running (like osc_client tests)

## MCP Server Setup

The server runs via stdio, configured in Claude Code's MCP settings:

```json
{
  "mcpServers": {
    "ableton": {
      "command": "python",
      "args": ["-m", "ableton_mcp"],
      "cwd": "/path/to/ableton-mcp-server"
    }
  }
}
```

## Development

```bash
# Install with OSC client dependency
pip install -e ".[dev]"
pip install -e ../ableton-music-development

# Run server directly for testing
python -m ableton_mcp

# Run tests
pytest
```

## Troubleshooting

See `docs/TROUBLESHOOTING.md` for:
- Common errors and fixes
- Critical patterns (delete backwards, sleep between ops)
- Working song template
- QA checklist

## Related Projects
- `ldraney/ableton-music-development` - OSC client wrapper (Phase 1)
- `ldraney/AbletonOSC` - Fork with device insertion (PR #173 to upstream)
- `ideoforms/AbletonOSC` - Upstream Ableton MIDI Remote Script
- `ldraney/ableton-manual` - RAG for Ableton documentation
