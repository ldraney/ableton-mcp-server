# Ableton Live Control

Use the Ableton MCP tools to control Ableton Live via OSC. Requires Ableton Live running with AbletonOSC enabled.

## Prerequisites
- Ableton Live 12 running
- AbletonOSC MIDI Remote Script enabled (Preferences > Link/Tempo/MIDI)

## Tool Categories

### Song Control
- `song_get_tempo` / `song_set_tempo` - Get/set BPM (20-999)
- `song_play` / `song_stop` - Start/stop playback
- `song_get_is_playing` - Check playback state
- `song_get_num_tracks` / `song_get_num_scenes` - Get counts
- `song_create_midi_track` / `song_create_audio_track` - Create tracks

### Track Control
- `track_get_name` / `track_set_name` - Get/set track name
- `track_get_volume` / `track_set_volume` - Get/set volume (0.0-1.0, 0.85 = 0dB)
- `track_set_mute` / `track_set_solo` / `track_set_arm` - Toggle states

### Clip Operations
- `clip_slot_create_clip` - Create MIDI clip (specify length in beats)
- `clip_slot_delete_clip` / `clip_slot_has_clip` - Manage clips
- `clip_fire` / `clip_stop` - Launch/stop clips
- `clip_add_notes` - Add MIDI notes to a clip
- `clip_get_notes` - Read notes from a clip
- `clip_set_name` - Name a clip

### Scene Control
- `scene_fire` - Launch all clips in a scene
- `scene_set_name` - Name a scene

### View/Selection
- `view_get_selected_track` / `view_set_selected_track` - Track selection
- `view_get_selected_scene` / `view_set_selected_scene` - Scene selection

## Common Workflows

### Create a simple beat
```
1. song_create_midi_track(-1)           # Add MIDI track at end
2. track_set_name(track_idx, "Drums")   # Name it
3. clip_slot_create_clip(track_idx, 0, 16.0)  # 4-bar clip
4. clip_add_notes(track_idx, 0, [...])  # Add drum pattern
5. clip_fire(track_idx, 0)              # Launch it
```

### Note format for clip_add_notes
```json
[
  {"pitch": 60, "start_time": 0.0, "duration": 0.5, "velocity": 100},
  {"pitch": 64, "start_time": 0.5, "duration": 0.5, "velocity": 80}
]
```
- pitch: MIDI note (60 = C4, 36 = kick, 38 = snare, 42 = hi-hat)
- start_time: Position in beats (0.0 = beat 1)
- duration: Length in beats
- velocity: 0-127

### MIDI note reference
- Kick: 36 (C1)
- Snare: 38 (D1)
- Hi-hat: 42 (F#1)
- C4 (middle C): 60
- Octave = 12 semitones

## Tips
- Track/scene indices are 0-based
- Volume 0.85 = unity gain (0dB)
- Clip lengths are in beats (4 = 1 bar at 4/4)
- Use `view_set_selected_track` before operations to show user what you're doing
