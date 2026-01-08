from main import play_chord, detect_chord, semitone_to_note
import time

PROGRESSIONS = {
    "I-IV-V (C Major)": [
        ["C4", "E4", "G4"],
        ["F4", "A4", "C5"],
        ["G4", "B4", "D5"],
    ],
    "ii-V-I (Jazz in C)": [
        ["D4", "F4", "A4"],
        ["G4", "B4", "D5", "F5"],
        ["C4", "E4", "G4", "B4"],
    ],
    "vi-IV-I-V (Pop progression)": [
        ["A3", "C4", "E4"],
        ["F3", "A3", "C4"],
        ["C4", "E4", "G4"],
        ["G3", "B3", "D4"],
    ],
    "I-vi-IV-V (50s progression)": [
        ["C4", "E4", "G4"],
        ["A3", "C4", "E4"],
        ["F3", "A3", "C4"],
        ["G3", "B3", "D4"],
    ],
}

def play_progression(name, chords, delay=1.5):
    print(f"\n{'='*50}")
    print(f"Playing: {name}")
    print(f"{'='*50}")
    
    for i, chord_notes in enumerate(chords, 1):
        chord_type, root, inversion = detect_chord(chord_notes)
        root_note = semitone_to_note(root)
        
        print(f"\nChord {i}: {' '.join(chord_notes)}")
        print(f"  Type: {chord_type}")
        print(f"  Root: {root_note}")
        
        play_chord(chord_notes, duration=1.5)
        time.sleep(delay)

def main():
    print("Chord Progression Examples")
    print("="*50)
    print("\nAvailable progressions:")
    for i, name in enumerate(PROGRESSIONS.keys(), 1):
        print(f"{i}. {name}")
    
    print("\nOptions:")
    print("  - Enter a number to play that progression")
    print("  - Enter 'all' to play all progressions")
    print("  - Enter 'exit' to quit")
    
    while True:
        choice = input("\nYour choice: ").strip().lower()
        
        if choice in ('exit', 'quit', 'q'):
            print("Goodbye!")
            break
        
        if choice == 'all':
            for name, chords in PROGRESSIONS.items():
                play_progression(name, chords)
                time.sleep(2)
        elif choice.isdigit():
            idx = int(choice) - 1
            names = list(PROGRESSIONS.keys())
            if 0 <= idx < len(names):
                name = names[idx]
                play_progression(name, PROGRESSIONS[name])
            else:
                print("Invalid number. Try again.")
        else:
            print("Invalid input. Enter a number, 'all', or 'exit'.")

if __name__ == "__main__":
    main()
