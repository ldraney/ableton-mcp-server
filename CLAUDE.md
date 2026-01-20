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

## Design Philosophy: Pure 1:1 Wrapper

This MCP server is a **pure wrapper** over AbletonOSC. Each tool is a direct pass-through to an OSC endpoint with no additional logic.

### What This Means for Agents

1. **No Timing Logic**: Tools return immediately. Agents must:
   - Add `time.sleep()` after operations that need settling time
   - Delete tracks backwards to avoid index shifts
   - Select track before loading devices

2. **No Composite Operations**: Tools do one thing. Multi-step workflows should be implemented by agents.

3. **No Filesystem Operations**: The MCP only communicates via OSC. Workarounds for broken APIs (like `browser.packs`) should be implemented by agents.

## Tool Organization

Tools are organized by domain, matching the OSC client structure:

### Song Tools
- `song_get_tempo` / `song_set_tempo` - BPM control
- `song_play` / `song_stop` - Transport
- `song_get_time_signature` / `song_set_time_signature`
- `song_get_num_tracks` / `song_get_num_scenes`
- `song_delete_track` - Delete a single track (agents handle sequencing)

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
- `track_insert_device` - Load device by name (fuzzy search via OSC)
- `device_get_parameters`
- `device_set_parameter`
- `device_enable` / `device_disable`

### Browser Tools
**Working (via OSC):**
- `browser_list_instruments` - List top-level instruments (Analog, Wavetable, etc.)
- `browser_list_audio_effects` - List top-level audio effects (Reverb, Compressor, etc.)
- `browser_list_midi_effects` - List top-level MIDI effects (Arpeggiator, Scale, etc.)
- `browser_list_drums` - List all drum kits (.adg files)
- `browser_list_sounds` - List sound categories
- `browser_search_by_type` - Search devices by category
- `browser_load_item` - Load a browser item by path

**Limited/Not Working (OSC API issues):**
- `browser_list_packs` - Returns empty (browser.packs API issue)
- `browser_search` - Times out (recursive search too slow)
- `browser_search_and_load` - Times out
- `browser_list_pack_contents` - Times out

**Removed (filesystem operations belong in agents):**
- ~~`browser_scan_packs_from_disk`~~ - Agents should scan `~/Music/Ableton/Factory Packs/` directly
- ~~`browser_search_in_packs`~~ - Agents should implement pack search
- ~~`browser_generate_local_cache`~~ - Agents should generate their own caches

### View Tools
- `view_select_track` / `view_select_scene`

## Device Discovery

### How Device Search Works
`track_insert_device` searches through standard browser locations via OSC:
- `browser.instruments`, `browser.audio_effects`, `browser.midi_effects`, `browser.drums`, `browser.sounds`

**Match logic** (fuzzy, case-insensitive): `query in item.name.lower()`

### Recommended Workflow

1. **Discover available devices**:
   ```python
   browser_list_drums()      # → ["808 Core Kit.adg", "Golden Era Kit.adg", ...]
   browser_list_instruments() # → ["Analog", "Wavetable", "Operator", ...]
   browser_list_audio_effects() # → ["Reverb", "Compressor", ...]
   ```

2. **Load devices** (fuzzy match):
   ```python
   track_insert_device(0, "Golden Era")  # Loads "Golden Era Kit"
   track_insert_device(0, "808 Core")    # Loads "808 Core Kit"
   track_insert_device(0, "Wavetable")   # Loads Wavetable synth
   ```

3. **Verify**:
   ```python
   track_get_device_names(0)  # Confirm device loaded
   ```

### Pack Discovery (Agent Responsibility)

Since `browser.packs` API doesn't work via OSC, agents that need pack discovery should scan the filesystem directly:

```
~/Music/Ableton/Factory Packs/
├── Chop and Swing/
├── Electric Keyboards/
│   └── Sounds/
│       ├── Suitcase Piano/
│       │   ├── Basic Suitcase Amp.adg
│       │   └── ...
├── Golden Era Hip-Hop Drums by Sound Oracle/
│   └── Drums/
│       ├── Golden Era Kit.adg
│       └── ...
└── ...
```

This is intentionally **not** in the MCP server - it's agent orchestration logic.

### Verified Working Devices
```
Drum Kits (.adg files):
- "Golden Era" → Golden Era Kit
- "808 Core" → 808 Core Kit
- "909 Core" → 909 Core Kit
- "707 Core" → 707 Core Kit

Stock Instruments:
- "Wavetable", "Analog", "Operator", "Drift", "Meld"

Stock Effects:
- "Reverb", "Compressor", "EQ Eight", "Delay", "Echo"
```

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
│       │   ├── clip_slot.py
│       │   ├── scene.py
│       │   ├── device.py
│       │   ├── view.py
│       │   ├── application.py
│       │   ├── midimap.py
│       │   └── browser.py     # Device browsing (OSC only)
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

**This project uses Poetry for dependency management.**

```bash
# Install dependencies
poetry install

# Install OSC client dependency (local development)
poetry add --editable ../ableton-music-development

# Run server directly for testing
poetry run python -m ableton_mcp

# Run tests
poetry run pytest

# Check Python syntax
poetry run python -m py_compile src/ableton_mcp/tools/track.py

# General rule: prefix all Python commands with `poetry run`
```

## Troubleshooting

See `docs/TROUBLESHOOTING.md` for:
- Common errors and fixes
- Agent responsibilities (timing, sequencing)
- Working song template
- QA checklist

## Related Projects
- `ldraney/ableton-music-development` - OSC client wrapper (Phase 1)
- `ldraney/AbletonOSC` - Fork with device insertion (PR #173 to upstream)
- `ideoforms/AbletonOSC` - Upstream Ableton MIDI Remote Script
- `ldraney/ableton-manual` - RAG for Ableton documentation
