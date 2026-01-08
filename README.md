# Chord Analyzer & Player

A Python script that analyzes musical chords, detects their type (major, minor, diminished, augmented, 7th, etc.), identifies the root note and inversion, and plays the chord using sine waves.

## Features

- Input chords as text (e.g., `C E G` or `Bb D F`)
- Detects chord type, root note, and inversion
- Continuously interactive: keeps asking for chords until you type `exit`
- Plays each chord in real time using sine wave synthesis
- Perfect for music students or hobbyists learning music theory

## Usage

1. Make sure you have Python 3 installed.
2. Install dependencies:

```bash
pip install numpy sounddevice
