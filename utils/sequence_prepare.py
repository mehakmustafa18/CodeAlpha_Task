# For creating training sequences
import numpy as np
from keras.utils import to_categorical

def prepare_sequences(notes, sequence_length):
    pitch_names = sorted(set(notes))
    note_to_int = dict((note, number) for number, note in enumerate(pitch_names))

    network_input = []
    network_output = []

    for i in range(0, len(notes) - sequence_length):
        sequence_in = notes[i:i + sequence_length]
        sequence_out = notes[i + sequence_length]
        network_input.append([note_to_int[note] for note in sequence_in])
        network_output.append(note_to_int[sequence_out])

    n_patterns = len(network_input)

    network_input = np.reshape(network_input, (n_patterns, sequence_length, 1))
    network_input = network_input / float(len(pitch_names))
    network_output = to_categorical(network_output)

    return network_input, network_output, note_to_int
