# For reading MIDI files and extracting notes
from music21 import converter, instrument, note, chord
import os

def extract_notes_from_midi(midi_folder):
    notes = []
    for file in os.listdir(midi_folder):
        if file.endswith(".mid"):
            midi = converter.parse(os.path.join(midi_folder, file))
            notes_to_parse = midi.flat.notes
            for element in notes_to_parse:
                if isinstance(element, note.Note):
                    notes.append(str(element.pitch))
                elif isinstance(element, chord.Chord):
                    notes.append('.'.join(str(n) for n in element.normalOrder))
    return notes
