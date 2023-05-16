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

@app.route('/instruments', methods=['GET'])
def get_instruments():
    """
    Route for getting a list of available instruments.
    Returns a list of dictionaries, each containing an instrument id and name.
    """
    instruments = [{"id": index, "name": name} for index, name in enumerate(pretty_midi.INSTRUMENT_MAP)]
    return jsonify(instruments)

@app.route('/generate-midi', methods=['POST'])
def generate_midi():
    """
    Route for generating a MIDI file based on the provided parameters.
    Requires a JSON payload with engine, style, genre, num_notes, temperature, and instruments.
    Returns a MIDI file generated based on the provided parameters.
    """
    # Extract JSON data from the request
    data = request.get_json()

    # Validate input data, raise BadRequest exception if validation fails
    if not data or 'engine' not in data or 'instruments' not in data or 'style' not in data or 'genre' not in data or 'num_notes' not in data or 'temperature' not in data:
        raise BadRequest("Invalid request data")

    # Log the incoming request data
    logging.info(f"Generating MIDI with data: {data}")

    try:
        # Map the engine name to the one used by OpenAI API
        engine_name = {
            "gpt-4": "gpt-4",
            "gpt-3": "text-davinci-003",
            "gpt-3-turbo": "gpt-3.5-turbo",
        }.get(data['engine'].lower(), "gpt-3.5-turbo")

        notations = []
        for instrument in data['instruments']:
            # Prepare the prompt for the AI
            prompt = f"Generate a {data['style']} {data['genre']} {instrument} song with individual notes and chords. Provide the melody in the following format: 'duration pitch1 pitch2 ...', with each note or chord on a separate line."
            
            # Call main.generate_music_notation() to generate music notation using AI
            notation = main.generate_music_notation(
                engine_name,
                prompt,
                int(data['num_notes']),
                float(data['temperature'])
            )
            notations.append(notation)

        # Create a temporary file to store the generated MIDI
        _, temp_path = tempfile.mkstemp(suffix=".mid")

        # Convert the generated notations to a MIDI file
        main.notation_to_midi(notations, temp_path, data['instruments'])
        
    except Exception as e:
        # Log the error and re-raise the exception
        logging.error(f"An error occurred while generating the MIDI file: {e}")
        raise e

    # Log the successful generation of the MIDI file
    logging.info("MIDI file generated successfully")

    # Return the generated MIDI file
    return send_file(temp_path, mimetype="audio/midi", as_attachment=True, attachment_filename="generated_music.mid")


# Run the Flask application
if __name__ == '__main__':
    app.run(debug=True)

