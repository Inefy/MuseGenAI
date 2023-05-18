import config
import pretty_midi
import fractions
import openai
import re
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize OpenAI API with a configurable API key
openai.api_key = config.API_KEY

def clean_instrument_name(instrument_name):
    """
    Clean instrument name by removing content within parentheses.
    """
    return re.sub(r'\s*\(.*?\)', '', instrument_name)

def generate_music_notation(engine_name, prompt, num_notes, temperature, instruments):
    """
    Generate music notation for the given set of instruments.
    """
    if not instruments:
        raise ValueError("Instruments cannot be empty")

    notations = []
    for instrument_name in instruments:
        instrument_prompt = f"{prompt} {instrument_name}:"
        notation = _generate_music_notation(
            engine_name, instrument_prompt, num_notes, temperature)
        notations.append(notation)
    return notations

def _generate_music_notation(engine_name, prompt, num_notes, temperature):
    """
    Generate music notation using the OpenAI API.
    """
    notation = []
    # Adjust this value based on the maximum tokens you want to request in one call
    tokens_per_request = 1000

    while len(notation) < num_notes:
        try:
            if engine_name == "gpt-3":
                response = openai.Completion.create(
                    engine=engine_name,
                    prompt=prompt,
                    max_tokens=min(tokens_per_request,
                                   (num_notes - len(notation)) * 5),
                    n=1,
                    stop=None,
                    temperature=temperature,
                )
                new_notation = response.choices[0].text.strip().split('\n')
            else:
                response = openai.ChatCompletion.create(
                    model=engine_name,
                    messages=[{"role": "system", "content": "You are a music generator AI."},
                              {"role": "user", "content": prompt}],
                    max_tokens=min(tokens_per_request,
                                   (num_notes - len(notation)) * 5),
                    n=1,
                    stop=None,
                    temperature=temperature,
                )
                new_notation = response.choices[0]['message']['content'].strip().split('\n')

            notation.extend(new_notation)

        except Exception as e:
            logging.error(
                f"An error occurred while generating music notation: {e}")
            raise e

    # Truncate the notation to the desired number of notes
    notation = notation[:num_notes]

    return notation

def notation_to_midi(notations, output_file, instrument_names):
    """
    Convert the generated music notation into a MIDI file.
    """
    midi = pretty_midi.PrettyMIDI()

    for notation, instrument_name in zip(notations, instrument_names):
        cleaned_instrument_name = clean_instrument_name(instrument_name)
        instrument_program = pretty_midi.instrument_name_to_program(
            cleaned_instrument_name)
        instrument = pretty_midi.Instrument(program=instrument_program)
        midi.instruments.append(instrument)

        time = 0
        for sub_notation in notation:
            for line in sub_notation:
                try:
                    split_line = line.split()
                    if len(split_line) < 2:
                        logging.warning(
                            f"Skipping line due to insufficient elements: {line}")
                        continue

                    try:
                        duration = round(4 * float(fractions.Fraction(split_line[0])))
                    except ValueError:
                        logging.warning(f"Skipping line due to non-numeric duration: {line}")
                        continue

                    if duration == 0:
                        logging.warning(
                            f"Skipping line due to zero duration: {line}")
                        continue

                    pitches = [pretty_midi.note_name_to_number(
                        pitch) for pitch in split_line[1:]]

                    for pitch in pitches:
                        note_on = pretty_midi.Note(
                            velocity=100, pitch=pitch, start=time, end=time + duration)
                        instrument.notes.append(note_on)

                    time += duration

                except Exception as e:
                    logging.error(
                        f"An error occurred while converting notation to MIDI: {e}")
                    raise e

    try:
        midi.write(output_file)
    except Exception as e:
        logging.error(f"An error occurred while writing the MIDI file: {e}")
        raise e
