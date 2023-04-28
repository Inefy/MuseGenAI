import openai
import config
import pretty_midi
import fractions

# Initialize OpenAI API (replace 'your_api_key' with your actual API key)
openai.api_key = config.API_KEY

# Function to generate music notation using the selected GPT engine
def generate_music_notation(engine_name, prompt, num_notes, temperature):
    response = openai.Completion.create(
        engine=engine_name,
        prompt=prompt,
        max_tokens=num_notes * 3,
        n=1,
        stop=None,
        temperature=temperature,
    )

    return response.choices[0].text.strip().split('\n')

# Function to convert music notation to MIDI
def notation_to_midi(notation, output_file, instrument_name):
    midi = pretty_midi.PrettyMIDI()
    instrument_program = pretty_midi.instrument_name_to_program(instrument_name)
    instrument = pretty_midi.Instrument(program=instrument_program)
    midi.instruments.append(instrument)

    time = 0
    for line in notation:
        try:
            split_line = line.split()
            duration = round(4 * float(fractions.Fraction(split_line[0])))
            if duration == 0:
                print(f"Skipping line due to zero duration: {line}")
                continue

            pitches = [pretty_midi.note_name_to_number(pitch) for pitch in split_line[1:]]

            for pitch in pitches:
                note_on = pretty_midi.Note(velocity=64, pitch=pitch, start=time, end=time + (1 / duration))
                instrument.notes.append(note_on)

            time += (1 / duration)
        except ValueError:
            print(f"Skipping line: {line}")

    midi.write(output_file)

# User input for parameters
engine_choice = input("Choose the GPT engine (gpt-4, gpt-3, gpt-3-turbo): ")
style = input("Enter the desired style (e.g., classical, jazz, pop): ")
genre = input("Enter the desired genre (e.g., upbeat, melancholic, energetic): ")
instrument_name = input("Enter the desired instrument (e.g., Acoustic Grand Piano, Violin, Flute): ")
num_notes = int(input("Enter the number of notes in the melody: "))
temperature = float(input("Enter the creativity level (0.1-1.0, higher is more creative): "))
output_file = input("Enter the desired output filename (e.g., my_song.mid): ")

# Set engine name based on user input
engine_name = {
    "gpt-4": "gpt-4",
    "gpt-3": "text-davinci-003",
    "gpt-3-turbo": "gpt-3.5-turbo",
}.get(engine_choice.lower(), "gpt-3.5-turbo")  # Default to GPT-3 Turbo (gpt-3.5-turbo) if input is not recognized

# Generate music notation
prompt = f"Generate a {style} {genre} {instrument_name} song with individual notes and chords. Provide the melody in the following format: 'duration pitch1 pitch2 ...', with each note or chord on a separate line."

notation = generate_music_notation(engine_name, prompt, num_notes, temperature)

# Convert music notation to MIDI
notation_to_midi(notation, output_file, instrument_name)
print(f"MIDI file generated: {output_file}")
