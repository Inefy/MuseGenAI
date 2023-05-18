from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
from werkzeug.exceptions import BadRequest
import main
import os
import tempfile
import openai
import pretty_midi
import config
import logging

# Set OpenAI API key
openai.api_key = config.API_KEY

# Initialize Flask application
app = Flask(__name__)

# Enable Cross-Origin Resource Sharing with Flask-Cors
CORS(app)

# Set the logging level
logging.basicConfig(level=logging.INFO)


@app.route('/', methods=['GET'])
def home():
    return "Welcome to my Flask application!"


@app.route('/instruments', methods=['GET'])
def get_instruments():
    """
    Route for getting a list of available instruments.
    Returns a list of dictionaries, each containing an instrument id and name.
    """
    instruments = [{"id": index, "name": name}
                   for index, name in enumerate(pretty_midi.INSTRUMENT_MAP)]
    return jsonify(instruments)


@app.route('/generate-midi', methods=['POST'])
def generate_midi():
    data = request.get_json()

    if not data or 'engine' not in data or 'instruments' not in data or 'style' not in data or 'genre' not in data or 'num_notes' not in data or 'temperature' not in data:
        raise BadRequest("Invalid request data")

    logging.info(f"Generating MIDI with data: {data}")

    try:
        engine_name = {
            "gpt-4": "gpt-4",
            "gpt-3": "text-davinci-003",
            "gpt-3-turbo": "gpt-3.5-turbo",
        }.get(data['engine'].lower(), "gpt-3.5-turbo")

        notations = []
        for instrument in data['instruments']:
            prompt = f"Generate a {data['style']} {data['genre']} {instrument} song with individual notes and chords. Provide the melody in the following format: 'duration pitch1 octave1 pitch2 octave2 ...', with each note or chord on a separate line. For example: '0.5 C4 0.5 E4'."


            notation = main.generate_music_notation(
                engine_name,
                prompt,
                int(data['num_notes']),
                float(data['temperature']),
                [instrument]
            )
            notations.append(notation)

        _, temp_path = tempfile.mkstemp(suffix=".mid")

        main.notation_to_midi(notations, temp_path, data['instruments'])

    except Exception as e:
        logging.error(f"An error occurred while generating the MIDI file: {e}")
        raise e

    logging.info("MIDI file generated successfully")

    return send_file(temp_path, mimetype="audio/midi", as_attachment=True, attachment_filename="generated_music.mid")


# Run the Flask application
if __name__ == '__main__':
    app.run(debug=True)
