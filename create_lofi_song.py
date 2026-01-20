#!/usr/bin/env python3
"""Create a 3-minute lofi study beats track in Ableton Live.

This script uses the ableton-osc-client to create a chill lofi song
with drums, bass, keys, melody, pad, and vinyl textures.
"""

import time
from abletonosc_client import (
    Client, Song, Track, Clip, ClipSlot, Device, View
)
from abletonosc_client.clip import Note


def main():
    # Initialize OSC client
    print("Connecting to Ableton Live...")
    client = Client()

    song = Song(client)
    track = Track(client)
    clip = Clip(client)
    clip_slot = ClipSlot(client)
    device = Device(client)
    view = View(client)

    # ==========================================================================
    # Phase 1: Setup
    # ==========================================================================
    print("\n=== Phase 1: Setup ===")

    # Stop playback first
    print("Stopping playback...")
    song.stop_playing()
    time.sleep(0.3)

    # Clear all existing tracks (delete backwards)
    print("Clearing existing tracks...")
    num_tracks = song.get_num_tracks()
    if num_tracks > 0:
        for i in range(num_tracks - 1, -1, -1):
            song.delete_track(i)
            time.sleep(0.15)
        print(f"Deleted {num_tracks} tracks")

    # Set tempo to 85 BPM (classic lofi range)
    print("Setting tempo to 85 BPM...")
    song.set_tempo(85)
    time.sleep(0.2)

    # Set key to D minor (root=2 for D, scale="Minor")
    print("Setting key to D minor...")
    song.set_root_note(2)  # D
    song.set_scale_name("Minor")
    time.sleep(0.2)

    # ==========================================================================
    # Phase 2: Create Tracks and Instruments
    # ==========================================================================
    print("\n=== Phase 2: Creating Tracks ===")

    track_config = [
        ("Drums", "Drum Rack"),
        ("Bass", "Wavetable"),
        ("Keys", "Electric"),
        ("Melody", "Wavetable"),
        ("Pad", "Wavetable"),
        ("Vinyl", "Operator"),
    ]

    for i, (name, instrument) in enumerate(track_config):
        print(f"Creating track {i}: {name} ({instrument})...")
        song.create_midi_track(-1)
        time.sleep(0.3)

        # Select track before inserting device
        view.set_selected_track(i)
        time.sleep(0.1)

        # Insert instrument
        result = track.insert_device(i, instrument, -1)
        time.sleep(0.4)

        if result == -1:
            print(f"  Warning: Device '{instrument}' not found")
        else:
            print(f"  Inserted {instrument} at device index {result}")

        # Set track name
        track.set_name(i, name)
        time.sleep(0.1)

    # Create return tracks for effects
    print("\nCreating return tracks...")
    song.create_return_track()
    time.sleep(0.3)
    song.create_return_track()
    time.sleep(0.3)

    # ==========================================================================
    # Phase 3: Create Clips
    # ==========================================================================
    print("\n=== Phase 3: Creating Clips ===")

    # Create 8-beat drum clip (scene 0)
    print("Creating drum clip (8 beats)...")
    clip_slot.create_clip(0, 0, 8.0)
    time.sleep(0.2)

    # Create 16-beat bass clip (scene 0) - covers 2 chord changes
    print("Creating bass clip (16 beats)...")
    clip_slot.create_clip(1, 0, 16.0)
    time.sleep(0.2)

    # Create 32-beat keys clip (scene 0) - full chord progression
    print("Creating keys clip (32 beats)...")
    clip_slot.create_clip(2, 0, 32.0)
    time.sleep(0.2)

    # Create 32-beat melody clip (scene 0)
    print("Creating melody clip (32 beats)...")
    clip_slot.create_clip(3, 0, 32.0)
    time.sleep(0.2)

    # Create 32-beat pad clip (scene 0)
    print("Creating pad clip (32 beats)...")
    clip_slot.create_clip(4, 0, 32.0)
    time.sleep(0.2)

    # Create 32-beat vinyl clip (scene 0)
    print("Creating vinyl clip (32 beats)...")
    clip_slot.create_clip(5, 0, 32.0)
    time.sleep(0.2)

    # ==========================================================================
    # Phase 4: Program Notes
    # ==========================================================================
    print("\n=== Phase 4: Programming Notes ===")

    # --- Drum Pattern (Track 0) ---
    print("Programming drum pattern...")
    drum_notes = []

    # Kicks (MIDI note 36)
    kicks = [
        (0.0, 0.5, 100),
        (1.5, 0.5, 80),
        (4.0, 0.5, 100),
        (5.0, 0.5, 70),
        (6.5, 0.5, 90),
    ]
    for start, dur, vel in kicks:
        drum_notes.append(Note(36, start, dur, vel))

    # Snares (MIDI note 38)
    snares = [
        (1.0, 0.5, 90),
        (3.0, 0.5, 85),
        (5.0, 0.5, 90),
        (7.0, 0.5, 85),
    ]
    for start, dur, vel in snares:
        drum_notes.append(Note(38, start, dur, vel))

    # Hi-hats (MIDI note 42) - every half beat with swing
    for i in range(16):
        vel = 60 + (i % 2) * 20  # Alternate velocity
        drum_notes.append(Note(42, i * 0.5, 0.25, vel))

    clip.add_notes(0, 0, drum_notes)
    time.sleep(0.2)

    # --- Bass Line (Track 1) ---
    print("Programming bass line...")
    bass_notes = []

    # First 8 beats: Em7 root (E=40) and A7 root (A=33)
    # E2 = 40
    bass_notes.append(Note(40, 0.0, 1.5, 100))   # E (root of Em7)
    bass_notes.append(Note(40, 2.0, 0.5, 70))    # E ghost
    bass_notes.append(Note(40, 3.5, 0.5, 80))    # E pickup
    bass_notes.append(Note(33, 4.0, 1.5, 100))   # A (root of A7)
    bass_notes.append(Note(33, 6.0, 0.5, 70))    # A ghost
    bass_notes.append(Note(45, 6.5, 0.5, 90))    # A octave jump

    # Second 8 beats: Dmaj7 root (D=38) and Bm7 root (B=35)
    bass_notes.append(Note(38, 8.0, 1.5, 100))   # D (root of Dmaj7)
    bass_notes.append(Note(38, 10.0, 0.5, 70))   # D ghost
    bass_notes.append(Note(38, 11.5, 0.5, 80))   # D pickup
    bass_notes.append(Note(35, 12.0, 1.5, 100))  # B (root of Bm7)
    bass_notes.append(Note(35, 14.0, 1.0, 80))   # B ghost

    clip.add_notes(1, 0, bass_notes)
    time.sleep(0.2)

    # --- Keys/Chords (Track 2) ---
    print("Programming keys/chords...")
    keys_notes = []

    # Em7 chord (bars 1-2, beats 0-8)
    # E3=52, G3=55, B3=59, D4=62
    for pitch in [52, 55, 59, 62]:
        keys_notes.append(Note(pitch, 0.0, 7.5, 70))

    # A7 chord (bars 3-4, beats 8-16)
    # A2=45, C#3=49, E3=52, G3=55
    for pitch in [45, 49, 52, 55]:
        keys_notes.append(Note(pitch, 8.0, 7.5, 70))

    # Dmaj7 chord (bars 5-6, beats 16-24)
    # D3=50, F#3=54, A3=57, C#4=61
    for pitch in [50, 54, 57, 61]:
        keys_notes.append(Note(pitch, 16.0, 7.5, 70))

    # Bm7 chord (bars 7-8, beats 24-32)
    # B2=47, D3=50, F#3=54, A3=57
    for pitch in [47, 50, 54, 57]:
        keys_notes.append(Note(pitch, 24.0, 7.5, 70))

    clip.add_notes(2, 0, keys_notes)
    time.sleep(0.2)

    # --- Melody (Track 3) ---
    print("Programming melody...")
    melody_notes = []

    # Sparse, study-friendly melody using D minor pentatonic
    # D=62, F=65, G=67, A=69, C=72
    melody_notes.append(Note(62, 0.0, 3.0, 65))    # D (long, gentle)
    melody_notes.append(Note(67, 4.0, 2.0, 60))    # G
    melody_notes.append(Note(69, 10.0, 2.0, 65))   # A
    melody_notes.append(Note(67, 14.0, 1.5, 55))   # G (soft)
    melody_notes.append(Note(65, 18.0, 4.0, 60))   # F (held)
    melody_notes.append(Note(62, 26.0, 5.0, 70))   # D (resolve, fade)

    clip.add_notes(3, 0, melody_notes)
    time.sleep(0.2)

    # --- Pad (Track 4) ---
    print("Programming pad...")
    pad_notes = []

    # Sustained chords, very soft for atmosphere
    # Em add9 (E, G, B, F#) for ethereal quality
    for pitch in [52, 55, 59, 66]:  # E3, G3, B3, F#4
        pad_notes.append(Note(pitch, 0.0, 15.5, 50))

    # D add9
    for pitch in [50, 54, 57, 64]:  # D3, F#3, A3, E4
        pad_notes.append(Note(pitch, 16.0, 15.5, 50))

    clip.add_notes(4, 0, pad_notes)
    time.sleep(0.2)

    # --- Vinyl Crackle (Track 5) ---
    print("Programming vinyl texture...")
    vinyl_notes = []

    # Low, sustained notes to generate noise texture with Operator
    # The actual sound depends on Operator preset, but we add long notes
    vinyl_notes.append(Note(36, 0.0, 32.0, 40))  # Very soft, constant

    clip.add_notes(5, 0, vinyl_notes)
    time.sleep(0.2)

    # ==========================================================================
    # Phase 5: Effects & Mixing
    # ==========================================================================
    print("\n=== Phase 5: Setting Up Mix ===")

    # Set track volumes
    print("Setting track volumes...")
    volumes = [0.75, 0.80, 0.65, 0.60, 0.50, 0.30]
    for i, vol in enumerate(volumes):
        track.set_volume(i, vol)
        time.sleep(0.1)

    # Set some groove
    print("Adding groove...")
    song.set_groove_amount(0.3)
    time.sleep(0.1)

    # ==========================================================================
    # Phase 6: Enable Loop
    # ==========================================================================
    print("\n=== Phase 6: Setting Up Loop ===")

    # Set loop for 32 beats (8 bars)
    song.set_loop(True)
    song.set_loop_start(0)
    song.set_loop_length(32)
    time.sleep(0.2)

    # ==========================================================================
    # Done!
    # ==========================================================================
    print("\n=== Lofi Song Created! ===")
    print("\nTrack layout:")
    print("  0: Drums   - 8-beat boom-bap pattern")
    print("  1: Bass    - 16-beat bass line following chords")
    print("  2: Keys    - 32-beat Rhodes chord progression")
    print("  3: Melody  - 32-beat sparse pentatonic melody")
    print("  4: Pad     - 32-beat atmospheric texture")
    print("  5: Vinyl   - 32-beat lo-fi texture")
    print("\nChord progression: Em7 - A7 - Dmaj7 - Bm7")
    print("Tempo: 85 BPM")
    print("Key: D minor")
    print("\nTo play: Use song_play or press play in Ableton")
    print("Tip: Fire all clips in scene 0 to hear the full arrangement")


if __name__ == "__main__":
    main()
