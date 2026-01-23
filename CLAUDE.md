# Ableton MCP Server

## Getting Started

### Quick Start (New Users)

1. **Install dependencies:**
   ```bash
   poetry install
   ```

2. **Start Ableton Live 12** with AbletonOSC enabled (Preferences → Link/Tempo/MIDI → Control Surface = AbletonOSC)

3. **That's it!** Now just ask me what you want to create. Examples:
   - "Create a lo-fi beat with drums, bass, and keys"
   - "Make a simple 4-bar loop with a kick on 1 and 3"
   - "Load a piano and play a C major chord"

### Song Development Workflow

There are two ways to create music:

**1. Conversational (Interactive)**
Just describe what you want and I'll build it in real-time:
```
You: "Create a chill lo-fi track at 85 BPM"
Me: [Creates tracks, loads instruments, programs notes, plays it]
You: "Add some reverb to the keys"
Me: [Adds reverb, adjusts parameters]
You: "Export it to MP3"
Me: [Records and exports to file]
```

**2. JSON Schema (Reproducible)**
Define songs as JSON files using `song-schema` (included as dependency):
```bash
# Execute a song definition
song_execute("path/to/song.json")

# Preview timing without executing
song_execute_info("path/to/song.json")
```

See `song-schema` examples at: https://github.com/ldraney/song-schema/tree/main/examples

### Export Workflow (Important!)

To export your creation to MP3/WAV:

1. **Warm up instruments** - Fire the scene, let it play 3-4 seconds
2. **Stop playback** - `song_stop()`
3. **Export** - `song_export_audio("/path/to/output.mp3", duration_seconds=30)`

Prerequisites:
- FFmpeg installed (`brew install ffmpeg` on macOS)
- Audio loopback device (BlackHole on macOS, VB-Cable on Windows)

---

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
- `song_clear_all_tracks` - Delete all tracks (backwards, with delays)

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
- `track_insert_device` - Load device by name (enhanced with recursive pack search)
- `device_get_parameters`
- `device_set_parameter`
- `device_enable` / `device_disable`

### Browser Tools
**Working:**
- `browser_list_instruments` - List top-level instruments (Analog, Wavetable, etc.)
- `browser_list_audio_effects` - List top-level audio effects (Reverb, Compressor, etc.)
- `browser_list_midi_effects` - List top-level MIDI effects (Arpeggiator, Scale, etc.)
- `browser_list_drums` - List all drum kits (.adg files) - **346 kits!**
- `browser_list_sounds` - List sound categories
- `browser_scan_packs_from_disk` - Scan filesystem for installed packs and .adg files
- `browser_generate_local_cache` - Generate JSON cache of all browser items + packs from disk

**Limited/Not Working:**
- `browser_list_packs` - Returns empty (browser.packs API issue)
- `browser_search` - Times out (recursive search too slow)
- `browser_search_and_load` - Times out
- `browser_list_pack_contents` - Times out
- `browser_load_item` - Use `track_insert_device` instead

### View Tools
- `view_select_track` / `view_select_scene`

### Export Tools
- `song_export_audio` - Export song to MP3/WAV by recording Ableton's audio output via FFmpeg
- `song_get_duration_seconds` - Calculate song duration in seconds from beats and tempo
- `export_list_audio_devices` - List available audio capture devices
- `export_test_audio_capture` - Test audio capture without Ableton playback

**Prerequisites for export:**
- FFmpeg installed (`sudo apt install ffmpeg` on Linux)
- Audio loopback device available:
  - Linux: PulseAudio monitor (default with WSLg) or ALSA loopback
  - Windows: Stereo Mix enabled, or VB-Cable virtual audio device
  - macOS: BlackHole or similar virtual audio device

### Executor Tools
- `song_execute` - Execute a song-schema JSON file with proper timing and optional recording
- `song_execute_info` - Preview song structure and timing without executing

**Usage:**
```python
# Execute and record to arrangement view
song_execute("~/song-schema/examples/deep-sine-track.json", record=True)

# Dry run - just see timing info
song_execute("~/song-schema/examples/deep-sine-track.json", dry_run=True)

# Or use the info-only tool
song_execute_info("~/song-schema/examples/deep-sine-track.json")
```

## Device Discovery

### Pack Locations on Disk

Since `browser.packs` API doesn't work, packs are scanned from the filesystem:

```
~/Music/Ableton/Factory Packs/
├── Chop and Swing/
├── Convolution Reverb/
├── Drum Essentials/
├── Electric Keyboards/
│   └── Sounds/
│       ├── Suitcase Piano/
│       │   ├── Basic Suitcase Amp.adg
│       │   ├── Basic Suitcase DI.adg
│       │   └── ...
│       ├── Tonewheel Organ/
│       └── Wurly Piano/
├── Golden Era Hip-Hop Drums by Sound Oracle/
│   └── Drums/
│       ├── Golden Era Kit.adg
│       ├── Black Squid Kit.adg
│       └── ...
├── Grand Piano/
├── Retro Synths/
└── ...
```

### Recommended Workflow

1. **Generate local cache** (one-time):
   ```
   browser_generate_local_cache()
   ```
   Creates `local_browser_cache.json` with all 346+ drum kits, instruments, effects, AND all packs from disk.

2. **Discover available devices**:
   ```python
   browser_list_drums()      # → ["808 Core Kit.adg", "Golden Era Kit.adg", ...]
   browser_list_instruments() # → ["Analog", "Wavetable", "Operator", ...]
   browser_list_audio_effects() # → ["Reverb", "Compressor", ...]
   ```

3. **Load devices** (fuzzy match):
   ```python
   track_insert_device(0, "Golden Era")  # Loads "Golden Era Kit"
   track_insert_device(0, "808 Core")    # Loads "808 Core Kit"
   track_insert_device(0, "Wavetable")   # Loads Wavetable synth
   ```

4. **Verify**:
   ```python
   track_get_device_names(0)  # Confirm device loaded
   ```

### How Device Search Works
`track_insert_device` searches through standard browser locations:
- `browser.instruments`, `browser.audio_effects`, `browser.midi_effects`, `browser.drums`, `browser.sounds`

**Match logic** (fuzzy, case-insensitive): `query in item.name.lower()`

### Verified Working Devices
```
Drum Kits (.adg files):
- "Golden Era" → Golden Era Kit
- "808 Core" → 808 Core Kit
- "909 Core" → 909 Core Kit
- "707 Core" → 707 Core Kit

Pack Presets (.adg files):
- "Suitcase" → Basic Suitcase Amp (Electric Keyboards pack)
- "Wurly" → Wurly Piano presets
- "Tonewheel" → Tonewheel Organ presets

Stock Instruments:
- "Wavetable", "Analog", "Operator", "Drift", "Meld"

Stock Effects:
- "Reverb", "Compressor", "EQ Eight", "Delay", "Echo"
```

### Local Browser Cache
The `browser_generate_local_cache()` tool creates a JSON file with:
- All 346 drum kits (.adg files)
- 23 instruments
- 66 audio effects
- 16 MIDI effects
- 20 sound categories
- All packs from disk with their .adg presets (from `~/Music/Ableton/Factory Packs/`)

This file is auto-generated and added to `.gitignore` (local configuration).

### Discovering Pack Contents
Use `browser_scan_packs_from_disk()` to enumerate all installed packs:
```python
browser_scan_packs_from_disk()
# Returns: {
#   "Electric Keyboards": ["Sounds/Suitcase Piano/Basic Suitcase Amp.adg", ...],
#   "Golden Era Hip-Hop Drums": ["Drums/Golden Era Kit.adg", ...],
#   ...
# }
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
│       │   └── browser.py     # NEW: Pack exploration and device discovery
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
- Critical patterns (delete backwards, sleep between ops)
- Working song template
- QA checklist

## Related Projects
- `ldraney/ableton-music-development` - OSC client wrapper (Phase 1)
- `ldraney/AbletonOSC` - Fork with device insertion (PR #173 to upstream)
- `ideoforms/AbletonOSC` - Upstream Ableton MIDI Remote Script
- `ldraney/ableton-manual` - RAG for Ableton documentation
