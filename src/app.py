from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
import main
import os
import tempfile
import openai
import pretty_midi
import config

# Initialize OpenAI API (replace 'your_api_key' with your actual API key)
openai.api_key = config.API_KEY

app = Flask(__name__)
CORS(app)

@app.route('/instruments', methods=['GET'])
def get_instruments():
    instruments = [{"id": index, "name": name} for index, name in enumerate(pretty_midi.INSTRUMENT_MAP)]
    return jsonify(instruments)

@app.route('/generate-midi', methods=['POST'])
def generate_midi():
    data = request.get_json()

    engine_name = {
        "gpt-4": "gpt-4",
        "gpt-3": "text-davinci-003",
        "gpt-3-turbo": "gpt-3.5-turbo",
    }.get(data['engine'].lower(), "gpt-3.5-turbo")

    notations = []
    for instrument in data['instruments']:
        prompt = f"Generate a {data['style']} {data['genre']} {instrument} song with individual notes and chords. Provide the melody in the following format: 'duration pitch1 pitch2 ...', with each note or chord on a separate line."
        notation = main.generate_music_notation(
            engine_name,
            prompt,
            int(data['num_notes']),
            float(data['temperature'])
        )
        notations.append(notation)

    _, temp_path = tempfile.mkstemp(suffix=".mid")
    main.notation_to_midi(notations, temp_path, data['instruments'])
    
    return send_file(temp_path, mimetype="audio/midi", as_attachment=True, attachment_filename="generated_music.mid")


if __name__ == '__main__':
    app.run(debug=True)
