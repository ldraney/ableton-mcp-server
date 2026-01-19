# Troubleshooting & QA Guide

## Quick Diagnostic

```python
from osc_client import connect
from osc_client.song import Song

client = connect()

# 1. Test connection
result = client.query('/live/test')
print(f"Connection: {result}")  # Should print ('ok',)

# 2. Check track count
song = Song(client)
print(f"Tracks: {song.get_num_tracks()}")

# 3. Check tempo
print(f"Tempo: {song.get_tempo()}")

client.close()
```

If step 1 fails → AbletonOSC not running or wrong port.

---

## Common Problems

### "TimeoutError: No response for /live/... within 2.0s"

**Causes:**
1. AbletonOSC not enabled in Ableton
2. Wrong port (should be 11000 send, 11001 receive)
3. Endpoint doesn't exist (typo or not implemented)
4. AbletonOSC crashed silently

**Fixes:**
- Check Ableton preferences → Link/Tempo/MIDI → Control Surface = AbletonOSC
- Restart Ableton completely
- Check `~/AbletonOSC/logs/abletonosc.log` for errors

### "insert_device times out"

This endpoint is in our fork, not upstream AbletonOSC.

**Fix:**
1. Ensure `~/AbletonOSC` is our fork (ldraney/AbletonOSC)
2. Ensure symlink exists:
   ```bash
   ls -la ~/Music/Ableton/User\ Library/Remote\ Scripts/AbletonOSC
   # Should show: AbletonOSC -> /Users/YOU/AbletonOSC
   ```
3. **Restart Ableton completely** (reload won't work after symlink change)

### "Tracks playing over each other / chaos"

Multiple songs or old tracks conflicting.

**Fix - Clean slate:**
```python
from osc_client import connect
from osc_client.song import Song
import time

client = connect()
song = Song(client)
song.stop_playing()

# DELETE BACKWARDS to avoid index shift
num_tracks = song.get_num_tracks()
for i in range(num_tracks - 1, -1, -1):
    try:
        song.delete_track(i)
        time.sleep(0.1)
    except:
        pass

print(f"Remaining: {song.get_num_tracks()}")  # Usually 1 (can't delete last)
client.close()
```

Then recreate your song fresh.

### "Notes not playing / silent"

**Check:**
1. Is there a device on the track? Empty MIDI track = silence
2. Is the clip fired? `clip_slot.fire(track_idx, scene_idx)`
3. Is Ableton's master volume up?
4. Is the track muted? `track.get_mute(idx)`

---

## Critical Patterns

### 1. Always Sleep Between Operations

Ableton needs processing time:
```python
song.create_midi_track(-1)
time.sleep(0.3)  # REQUIRED

track.insert_device(idx, "Wavetable")
time.sleep(0.3)  # REQUIRED

clip_slot.create_clip(idx, 0, 16.0)
time.sleep(0.2)  # REQUIRED
```

Without sleeps → race conditions → missing devices/clips.

### 2. Delete Tracks Backwards

```python
# WRONG - indices shift as you delete
for i in range(num_tracks):
    song.delete_track(i)  # BREAKS

# RIGHT - delete from end
for i in range(num_tracks - 1, -1, -1):
    song.delete_track(i)  # WORKS
```

### 3. Get Track Index Before Creating

```python
# Track will be created at current count
start_tracks = song.get_num_tracks()
song.create_midi_track(-1)
time.sleep(0.3)
# New track is now at index `start_tracks`
my_track_idx = start_tracks
```

### 4. Fire Clips to Hear Them

Creating a clip doesn't play it:
```python
clip_slot.create_clip(track_idx, scene_idx, 16.0)
clip.add_notes(track_idx, scene_idx, notes)
# Still silent!

clip_slot.fire(track_idx, scene_idx)  # NOW it plays
```

---

## Working Song Template

```python
"""Minimal working song template."""
import time
import sys
sys.path.insert(0, '/Users/ldraney/ableton-music-development')

from osc_client import connect
from osc_client.song import Song
from osc_client.track import Track
from osc_client.clip_slot import ClipSlot
from osc_client.clip import Clip, Note


def create_song():
    client = connect()
    song = Song(client)
    track = Track(client)
    clip_slot = ClipSlot(client)
    clip = Clip(client)

    # Stop anything playing
    song.stop_playing()

    # Set tempo
    song.set_tempo(90.0)

    # Get starting index
    start_idx = song.get_num_tracks()

    # Create track
    song.create_midi_track(-1)
    time.sleep(0.3)

    # Add instrument
    track.insert_device(start_idx, "Wavetable")
    time.sleep(0.3)

    # Create clip (4 bars = 16 beats)
    clip_slot.create_clip(start_idx, 0, 16.0)
    time.sleep(0.2)

    # Add notes
    notes = [
        Note(pitch=60, start_time=0.0, duration=1.0, velocity=100),
        Note(pitch=64, start_time=1.0, duration=1.0, velocity=100),
        Note(pitch=67, start_time=2.0, duration=1.0, velocity=100),
        Note(pitch=72, start_time=3.0, duration=1.0, velocity=100),
    ]
    clip.add_notes(start_idx, 0, notes)
    time.sleep(0.1)

    # FIRE to play
    clip_slot.fire(start_idx, 0)

    print("Playing!")
    client.close()


if __name__ == "__main__":
    create_song()
```

---

## QA Checklist

Before reporting "it doesn't work":

- [ ] `client.query('/live/test')` returns `('ok',)`
- [ ] Ableton is open with a project loaded
- [ ] AbletonOSC shows in Control Surface preferences
- [ ] `~/AbletonOSC` is symlinked to Remote Scripts (if using fork features)
- [ ] Ableton was **restarted** (not just reloaded) after symlink
- [ ] Code includes `time.sleep()` after create/insert operations
- [ ] Clips are fired with `clip_slot.fire()`
- [ ] Track has a device (instrument) on it

---

## Log Locations

- AbletonOSC: `~/AbletonOSC/logs/abletonosc.log`
- Ableton crash: `~/Library/Logs/DiagnosticReports/`

## Useful Debug Commands

```python
# See all tracks
for i in range(song.get_num_tracks()):
    print(f"{i}: {track.get_name(i)}")

# See devices on track
print(track.get_device_names(0))

# See if clip exists
print(clip_slot.has_clip(0, 0))
```
