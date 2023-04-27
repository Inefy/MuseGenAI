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
        max_tokens=num_notes * 5,
        n=1,
        stop=None,
        temperature=temperature,
    )

    return response.choices[0].text.strip().split('\n')

# Function to convert music notation to MIDI
def notation_to_midi(notation, output_file, tempo):
    midi = pretty_midi.PrettyMIDI()
    piano_program = pretty_midi.instrument_name_to_program('Acoustic Grand Piano')
    piano = pretty_midi.Instrument(program=piano_program)
    midi.instruments.append(piano)
    midi.adjust_times([0], [60 / tempo])

    time = 0
    for line in notation:
        try:
            duration, pitch = line.split()
            duration = round(4 * float(fractions.Fraction(duration)))
            note = pretty_midi.note_name_to_number(pitch)

            note_on = pretty_midi.Note(velocity=64, pitch=note, start=time, end=time + (4 / duration))
            piano.notes.append(note_on)

            time += (4 / duration)
        except ValueError:
            print(f"Skipping line: {line}")

    midi.write(output_file)

# User input for parameters
engine_choice = input("Choose the GPT engine (gpt-4, gpt-3, gpt-3-turbo): ")
style = input("Enter the desired style (e.g., classical, jazz, pop): ")
genre = input("Enter the desired genre (e.g., upbeat, melancholic, energetic): ")
key = input("Enter the desired key (e.g., C major, A minor): ")
num_notes = int(input("Enter the number of notes in the melody: "))
temperature = float(input("Enter the creativity level (0.1-1.0, higher is more creative): "))
tempo = int(input("Enter the desired tempo in BPM: "))

# Set engine name based on user input
engine_name = {
    "gpt-4": "gpt-4",
    "gpt-3": "text-davinci-003",
    "gpt-3-turbo": "gpt-3.5-turbo",
}.get(engine_choice.lower(), "gpt-3.5-turbo")  # Default to GPT-3 Turbo (gpt-3.5-turbo) if input is not recognized

# Generate music notation
prompt = f"Generate a {style} {genre} piano melody with individual notes in the key of {key} at {tempo} BPM. Provide the melody in the following format: 'duration pitch', with each note on a separate line."
notation = generate_music_notation(engine_name, prompt, num_notes, temperature)

# Convert music notation to MIDI
output_file = 'output.mid'
notation_to_midi(notation, output_file, tempo)
print(f"MIDI file generated: {output_file}")
