"""MCP server for Ableton Live control.

Exposes tools for controlling Ableton Live via the Model Context Protocol.
"""

from typing import Annotated

from fastmcp import FastMCP
from pydantic import Field

from ableton_mcp.connection import get_client
from abletonosc_client import Song, Track, Clip, ClipSlot, Scene, View
from abletonosc_client.clip import Note

# Create FastMCP server
mcp = FastMCP("Ableton MCP Server")


# =============================================================================
# Song Tools
# =============================================================================


@mcp.tool()
def song_get_tempo() -> float:
    """Get the current song tempo in BPM.

    Returns:
        Current tempo in beats per minute (20-999)
    """
    song = Song(get_client())
    return song.get_tempo()


@mcp.tool()
def song_set_tempo(
    bpm: Annotated[float, Field(description="Tempo in beats per minute (20-999)", ge=20, le=999)]
) -> str:
    """Set the song tempo.

    Args:
        bpm: Tempo in beats per minute (20-999)

    Returns:
        Confirmation message with the new tempo
    """
    song = Song(get_client())
    song.set_tempo(bpm)
    return f"Tempo set to {bpm} BPM"


@mcp.tool()
def song_play() -> str:
    """Start playback.

    Returns:
        Confirmation message
    """
    song = Song(get_client())
    song.start_playing()
    return "Playback started"


@mcp.tool()
def song_stop() -> str:
    """Stop playback.

    Returns:
        Confirmation message
    """
    song = Song(get_client())
    song.stop_playing()
    return "Playback stopped"


@mcp.tool()
def song_get_is_playing() -> bool:
    """Check if the song is currently playing.

    Returns:
        True if playing, False if stopped
    """
    song = Song(get_client())
    return song.get_is_playing()


@mcp.tool()
def song_get_num_tracks() -> int:
    """Get the number of tracks in the song.

    Returns:
        Number of tracks
    """
    song = Song(get_client())
    return song.get_num_tracks()


@mcp.tool()
def song_get_num_scenes() -> int:
    """Get the number of scenes in the song.

    Returns:
        Number of scenes
    """
    song = Song(get_client())
    return song.get_num_scenes()


@mcp.tool()
def song_create_midi_track(
    index: Annotated[int, Field(description="Position to insert track (-1 appends to end)")] = -1
) -> str:
    """Create a new MIDI track.

    Args:
        index: Position to insert track (-1 appends to end)

    Returns:
        Confirmation message
    """
    song = Song(get_client())
    song.create_midi_track(index)
    return f"MIDI track created at index {index}"


@mcp.tool()
def song_create_audio_track(
    index: Annotated[int, Field(description="Position to insert track (-1 appends to end)")] = -1
) -> str:
    """Create a new audio track.

    Args:
        index: Position to insert track (-1 appends to end)

    Returns:
        Confirmation message
    """
    song = Song(get_client())
    song.create_audio_track(index)
    return f"Audio track created at index {index}"


# =============================================================================
# Track Tools
# =============================================================================


@mcp.tool()
def track_get_name(
    track_index: Annotated[int, Field(description="Track index (0-based)", ge=0)]
) -> str:
    """Get the name of a track.

    Args:
        track_index: Track index (0-based)

    Returns:
        Track name
    """
    track = Track(get_client())
    return track.get_name(track_index)


@mcp.tool()
def track_set_name(
    track_index: Annotated[int, Field(description="Track index (0-based)", ge=0)],
    name: Annotated[str, Field(description="New track name")]
) -> str:
    """Set the name of a track.

    Args:
        track_index: Track index (0-based)
        name: New track name

    Returns:
        Confirmation message
    """
    track = Track(get_client())
    track.set_name(track_index, name)
    return f"Track {track_index} renamed to '{name}'"


@mcp.tool()
def track_get_volume(
    track_index: Annotated[int, Field(description="Track index (0-based)", ge=0)]
) -> float:
    """Get the volume of a track.

    Args:
        track_index: Track index (0-based)

    Returns:
        Volume level (0.0-1.0, where 0.85 is 0dB)
    """
    track = Track(get_client())
    return track.get_volume(track_index)


@mcp.tool()
def track_set_volume(
    track_index: Annotated[int, Field(description="Track index (0-based)", ge=0)],
    volume: Annotated[float, Field(description="Volume level (0.0-1.0, where 0.85 is 0dB)", ge=0, le=1)]
) -> str:
    """Set the volume of a track.

    Args:
        track_index: Track index (0-based)
        volume: Volume level (0.0-1.0, where 0.85 is 0dB)

    Returns:
        Confirmation message
    """
    track = Track(get_client())
    track.set_volume(track_index, volume)
    return f"Track {track_index} volume set to {volume}"


@mcp.tool()
def track_set_mute(
    track_index: Annotated[int, Field(description="Track index (0-based)", ge=0)],
    muted: Annotated[bool, Field(description="True to mute, False to unmute")]
) -> str:
    """Mute or unmute a track.

    Args:
        track_index: Track index (0-based)
        muted: True to mute, False to unmute

    Returns:
        Confirmation message
    """
    track = Track(get_client())
    track.set_mute(track_index, muted)
    state = "muted" if muted else "unmuted"
    return f"Track {track_index} {state}"


@mcp.tool()
def track_set_solo(
    track_index: Annotated[int, Field(description="Track index (0-based)", ge=0)],
    soloed: Annotated[bool, Field(description="True to solo, False to unsolo")]
) -> str:
    """Solo or unsolo a track.

    Args:
        track_index: Track index (0-based)
        soloed: True to solo, False to unsolo

    Returns:
        Confirmation message
    """
    track = Track(get_client())
    track.set_solo(track_index, soloed)
    state = "soloed" if soloed else "unsoloed"
    return f"Track {track_index} {state}"


@mcp.tool()
def track_set_arm(
    track_index: Annotated[int, Field(description="Track index (0-based)", ge=0)],
    armed: Annotated[bool, Field(description="True to arm, False to disarm")]
) -> str:
    """Arm or disarm a track for recording.

    Args:
        track_index: Track index (0-based)
        armed: True to arm, False to disarm

    Returns:
        Confirmation message
    """
    track = Track(get_client())
    track.set_arm(track_index, armed)
    state = "armed" if armed else "disarmed"
    return f"Track {track_index} {state}"


# =============================================================================
# Clip Slot Tools
# =============================================================================


@mcp.tool()
def clip_slot_create_clip(
    track_index: Annotated[int, Field(description="Track index (0-based)", ge=0)],
    scene_index: Annotated[int, Field(description="Scene index (0-based)", ge=0)],
    length: Annotated[float, Field(description="Clip length in beats", gt=0)] = 4.0
) -> str:
    """Create a new MIDI clip in a clip slot.

    Args:
        track_index: Track index (0-based)
        scene_index: Scene index (0-based)
        length: Clip length in beats (default 4.0 = 1 bar at 4/4)

    Returns:
        Confirmation message
    """
    clip_slot = ClipSlot(get_client())
    clip_slot.create_clip(track_index, scene_index, length)
    return f"Clip created at track {track_index}, scene {scene_index} with length {length} beats"


@mcp.tool()
def clip_slot_delete_clip(
    track_index: Annotated[int, Field(description="Track index (0-based)", ge=0)],
    scene_index: Annotated[int, Field(description="Scene index (0-based)", ge=0)]
) -> str:
    """Delete a clip from a clip slot.

    Args:
        track_index: Track index (0-based)
        scene_index: Scene index (0-based)

    Returns:
        Confirmation message
    """
    clip_slot = ClipSlot(get_client())
    clip_slot.delete_clip(track_index, scene_index)
    return f"Clip deleted from track {track_index}, scene {scene_index}"


@mcp.tool()
def clip_slot_has_clip(
    track_index: Annotated[int, Field(description="Track index (0-based)", ge=0)],
    scene_index: Annotated[int, Field(description="Scene index (0-based)", ge=0)]
) -> bool:
    """Check if a clip slot contains a clip.

    Args:
        track_index: Track index (0-based)
        scene_index: Scene index (0-based)

    Returns:
        True if the slot contains a clip
    """
    clip_slot = ClipSlot(get_client())
    return clip_slot.has_clip(track_index, scene_index)


# =============================================================================
# Clip Tools
# =============================================================================


@mcp.tool()
def clip_fire(
    track_index: Annotated[int, Field(description="Track index (0-based)", ge=0)],
    scene_index: Annotated[int, Field(description="Scene index (0-based)", ge=0)]
) -> str:
    """Launch (fire) a clip.

    Args:
        track_index: Track index (0-based)
        scene_index: Scene index (0-based)

    Returns:
        Confirmation message
    """
    clip = Clip(get_client())
    clip.fire(track_index, scene_index)
    return f"Clip fired at track {track_index}, scene {scene_index}"


@mcp.tool()
def clip_stop(
    track_index: Annotated[int, Field(description="Track index (0-based)", ge=0)],
    scene_index: Annotated[int, Field(description="Scene index (0-based)", ge=0)]
) -> str:
    """Stop a clip.

    Args:
        track_index: Track index (0-based)
        scene_index: Scene index (0-based)

    Returns:
        Confirmation message
    """
    clip = Clip(get_client())
    clip.stop(track_index, scene_index)
    return f"Clip stopped at track {track_index}, scene {scene_index}"


@mcp.tool()
def clip_add_notes(
    track_index: Annotated[int, Field(description="Track index (0-based)", ge=0)],
    scene_index: Annotated[int, Field(description="Scene index (0-based)", ge=0)],
    notes: Annotated[list[dict], Field(
        description="List of notes, each with pitch (0-127), start_time (beats), duration (beats), velocity (0-127)"
    )]
) -> str:
    """Add MIDI notes to a clip.

    Args:
        track_index: Track index (0-based)
        scene_index: Scene index (0-based)
        notes: List of notes, each dict with: pitch (0-127), start_time (beats), duration (beats), velocity (0-127)

    Returns:
        Confirmation message

    Example notes:
        [
            {"pitch": 60, "start_time": 0.0, "duration": 0.5, "velocity": 100},
            {"pitch": 64, "start_time": 0.5, "duration": 0.5, "velocity": 100}
        ]
    """
    clip = Clip(get_client())
    note_objects = [
        Note(
            pitch=n["pitch"],
            start_time=n["start_time"],
            duration=n["duration"],
            velocity=n["velocity"],
            mute=n.get("mute", False)
        )
        for n in notes
    ]
    clip.add_notes(track_index, scene_index, note_objects)
    return f"Added {len(notes)} notes to clip at track {track_index}, scene {scene_index}"


@mcp.tool()
def clip_get_notes(
    track_index: Annotated[int, Field(description="Track index (0-based)", ge=0)],
    scene_index: Annotated[int, Field(description="Scene index (0-based)", ge=0)]
) -> list[dict]:
    """Get all notes from a MIDI clip.

    Args:
        track_index: Track index (0-based)
        scene_index: Scene index (0-based)

    Returns:
        List of notes, each with pitch, start_time, duration, velocity, mute
    """
    clip = Clip(get_client())
    notes = clip.get_notes(track_index, scene_index)
    return [
        {
            "pitch": n.pitch,
            "start_time": n.start_time,
            "duration": n.duration,
            "velocity": n.velocity,
            "mute": n.mute
        }
        for n in notes
    ]


@mcp.tool()
def clip_set_name(
    track_index: Annotated[int, Field(description="Track index (0-based)", ge=0)],
    scene_index: Annotated[int, Field(description="Scene index (0-based)", ge=0)],
    name: Annotated[str, Field(description="New clip name")]
) -> str:
    """Set the name of a clip.

    Args:
        track_index: Track index (0-based)
        scene_index: Scene index (0-based)
        name: New clip name

    Returns:
        Confirmation message
    """
    clip = Clip(get_client())
    clip.set_name(track_index, scene_index, name)
    return f"Clip at track {track_index}, scene {scene_index} renamed to '{name}'"


# =============================================================================
# Scene Tools
# =============================================================================


@mcp.tool()
def scene_fire(
    scene_index: Annotated[int, Field(description="Scene index (0-based)", ge=0)]
) -> str:
    """Fire (launch) a scene.

    Args:
        scene_index: Scene index (0-based)

    Returns:
        Confirmation message
    """
    scene = Scene(get_client())
    scene.fire(scene_index)
    return f"Scene {scene_index} fired"


@mcp.tool()
def scene_set_name(
    scene_index: Annotated[int, Field(description="Scene index (0-based)", ge=0)],
    name: Annotated[str, Field(description="New scene name")]
) -> str:
    """Set the name of a scene.

    Args:
        scene_index: Scene index (0-based)
        name: New scene name

    Returns:
        Confirmation message
    """
    scene = Scene(get_client())
    scene.set_name(scene_index, name)
    return f"Scene {scene_index} renamed to '{name}'"


# =============================================================================
# View Tools
# =============================================================================


@mcp.tool()
def view_get_selected_track() -> int:
    """Get the currently selected track index.

    Returns:
        Selected track index (0-based)
    """
    view = View(get_client())
    return view.get_selected_track()


@mcp.tool()
def view_set_selected_track(
    track_index: Annotated[int, Field(description="Track index (0-based)", ge=0)]
) -> str:
    """Select a track in the view.

    Args:
        track_index: Track index (0-based)

    Returns:
        Confirmation message
    """
    view = View(get_client())
    view.set_selected_track(track_index)
    return f"Track {track_index} selected"


@mcp.tool()
def view_get_selected_scene() -> int:
    """Get the currently selected scene index.

    Returns:
        Selected scene index (0-based)
    """
    view = View(get_client())
    return view.get_selected_scene()


@mcp.tool()
def view_set_selected_scene(
    scene_index: Annotated[int, Field(description="Scene index (0-based)", ge=0)]
) -> str:
    """Select a scene in the view.

    Args:
        scene_index: Scene index (0-based)

    Returns:
        Confirmation message
    """
    view = View(get_client())
    view.set_selected_scene(scene_index)
    return f"Scene {scene_index} selected"


def main():
    """Run the MCP server."""
    mcp.run()


if __name__ == "__main__":
    main()
