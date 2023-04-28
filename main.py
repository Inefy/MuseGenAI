import openai
import config
import pretty_midi
import fractions

# Initialize OpenAI API (replace 'your_api_key' with your actual API key)
openai.api_key = config.API_KEY

# Function to generate music notation using the selected GPT engine


def generate_music_notation(engine_name, prompt, num_notes, temperature):
    if engine_name == "gpt-3":
        response = openai.Completion.create(
            engine=engine_name,
            prompt=prompt,
            max_tokens=num_notes * 3,
            n=1,
            stop=None,
            temperature=temperature,
        )
        notation = response.choices[0].text.strip().split('\n')
    else:
        response = openai.ChatCompletion.create(
            model=engine_name,
            messages=[{"role": "system", "content": "You are a music generator AI."}, {
                "role": "user", "content": prompt}],
            max_tokens=num_notes * 3,
            n=1,
            stop=None,
            temperature=temperature,
        )
        notation = response.choices[0]['message']['content'].strip().split(
            '\n')

    return notation


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
            if len(split_line) < 2:
                print(f"Skipping line due to insufficient elements: {line}")
                continue

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
