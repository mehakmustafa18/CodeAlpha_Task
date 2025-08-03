from music21 import converter

# Load and play the MIDI file using music21
midi = converter.parse("output/generated.mid")
midi.show('midi')  
