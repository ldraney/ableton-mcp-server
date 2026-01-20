"""Song tools for the Ableton MCP server.

Covers song-level operations like tempo, transport, scenes, and global settings.
"""

import time
from typing import Annotated

from pydantic import Field

from ableton_mcp.connection import get_client
from abletonosc_client import Song


def register_song_tools(mcp):
    """Register all song tools with the MCP server."""

    # =============================================================================
    # Tempo & Transport
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
    def song_continue_playing() -> str:
        """Continue playback from current position.

        Returns:
            Confirmation message
        """
        song = Song(get_client())
        song.continue_playing()
        return "Playback continued"

    @mcp.tool()
    def song_get_is_playing() -> bool:
        """Check if the song is currently playing.

        Returns:
            True if playing, False if stopped
        """
        song = Song(get_client())
        return song.get_is_playing()

    # =============================================================================
    # Time Signature
    # =============================================================================

    @mcp.tool()
    def song_get_signature_numerator() -> int:
        """Get the time signature numerator.

        Returns:
            Time signature numerator (e.g., 4 for 4/4)
        """
        song = Song(get_client())
        return song.get_signature_numerator()

    @mcp.tool()
    def song_set_signature_numerator(
        numerator: Annotated[int, Field(description="Time signature numerator", ge=1)]
    ) -> str:
        """Set the time signature numerator.

        Args:
            numerator: Time signature numerator

        Returns:
            Confirmation message
        """
        song = Song(get_client())
        song.set_signature_numerator(numerator)
        return f"Time signature numerator set to {numerator}"

    @mcp.tool()
    def song_get_signature_denominator() -> int:
        """Get the time signature denominator.

        Returns:
            Time signature denominator (e.g., 4 for 4/4)
        """
        song = Song(get_client())
        return song.get_signature_denominator()

    @mcp.tool()
    def song_set_signature_denominator(
        denominator: Annotated[int, Field(description="Time signature denominator (must be power of 2)", ge=1)]
    ) -> str:
        """Set the time signature denominator.

        Args:
            denominator: Time signature denominator (must be power of 2)

        Returns:
            Confirmation message
        """
        song = Song(get_client())
        song.set_signature_denominator(denominator)
        return f"Time signature denominator set to {denominator}"

    # =============================================================================
    # Song Structure
    # =============================================================================

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
    def song_get_song_length() -> float:
        """Get the total song length in beats.

        Returns:
            Song length in beats
        """
        song = Song(get_client())
        return song.get_song_length()

    # =============================================================================
    # Position
    # =============================================================================

    @mcp.tool()
    def song_get_current_song_time() -> float:
        """Get the current playback position in beats.

        Returns:
            Current position in beats
        """
        song = Song(get_client())
        return song.get_current_song_time()

    @mcp.tool()
    def song_set_current_song_time(
        beats: Annotated[float, Field(description="Position in beats", ge=0)]
    ) -> str:
        """Set the playback position.

        Args:
            beats: Position in beats

        Returns:
            Confirmation message
        """
        song = Song(get_client())
        song.set_current_song_time(beats)
        return f"Playback position set to {beats} beats"

    @mcp.tool()
    def song_get_beat() -> float:
        """Get the current beat position.

        Returns:
            Current beat position
        """
        song = Song(get_client())
        return song.get_beat()

    # =============================================================================
    # Metronome
    # =============================================================================

    @mcp.tool()
    def song_get_metronome() -> bool:
        """Check if the metronome is enabled.

        Returns:
            True if metronome is on
        """
        song = Song(get_client())
        return song.get_metronome()

    @mcp.tool()
    def song_set_metronome(
        enabled: Annotated[bool, Field(description="True to enable metronome")]
    ) -> str:
        """Enable or disable the metronome.

        Args:
            enabled: True to enable metronome

        Returns:
            Confirmation message
        """
        song = Song(get_client())
        song.set_metronome(enabled)
        state = "enabled" if enabled else "disabled"
        return f"Metronome {state}"

    # =============================================================================
    # Record Mode
    # =============================================================================

    @mcp.tool()
    def song_get_record_mode() -> bool:
        """Check if record mode is enabled.

        Returns:
            True if record mode is on
        """
        song = Song(get_client())
        return song.get_record_mode()

    @mcp.tool()
    def song_set_record_mode(
        enabled: Annotated[bool, Field(description="True to enable record mode")]
    ) -> str:
        """Enable or disable record mode.

        Args:
            enabled: True to enable record mode

        Returns:
            Confirmation message
        """
        song = Song(get_client())
        song.set_record_mode(enabled)
        state = "enabled" if enabled else "disabled"
        return f"Record mode {state}"

    # =============================================================================
    # Loop Control
    # =============================================================================

    @mcp.tool()
    def song_get_loop() -> bool:
        """Check if loop is enabled.

        Returns:
            True if loop is enabled
        """
        song = Song(get_client())
        return song.get_loop()

    @mcp.tool()
    def song_set_loop(
        enabled: Annotated[bool, Field(description="True to enable loop")]
    ) -> str:
        """Enable or disable loop.

        Args:
            enabled: True to enable loop

        Returns:
            Confirmation message
        """
        song = Song(get_client())
        song.set_loop(enabled)
        state = "enabled" if enabled else "disabled"
        return f"Loop {state}"

    @mcp.tool()
    def song_get_loop_start() -> float:
        """Get the loop start position in beats.

        Returns:
            Loop start position in beats
        """
        song = Song(get_client())
        return song.get_loop_start()

    @mcp.tool()
    def song_set_loop_start(
        beats: Annotated[float, Field(description="Loop start position in beats", ge=0)]
    ) -> str:
        """Set the loop start position.

        Args:
            beats: Loop start position in beats

        Returns:
            Confirmation message
        """
        song = Song(get_client())
        song.set_loop_start(beats)
        return f"Loop start set to {beats} beats"

    @mcp.tool()
    def song_get_loop_length() -> float:
        """Get the loop length in beats.

        Returns:
            Loop length in beats
        """
        song = Song(get_client())
        return song.get_loop_length()

    @mcp.tool()
    def song_set_loop_length(
        beats: Annotated[float, Field(description="Loop length in beats", gt=0)]
    ) -> str:
        """Set the loop length.

        Args:
            beats: Loop length in beats

        Returns:
            Confirmation message
        """
        song = Song(get_client())
        song.set_loop_length(beats)
        return f"Loop length set to {beats} beats"

    # =============================================================================
    # Undo/Redo
    # =============================================================================

    @mcp.tool()
    def song_undo() -> str:
        """Undo the last action.

        Returns:
            Confirmation message
        """
        song = Song(get_client())
        song.undo()
        return "Undo performed"

    @mcp.tool()
    def song_redo() -> str:
        """Redo the last undone action.

        Returns:
            Confirmation message
        """
        song = Song(get_client())
        song.redo()
        return "Redo performed"

    @mcp.tool()
    def song_can_undo() -> bool:
        """Check if undo is available.

        Returns:
            True if undo is possible
        """
        song = Song(get_client())
        return song.can_undo()

    @mcp.tool()
    def song_can_redo() -> bool:
        """Check if redo is available.

        Returns:
            True if redo is possible
        """
        song = Song(get_client())
        return song.can_redo()

    # =============================================================================
    # Track Management
    # =============================================================================

    @mcp.tool()
    def song_clear_all_tracks() -> str:
        """Delete all tracks from the song.

        Deletes tracks from highest index to lowest to avoid index shifting issues.
        Includes a small delay between deletions for Ableton to process.

        Returns:
            Confirmation message with number of tracks deleted
        """
        song = Song(get_client())
        num_tracks = song.get_num_tracks()
        if num_tracks == 0:
            return "No tracks to delete"

        for i in range(num_tracks - 1, -1, -1):
            song.delete_track(i)
            time.sleep(0.1)

        return f"Deleted {num_tracks} tracks"

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

    @mcp.tool()
    def song_create_return_track() -> str:
        """Create a new return track.

        Returns:
            Confirmation message
        """
        song = Song(get_client())
        song.create_return_track()
        return "Return track created"

    @mcp.tool()
    def song_delete_track(
        index: Annotated[int, Field(description="Track index to delete (0-based)", ge=0)]
    ) -> str:
        """Delete track at index.

        Args:
            index: Track index to delete (0-based)

        Returns:
            Confirmation message
        """
        song = Song(get_client())
        song.delete_track(index)
        return f"Track {index} deleted"

    @mcp.tool()
    def song_delete_return_track(
        index: Annotated[int, Field(description="Return track index to delete (0-based)", ge=0)]
    ) -> str:
        """Delete return track at index.

        Args:
            index: Return track index to delete (0-based)

        Returns:
            Confirmation message
        """
        song = Song(get_client())
        song.delete_return_track(index)
        return f"Return track {index} deleted"

    @mcp.tool()
    def song_duplicate_track(
        index: Annotated[int, Field(description="Track index to duplicate (0-based)", ge=0)]
    ) -> str:
        """Duplicate track at index.

        Args:
            index: Track index to duplicate (0-based)

        Returns:
            Confirmation message
        """
        song = Song(get_client())
        song.duplicate_track(index)
        return f"Track {index} duplicated"

    # =============================================================================
    # Scene Management
    # =============================================================================

    @mcp.tool()
    def song_create_scene(
        index: Annotated[int, Field(description="Position to insert scene (-1 appends to end)")] = -1
    ) -> str:
        """Create a new scene.

        Args:
            index: Position to insert scene (-1 appends to end)

        Returns:
            Confirmation message
        """
        song = Song(get_client())
        song.create_scene(index)
        return f"Scene created at index {index}"

    @mcp.tool()
    def song_delete_scene(
        index: Annotated[int, Field(description="Scene index to delete (0-based)", ge=0)]
    ) -> str:
        """Delete scene at index.

        Args:
            index: Scene index to delete (0-based)

        Returns:
            Confirmation message
        """
        song = Song(get_client())
        song.delete_scene(index)
        return f"Scene {index} deleted"

    @mcp.tool()
    def song_duplicate_scene(
        index: Annotated[int, Field(description="Scene index to duplicate (0-based)", ge=0)]
    ) -> str:
        """Duplicate scene at index.

        Args:
            index: Scene index to duplicate (0-based)

        Returns:
            Confirmation message
        """
        song = Song(get_client())
        song.duplicate_scene(index)
        return f"Scene {index} duplicated"

    # =============================================================================
    # Groove
    # =============================================================================

    @mcp.tool()
    def song_get_groove_amount() -> float:
        """Get the global groove amount.

        Returns:
            Groove amount (0.0-1.0)
        """
        song = Song(get_client())
        return song.get_groove_amount()

    @mcp.tool()
    def song_set_groove_amount(
        amount: Annotated[float, Field(description="Groove amount (0.0-1.0)", ge=0, le=1)]
    ) -> str:
        """Set the global groove amount.

        Args:
            amount: Groove amount (0.0-1.0)

        Returns:
            Confirmation message
        """
        song = Song(get_client())
        song.set_groove_amount(amount)
        return f"Groove amount set to {amount}"

    # =============================================================================
    # Quantization
    # =============================================================================

    @mcp.tool()
    def song_get_midi_recording_quantization() -> int:
        """Get the MIDI recording quantization setting.

        Returns:
            Quantization value (0=None, 1=1/4, 2=1/8, 3=1/8T, 4=1/8+1/8T,
            5=1/16, 6=1/16T, 7=1/16+1/16T, 8=1/32)
        """
        song = Song(get_client())
        return song.get_midi_recording_quantization()

    @mcp.tool()
    def song_set_midi_recording_quantization(
        value: Annotated[int, Field(description="Quantization value (0-8)", ge=0, le=8)]
    ) -> str:
        """Set the MIDI recording quantization.

        Args:
            value: Quantization value (0=None, 1=1/4, 2=1/8, 3=1/8T, 4=1/8+1/8T,
                   5=1/16, 6=1/16T, 7=1/16+1/16T, 8=1/32)

        Returns:
            Confirmation message
        """
        song = Song(get_client())
        song.set_midi_recording_quantization(value)
        return f"MIDI recording quantization set to {value}"

    @mcp.tool()
    def song_get_clip_trigger_quantization() -> int:
        """Get the clip trigger quantization setting.

        Returns:
            Quantization value (0=None, 1=8 bars, 2=4 bars, 3=2 bars,
            4=1 bar, 5=1/2, 6=1/2T, 7=1/4, 8=1/4T, 9=1/8, 10=1/8T,
            11=1/16, 12=1/16T, 13=1/32)
        """
        song = Song(get_client())
        return song.get_clip_trigger_quantization()

    @mcp.tool()
    def song_set_clip_trigger_quantization(
        value: Annotated[int, Field(description="Quantization value (0-13)", ge=0, le=13)]
    ) -> str:
        """Set the clip trigger quantization.

        Args:
            value: Quantization value (0=None, 1=8 bars, 2=4 bars, 3=2 bars,
                   4=1 bar, 5=1/2, 6=1/2T, 7=1/4, 8=1/4T, 9=1/8, 10=1/8T,
                   11=1/16, 12=1/16T, 13=1/32)

        Returns:
            Confirmation message
        """
        song = Song(get_client())
        song.set_clip_trigger_quantization(value)
        return f"Clip trigger quantization set to {value}"

    # =============================================================================
    # Session Recording
    # =============================================================================

    @mcp.tool()
    def song_trigger_session_record() -> str:
        """Trigger session recording.

        Starts recording into the session view.

        Returns:
            Confirmation message
        """
        song = Song(get_client())
        song.trigger_session_record()
        return "Session recording triggered"

    @mcp.tool()
    def song_get_session_record() -> bool:
        """Check if session recording is enabled.

        Returns:
            True if session recording is enabled
        """
        song = Song(get_client())
        return song.get_session_record()

    @mcp.tool()
    def song_set_session_record(
        enabled: Annotated[bool, Field(description="True to enable session recording")]
    ) -> str:
        """Enable or disable session recording.

        Args:
            enabled: True to enable session recording

        Returns:
            Confirmation message
        """
        song = Song(get_client())
        song.set_session_record(enabled)
        state = "enabled" if enabled else "disabled"
        return f"Session recording {state}"

    @mcp.tool()
    def song_get_session_record_status() -> int:
        """Get the session record status.

        Returns:
            Session record status (0=Off, 1=On, 2=Transition)
        """
        song = Song(get_client())
        return song.get_session_record_status()

    # =============================================================================
    # Arrangement Recording
    # =============================================================================

    @mcp.tool()
    def song_get_arrangement_overdub() -> bool:
        """Check if arrangement overdub is enabled.

        Returns:
            True if arrangement overdub is enabled
        """
        song = Song(get_client())
        return song.get_arrangement_overdub()

    @mcp.tool()
    def song_set_arrangement_overdub(
        enabled: Annotated[bool, Field(description="True to enable arrangement overdub")]
    ) -> str:
        """Enable or disable arrangement overdub.

        Args:
            enabled: True to enable arrangement overdub

        Returns:
            Confirmation message
        """
        song = Song(get_client())
        song.set_arrangement_overdub(enabled)
        state = "enabled" if enabled else "disabled"
        return f"Arrangement overdub {state}"

    # =============================================================================
    # Punch In/Out
    # =============================================================================

    @mcp.tool()
    def song_get_punch_in() -> bool:
        """Check if punch-in is enabled.

        Returns:
            True if punch-in is enabled
        """
        song = Song(get_client())
        return song.get_punch_in()

    @mcp.tool()
    def song_set_punch_in(
        enabled: Annotated[bool, Field(description="True to enable punch-in")]
    ) -> str:
        """Enable or disable punch-in.

        Args:
            enabled: True to enable punch-in

        Returns:
            Confirmation message
        """
        song = Song(get_client())
        song.set_punch_in(enabled)
        state = "enabled" if enabled else "disabled"
        return f"Punch-in {state}"

    @mcp.tool()
    def song_get_punch_out() -> bool:
        """Check if punch-out is enabled.

        Returns:
            True if punch-out is enabled
        """
        song = Song(get_client())
        return song.get_punch_out()

    @mcp.tool()
    def song_set_punch_out(
        enabled: Annotated[bool, Field(description="True to enable punch-out")]
    ) -> str:
        """Enable or disable punch-out.

        Args:
            enabled: True to enable punch-out

        Returns:
            Confirmation message
        """
        song = Song(get_client())
        song.set_punch_out(enabled)
        state = "enabled" if enabled else "disabled"
        return f"Punch-out {state}"

    # =============================================================================
    # Navigation
    # =============================================================================

    @mcp.tool()
    def song_tap_tempo() -> str:
        """Tap tempo - call repeatedly to set tempo by tapping.

        Returns:
            Confirmation message
        """
        song = Song(get_client())
        song.tap_tempo()
        return "Tap tempo registered"

    @mcp.tool()
    def song_jump_by(
        beats: Annotated[float, Field(description="Number of beats to jump (negative to go backward)")]
    ) -> str:
        """Jump forward or backward by a number of beats.

        Args:
            beats: Number of beats to jump (negative to go backward)

        Returns:
            Confirmation message
        """
        song = Song(get_client())
        song.jump_by(beats)
        direction = "forward" if beats >= 0 else "backward"
        return f"Jumped {direction} by {abs(beats)} beats"

    @mcp.tool()
    def song_jump_to_next_cue() -> str:
        """Jump to the next cue point.

        Returns:
            Confirmation message
        """
        song = Song(get_client())
        song.jump_to_next_cue()
        return "Jumped to next cue point"

    @mcp.tool()
    def song_jump_to_prev_cue() -> str:
        """Jump to the previous cue point.

        Returns:
            Confirmation message
        """
        song = Song(get_client())
        song.jump_to_prev_cue()
        return "Jumped to previous cue point"

    @mcp.tool()
    def song_nudge_down() -> str:
        """Nudge tempo down (temporary slow down).

        Returns:
            Confirmation message
        """
        song = Song(get_client())
        song.nudge_down()
        return "Tempo nudged down"

    @mcp.tool()
    def song_nudge_up() -> str:
        """Nudge tempo up (temporary speed up).

        Returns:
            Confirmation message
        """
        song = Song(get_client())
        song.nudge_up()
        return "Tempo nudged up"

    # =============================================================================
    # Cue Points
    # =============================================================================

    @mcp.tool()
    def song_get_cue_points() -> list:
        """Get all cue points in the song.

        Returns:
            List of cue point data (name, time pairs)
        """
        song = Song(get_client())
        return list(song.get_cue_points())

    @mcp.tool()
    def song_cue_point_jump(
        cue_index: Annotated[int, Field(description="Cue point index (0-based)", ge=0)]
    ) -> str:
        """Jump to a specific cue point by index.

        Args:
            cue_index: Cue point index (0-based)

        Returns:
            Confirmation message
        """
        song = Song(get_client())
        song.cue_point_jump(cue_index)
        return f"Jumped to cue point {cue_index}"

    @mcp.tool()
    def song_cue_point_add_or_delete() -> str:
        """Add or delete a cue point at the current position.

        If a cue point exists at the current position, it will be deleted.
        Otherwise, a new cue point will be created.

        Returns:
            Confirmation message
        """
        song = Song(get_client())
        song.cue_point_add_or_delete()
        return "Cue point added or deleted at current position"

    @mcp.tool()
    def song_cue_point_set_name(
        cue_index: Annotated[int, Field(description="Cue point index (0-based)", ge=0)],
        name: Annotated[str, Field(description="New name for the cue point")]
    ) -> str:
        """Set the name of a cue point.

        Args:
            cue_index: Cue point index (0-based)
            name: New name for the cue point

        Returns:
            Confirmation message
        """
        song = Song(get_client())
        song.cue_point_set_name(cue_index, name)
        return f"Cue point {cue_index} renamed to '{name}'"

    # =============================================================================
    # Key and Scale
    # =============================================================================

    @mcp.tool()
    def song_get_root_note() -> int:
        """Get the root note of the song's key.

        Returns:
            Root note as MIDI note number (0-11, where 0=C, 1=C#, etc.)
        """
        song = Song(get_client())
        return song.get_root_note()

    @mcp.tool()
    def song_set_root_note(
        note: Annotated[int, Field(description="Root note (0-11, where 0=C, 1=C#, etc.)", ge=0, le=11)]
    ) -> str:
        """Set the root note of the song's key.

        Args:
            note: Root note as MIDI note number (0-11, where 0=C, 1=C#, etc.)

        Returns:
            Confirmation message
        """
        note_names = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
        song = Song(get_client())
        song.set_root_note(note)
        return f"Root note set to {note_names[note]}"

    @mcp.tool()
    def song_get_scale_name() -> str:
        """Get the scale name of the song.

        Returns:
            Scale name (e.g., "Major", "Minor", "Dorian")
        """
        song = Song(get_client())
        return song.get_scale_name()

    @mcp.tool()
    def song_set_scale_name(
        name: Annotated[str, Field(description="Scale name (e.g., 'Major', 'Minor', 'Dorian')")]
    ) -> str:
        """Set the scale name of the song.

        Args:
            name: Scale name (e.g., "Major", "Minor", "Dorian")

        Returns:
            Confirmation message
        """
        song = Song(get_client())
        song.set_scale_name(name)
        return f"Scale set to {name}"

    # =============================================================================
    # Clip Control
    # =============================================================================

    @mcp.tool()
    def song_stop_all_clips() -> str:
        """Stop all playing clips in the session.

        Returns:
            Confirmation message
        """
        song = Song(get_client())
        song.stop_all_clips()
        return "All clips stopped"

    @mcp.tool()
    def song_capture_midi() -> str:
        """Capture recently played MIDI notes into a clip.

        Creates a new clip from MIDI notes that were played
        while not recording (requires armed track).

        Returns:
            Confirmation message
        """
        song = Song(get_client())
        song.capture_midi()
        return "MIDI captured"

    # =============================================================================
    # Back to Arranger
    # =============================================================================

    @mcp.tool()
    def song_get_back_to_arranger() -> bool:
        """Check if back-to-arranger button is highlighted.

        Returns:
            True if back-to-arranger is active (session changes pending)
        """
        song = Song(get_client())
        return song.get_back_to_arranger()

    @mcp.tool()
    def song_set_back_to_arranger(
        enabled: Annotated[bool, Field(description="True to trigger back-to-arranger")]
    ) -> str:
        """Trigger back-to-arranger.

        When enabled=True, returns to arrangement view from session recording.

        Args:
            enabled: True to trigger back-to-arranger

        Returns:
            Confirmation message
        """
        song = Song(get_client())
        song.set_back_to_arranger(enabled)
        return "Back to arranger triggered" if enabled else "Back to arranger cleared"

    # =============================================================================
    # Bulk Queries
    # =============================================================================

    @mcp.tool()
    def song_get_track_names(
        start: Annotated[int, Field(description="Starting track index", ge=0)] = 0,
        end: Annotated[int, Field(description="Ending track index (-1 for all)")] = -1
    ) -> list[str]:
        """Get names of all tracks in a range.

        Args:
            start: Starting track index (default 0)
            end: Ending track index, exclusive (-1 for all)

        Returns:
            List of track names
        """
        song = Song(get_client())
        return list(song.get_track_names(start, end))

