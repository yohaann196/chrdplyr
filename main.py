import numpy as np
import simpleaudio as sa
from constants import SAMPLE_RATE, NOTE_TO_SEMITONE, CHORD_PATTERNS

def note_to_semitone(note):
    note = note.strip()
    octave = 4
    if len(note) > 1 and note[-1].isdigit():
        octave = int(note[-1])
        note = note[:-1]
    if note not in NOTE_TO_SEMITONE:
        raise ValueError(f"Invalid note: {note}")
    return NOTE_TO_SEMITONE[note] + 12 * octave

def normalize_notes(notes):
    semitones = [note_to_semitone(n) % 12 for n in notes]
    return sorted(set(semitones))

def detect_chord(notes):
    semis = normalize_notes(notes)
    original = [note_to_semitone(n) % 12 for n in notes]

    for chord_name, pattern in CHORD_PATTERNS.items():
        for root in semis:
            shifted = sorted((s - root) % 12 for s in semis)
            if shifted == pattern:
                inversion = original.index(root)
                return chord_name, root, inversion

    return "unknown", semis[0], 0

SEMITONE_TO_NOTE = {
    v: k for k, v in NOTE_TO_SEMITONE.items()
    if '#' in k or len(k) == 1
}

def semitone_to_note(semi):
    return SEMITONE_TO_NOTE.get(semi % 12, '?')

def generate_sine(frequency, duration=1.0, amplitude=0.3):
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration), False)
    return amplitude * np.sin(2 * np.pi * frequency * t)

def play_chord(notes, duration=1.0, amplitude=0.3):
    waves = []

    for n in notes:
        semi_abs = note_to_semitone(n)
        octave = semi_abs // 12
        semi = semi_abs % 12
        freq = 440.0 * 2 ** ((semi - 9) / 12 + (octave - 4))
        waves.append(generate_sine(freq, duration, amplitude))

    mix = np.sum(waves, axis=0)
    mix /= max(abs(mix))
    audio = (mix * 32767).astype(np.int16)
    sa.play_buffer(audio, 1, 2, SAMPLE_RATE).wait_done()

if __name__ == "__main__":
    print("Chord Analyzer & Player (type 'exit' to quit)")
    while True:
        user_input = input("Enter chord notes separated by space: ").strip()
        if user_input.lower() in ("exit", "quit"):
            print("Goodbye!")
            break

        notes = user_input.split()
        chord, root, inversion = detect_chord(notes)
        root_note = semitone_to_note(root)
        inv_text = "root position" if inversion == 0 else f"{inversion + 1} inversion"

        print(f"Chord type: {chord}")
        print(f"Root: {root_note}")
        print(f"Inversion: {inv_text}")
        play_chord(notes)
