 # Script to train the LSTM model
from keras.models import Sequential
from keras.layers import LSTM, Dropout, Dense, Activation
from utils.midi_processor import extract_notes_from_midi
from utils.sequence_prepare import prepare_sequences
import pickle
import os
from keras.models import load_model

# Step 1: Extract notes
notes = extract_notes_from_midi("data/midi/")
print(f"Extracted {len(notes)} notes")
# Save notes for later generation
with open("data/notes.pkl", "wb") as f:
    pickle.dump(notes, f)

# Step 2: Prepare sequences
sequence_length = 100
network_input, network_output, note_to_int = prepare_sequences(notes, sequence_length)

# Step 3: Build model
model_path = "models/model.h5"
if os.path.exists(model_path):
    model = load_model(model_path)
    print("✅ Loaded previously trained model.")
else:

     model = Sequential()
     model.add(LSTM(512, input_shape=(network_input.shape[1], 1), return_sequences=True))
     model.add(Dropout(0.3))
     model.add(LSTM(512))
     model.add(Dense(256))
     model.add(Dropout(0.3))
     model.add(Dense(len(note_to_int)))
     model.add(Activation('softmax'))
     model.compile(loss='categorical_crossentropy', optimizer='adam')
     model.fit(network_input, network_output, epochs=100, batch_size=64)
     model.save("models/model.h5")
     print("✅ Model saved as music_model.h5")

