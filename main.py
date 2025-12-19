import numpy as np
import simpleaudio as sa

SAMPLE_RATE = 44100

NOTE_TO_SEMITONE = {
    'C':0, 'C#':1, 'Db':1, 'D':2, 'D#':3, 'Eb':3, 'E':4, 'F':5,
    'F#':6, 'Gb':6, 'G':7, 'G#':8, 'Ab':8, 'A':9, 'A#':10, 'Bb':10, 'B':11
}

CHORD_PATTERNS = {
    'major': [0,4,7],
    'minor': [0,3,7],
    'diminished': [0,3,6],
    'augmented': [0,4,8],
    'dominant7': [0,4,7,10],
    'major7': [0,4,7,11],
    'minor7': [0,3,7,10],
    'dim7': [0,3,6,9]
}

def note_to_semitone(note):
    note = note.strip()
    if note[-1].isdigit():
        note = note[:-1]
    if note not in NOTE_TO_SEMITONE:
        raise ValueError(f"Invalid note: {note}")
    return NOTE_TO_SEMITONE[note]

def normalize_notes(notes):
    semitones = [note_to_semitone(n) % 12 for n in notes]
    semitones = sorted(list(set(semitones)))
    return semitones

def detect_chord(notes):
    semis = normalize_notes(notes)
    for chord_name, pattern in CHORD_PATTERNS.items():
        for root in semis:
            shifted = sorted([(s - root) % 12 for s in semis])
            if shifted == pattern:
                inversion = semis.index(root)
                return chord_name, root, inversion
    return "unknown", semis[0], 0

def semitone_to_note(semi):
    for k,v in NOTE_TO_SEMITONE.items():
        if v == semi:
            return k
    return '?'

def generate_sine(frequency, duration, amplitude=0.3):
    t = np.linspace(0, duration, int(SAMPLE_RATE*duration), False)
    return amplitude * np.sin(2*np.pi*frequency*t)

def play_chord(notes, duration=1.0, amplitude=0.3):
    waves = []
    for n in notes:
        semitone = NOTE_TO_SEMITONE[n]
        freq = 440.0 * 2**((semitone - 9)/12)
        waves.append(generate_sine(freq, duration, amplitude))
    mix = np.sum(waves, axis=0)
    mix /= np.max(np.abs(mix))
    audio = (mix * 32767).astype(np.int16)
    sa.play_buffer(audio, 1, 2, SAMPLE_RATE).wait_done()

if __name__=="__main__":
    print("Chord Analyzer & Player (type 'exit' to quit)")
    while True:
        user_input = input("Enter chord notes separated by space (e.g., C E G): ").strip()
        if user_input.lower() in ('exit','quit'):
            print("Goodbye!")
            break
        notes = user_input.split()
        try:
            chord_type, root_semi, inversion = detect_chord(notes)
            root_note = semitone_to_note(root_semi)
            inv_text = 'root position' if inversion==0 else f"{inversion+1} inversion"
            print(f"Chord type: {chord_type}")
            print(f"Root: {root_note}")
            print(f"Inversion: {inv_text}")
            print("Playing chord...")
            play_chord(notes)
        except Exception as e:
            print(f"Error: {e}")
            print("Please enter valid notes (e.g., C E G).")
