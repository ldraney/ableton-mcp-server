# Ableton MCP Server

**Control Ableton Live with AI through natural conversation.**

An MCP (Model Context Protocol) server that exposes 260+ tools for controlling Ableton Live from Claude Code. Create tracks, manipulate MIDI, load instruments, and produce music—all through natural language.

## Quick Start

```bash
# 1. Clone and install
git clone https://github.com/ldraney/ableton-mcp.git
cd ableton-mcp
poetry install

# 2. Start Ableton Live 12 with AbletonOSC enabled

# 3. Start Claude Code in this directory
claude

# 4. Just ask for what you want!
```

**That's it.** Claude reads the project documentation and knows how to guide you through creating music. Try:
- "Create a lo-fi beat"
- "Make a simple drum pattern"
- "Help me set up audio export"

## Why This Exists

Traditional DAW workflows require clicking through menus and dialogs. This project lets you describe what you want in plain English:

> "Create a MIDI track, load a drum kit, and add a four-on-the-floor kick pattern at 120 BPM"

Claude Code executes the sequence of operations in Ableton while you watch it happen in real-time.

## Features

### Comprehensive Control
- **80+ Song Tools** - Transport, tempo, time signature, loop regions, cue points, recording
- **70+ Track Tools** - Volume, pan, mute/solo, routing, sends, device management
- **50+ Clip Tools** - MIDI note manipulation, audio warping, launch modes, loop settings
- **40+ Device Tools** - Parameter control, enable/disable, MIDI mapping
- **20+ Browser Tools** - Search instruments, load presets, explore packs

### Key Capabilities
- Full transport control (play, stop, record, loop)
- Create and delete MIDI/audio tracks
- Add, edit, and remove MIDI notes programmatically
- Load any Ableton instrument, effect, or preset by name
- Control device parameters in real-time
- Navigate session view (select tracks, scenes, clips)
- Query song state (tempo, time signature, track counts)

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                     Claude Code                         │
│              (or any MCP-compatible client)             │
└───────────────────────┬─────────────────────────────────┘
                        │ MCP Protocol (stdio)
                        ▼
┌─────────────────────────────────────────────────────────┐
│              ableton-mcp (this project)          │
│                   FastMCP + Python                      │
└───────────────────────┬─────────────────────────────────┘
                        │ Python imports
                        ▼
┌─────────────────────────────────────────────────────────┐
│                  abletonosc-client                      │
│         github.com/ldraney/abletonosc-client    │
└───────────────────────┬─────────────────────────────────┘
                        │ UDP (ports 11000/11001)
                        ▼
┌─────────────────────────────────────────────────────────┐
│                      AbletonOSC                         │
│            MIDI Remote Script in Ableton Live           │
└───────────────────────┬─────────────────────────────────┘
                        │ Live Object Model
                        ▼
┌─────────────────────────────────────────────────────────┐
│                    Ableton Live 12                      │
└─────────────────────────────────────────────────────────┘
```

## Quick Example

Once configured, you can have conversations like:

**You:** Create a simple beat
**Claude:** *Creates MIDI track → Loads 808 Core Kit → Adds kick on 1 and 3, snare on 2 and 4 → Sets tempo to 90 BPM → Hits play*

Behind the scenes, Claude calls tools like:
```python
song_set_tempo(bpm=90)
song_create_midi_track(index=0)
track_set_name(track_index=0, name="Drums")
track_insert_device(track_index=0, device_name="808 Core Kit")
clip_slot_create_clip(track_index=0, scene_index=0, length=4)
clip_add_notes(track_index=0, clip_index=0, notes=[
    {"pitch": 36, "start_time": 0, "duration": 0.5, "velocity": 100},  # Kick
    {"pitch": 38, "start_time": 1, "duration": 0.5, "velocity": 100},  # Snare
    {"pitch": 36, "start_time": 2, "duration": 0.5, "velocity": 100},  # Kick
    {"pitch": 38, "start_time": 3, "duration": 0.5, "velocity": 100},  # Snare
])
clip_fire(track_index=0, clip_index=0)
```

## Prerequisites

- **Python 3.11+**
- **Ableton Live 12** with [AbletonOSC](https://github.com/ideoforms/AbletonOSC) installed and enabled
- **Claude Code** (or any MCP-compatible client)

## Installation

```bash
# Clone the repository
git clone https://github.com/ldraney/ableton-mcp.git
cd ableton-mcp

# Install with Poetry
poetry install
```

## Configuration

Add to your Claude Code MCP settings (`~/.claude/settings.json` or project `.mcp.json`):

```json
{
  "mcpServers": {
    "ableton": {
      "command": "poetry",
      "args": ["run", "ableton-mcp"],
      "cwd": "/path/to/ableton-mcp"
    }
  }
}
```

### WSL2 Support

The server auto-detects WSL2 environments and configures the correct Windows host IP. No manual configuration needed.

## Documentation

- **[CLAUDE.md](./CLAUDE.md)** - Full tool reference, device discovery, and implementation details
- **[docs/TROUBLESHOOTING.md](./docs/TROUBLESHOOTING.md)** - Common issues and solutions

## Related Projects

| Project | Description |
|---------|-------------|
| [song-schema](https://github.com/ldraney/song-schema) | Define songs as JSON, execute them in Ableton (included as dependency) |
| [abletonosc-client](https://github.com/ldraney/abletonosc-client) | Python OSC client wrapper for Ableton |
| [AbletonOSC](https://github.com/ideoforms/AbletonOSC) | The MIDI Remote Script that makes this possible |

## Development

```bash
# Run tests
poetry run pytest

# Run the server directly (for debugging)
poetry run ableton-mcp

# Check Python syntax
poetry run python -m py_compile src/ableton_mcp/server.py
```

## License

MIT
