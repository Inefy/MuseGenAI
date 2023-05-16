import openai
import config
import pretty_midi
import fractions
import re

# Initialize OpenAI API (replace 'your_api_key' with your actual API key)
openai.api_key = config.API_KEY

def clean_instrument_name(instrument_name):
    return re.sub(r'\s*\(.*?\)', '', instrument_name)


def generate_music_notation(engine_name, prompt, num_notes, temperature, instruments):
    notations = []
    for instrument_name in instruments:
        instrument_prompt = f"{prompt} {instrument_name}:"
        notation = _generate_music_notation(engine_name, instrument_prompt, num_notes, temperature)
        notations.append(notation)
    return notations


def _generate_music_notation(engine_name, prompt, num_notes, temperature):
    notation = []
    tokens_per_request = 1000  # Adjust this value based on the maximum tokens you want to request in one call

    while len(notation) < num_notes:
        if engine_name == "gpt-3":
            response = openai.Completion.create(
                engine=engine_name,
                prompt=prompt,
                max_tokens=min(tokens_per_request, (num_notes - len(notation)) * 5),
                n=1,
                stop=None,
                temperature=temperature,
            )
            new_notation = response.choices[0].text.strip().split('\n')
        else:
            response = openai.ChatCompletion.create(
                model=engine_name,
                messages=[{"role": "system", "content": "You are a music generator AI."}, {
                    "role": "user", "content": prompt}],
                max_tokens=min(tokens_per_request, (num_notes - len(notation)) * 5),
                n=1,
                stop=None,
                temperature=temperature,
            )
            new_notation = response.choices[0]['message']['content'].strip().split('\n')

        notation.extend(new_notation)

    # Truncate the notation to the desired number of notes
    notation = notation[:num_notes]

    return notation


def notation_to_midi(notations, output_file, instrument_names):
    midi = pretty_midi.PrettyMIDI()

    for notation, instrument_name in zip(notations, instrument_names):
        cleaned_instrument_name = clean_instrument_name(instrument_name)
        instrument_program = pretty_midi.instrument_name_to_program(cleaned_instrument_name)
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
                    note_on = pretty_midi.Note(velocity=64, pitch=pitch, start=time, end=time + (4 / duration))
                    instrument.notes.append(note_on)

                time += (4 / duration)
            except ValueError:
                print(f"Skipping line: {line}")

    midi.write(output_file)
