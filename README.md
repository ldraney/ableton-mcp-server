# Ableton MCP Server

MCP server for controlling Ableton Live via Claude Code.

## Prerequisites

- Python 3.11+
- Ableton Live with [AbletonOSC](https://github.com/ideoforms/AbletonOSC) installed
- Claude Code with MCP support

## Installation

```bash
# Clone and install
git clone https://github.com/ldraney/ableton-mcp-server.git
cd ableton-mcp-server
poetry install
```

## Configuration

Add to your Claude Code MCP settings (`~/.claude/mcp.json`):

```json
{
  "mcpServers": {
    "ableton": {
      "command": "poetry",
      "args": ["run", "ableton-mcp"],
      "cwd": "/path/to/ableton-mcp-server"
    }
  }
}
```

Or if using the installed package:

```json
{
  "mcpServers": {
    "ableton": {
      "command": "ableton-mcp"
    }
  }
}
```

## Available Tools

### Song Tools
- `song_get_tempo` - Get current tempo in BPM
- `song_set_tempo` - Set tempo (20-999 BPM)
- `song_play` - Start playback
- `song_stop` - Stop playback
- `song_get_is_playing` - Check if playing
- `song_get_num_tracks` - Get track count
- `song_get_num_scenes` - Get scene count
- `song_create_midi_track` - Create a MIDI track
- `song_create_audio_track` - Create an audio track

### Track Tools
- `track_get_name` - Get track name
- `track_set_name` - Set track name
- `track_get_volume` - Get track volume (0-1)
- `track_set_volume` - Set track volume
- `track_set_mute` - Mute/unmute track
- `track_set_solo` - Solo/unsolo track
- `track_set_arm` - Arm/disarm track for recording

### Clip Slot Tools
- `clip_slot_create_clip` - Create a new MIDI clip
- `clip_slot_delete_clip` - Delete a clip
- `clip_slot_has_clip` - Check if slot has a clip

### Clip Tools
- `clip_fire` - Launch a clip
- `clip_stop` - Stop a clip
- `clip_add_notes` - Add MIDI notes to a clip
- `clip_get_notes` - Get all notes from a clip
- `clip_set_name` - Set clip name

### Scene Tools
- `scene_fire` - Launch a scene
- `scene_set_name` - Set scene name

### View Tools
- `view_get_selected_track` - Get selected track
- `view_set_selected_track` - Select a track
- `view_get_selected_scene` - Get selected scene
- `view_set_selected_scene` - Select a scene

## Development

```bash
# Run tests
poetry run pytest

# Run the server directly
poetry run ableton-mcp
```

## License

MIT
