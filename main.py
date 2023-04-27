import openai
import mido
from mido import Message, MidiFile, MidiTrack

# Initialize OpenAI API (replace 'your_api_key' with your actual API key)
openai.api_key = 'your_api_key'

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
def notation_to_midi(notation, output_file):
    midi = MidiFile()
    track = MidiTrack()
    midi.tracks.append(track)

    for line in notation:
        duration, pitch = line.split()
        duration = int(duration)
        note = mido.note_name_to_number(pitch)

        track.append(Message('note_on', note=note, velocity=64, time=0))
        track.append(Message('note_off', note=note, velocity=64, time=int(480 * (4 / duration))))

    midi.save(output_file)

# User input for parameters
engine_choice = input("Choose the GPT engine (gpt-4, gpt-3, gpt-3-turbo): ")
style = input("Enter the desired style (e.g., classical, jazz, pop): ")
genre = input("Enter the desired genre (e.g., upbeat, melancholic, energetic): ")
key = input("Enter the desired key (e.g., C major, A minor): ")
num_notes = int(input("Enter the number of notes in the melody: "))
temperature = float(input("Enter the creativity level (0.1-1.0, higher is more creative): "))

# Set engine name based on user input
engine_name = {
    "gpt-4": "text-davinci-002",
    "gpt-3": "davinci",
    "gpt-3-turbo": "davinci-codex",
}.get(engine_choice.lower(), "text-davinci-002")  # Default to GPT-4 if input is not recognized

# Generate music notation
prompt = f"Generate a {style} {genre} piano melody in the key of {key}:"
notation = generate_music_notation(engine_name, prompt, num_notes, temperature)

# Convert music notation to MIDI
output_file = 'output.mid'
notation_to_midi(notation, output_file)
print(f"MIDI file generated: {output_file}")
