# Music Generator

A user-friendly application that generates MIDI files using the GPT-4 engine, GPT-3 engine, or GPT-3 Turbo engine from OpenAI. Users can input their preferred music style, genre, and instrument to generate unique melodies.

## Features

- Simple graphical user interface for user input
- Generates music notations using GPT engines from OpenAI
- Converts generated music notations into MIDI files
- Allows users to choose from a variety of music styles, genres, and instruments

## Installation

1. Install the required packages:

```bash
pip install openai pretty_midi
```

2. Edit the `configTemplate.py` file in the same directory as the scripts, and add your OpenAI API key:

```python
API_KEY = "your_api_key_here"
```
Rename the file to `config.py`

3. Run the `ui.py` script:

```bash
python ui.py
```

## Usage

1. Launch the application by running the `ui.py` script.
2. Choose the desired GPT engine from the "Engine" dropdown menu.
3. Enter the desired music style (e.g., classical, jazz, pop) in the "Style" field.
4. Enter the desired genre (e.g., upbeat, melancholic, energetic) in the "Genre" field.
5. Choose the desired instrument from the "Instrument" dropdown menu.
6. Enter the number of notes in the melody in the "Number of notes" field.
7. Enter the creativity level (0.1-1.0, higher is more creative) in the "Creativity level" field.
8. Click the "Generate MIDI" button.
9. Choose a location to save the generated MIDI file.

## License

This project is released under the MIT License. See `LICENSE` for more details.