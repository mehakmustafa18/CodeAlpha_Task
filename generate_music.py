# Script to generate new music
from music21 import stream, note, chord
from keras.models import load_model
import pickle
import numpy as np
import random

# Load model and data
model = load_model("models/model.h5")
with open("data/notes.pkl", "rb") as f:
    notes = pickle.load(f)

pitch_names = sorted(set(notes))
note_to_int = dict((note, number) for number, note in enumerate(pitch_names))
int_to_note = dict((number, note) for note, number in note_to_int.items())

sequence_length = 100
start = np.random.randint(0, len(notes) - sequence_length)
pattern = [note_to_int[n] for n in notes[start:start + sequence_length]]

# Generate 500 notes
prediction_output = []
for _ in range(500):
    input_seq = np.reshape(pattern, (1, sequence_length, 1))
    input_seq = input_seq / float(len(pitch_names))
    prediction = model.predict(input_seq, verbose=0)
    index = np.argmax(prediction)
    result = int_to_note[index]
    prediction_output.append(result)
    pattern.append(index)
    pattern = pattern[1:]

# Convert to MIDI
output_notes = []
for pattern in prediction_output:
    if ('.' in pattern) or pattern.isdigit():
        notes_in_chord = [note.Note(int(n)) for n in pattern.split('.')]
        new_chord = chord.Chord(notes_in_chord)
        output_notes.append(new_chord)
    else:
        new_note = note.Note(pattern)
        output_notes.append(new_note)

midi_stream = stream.Stream(output_notes)
midi_stream.write('midi', fp='output/generated.mid')
print("🎵 Generated music saved as generated_song.mid")