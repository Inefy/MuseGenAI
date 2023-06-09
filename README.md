# MuseGenAI

MuseGenAI is a Music Generator powered by OpenAI's GPT-4, GPT-3, and GPT-3-turbo. This application generates a MIDI file based on the user's chosen musical style, genre, instrument(s), and number of notes. The creativity level of the generated music is adjustable via the temperature parameter.

## Features

- Selection between AI engines: GPT-4, GPT-3, and GPT-3 Turbo.
- User-defined musical style, genre, and the number of notes to be generated.
- Multi-selection of instruments from a comprehensive list.
- Adjustable creativity level via the temperature slider.
- Generation and automatic download of a MIDI file, which can also be played within the application.

## How it works

On the frontend, the React.js application serves as the user interface for our music generator. Users can input their choices and these selections are sent to the backend.

The backend is a Flask application that communicates with the OpenAI API. Depending on the user's choice, the application uses either the Completion or ChatCompletion endpoints of the API to generate music notation. These notations are then converted to MIDI format using the Pretty MIDI library and sent back to the frontend to be downloaded by the user.

The primary entry point for the backend is `main.py`, while the frontend starts at `index.js`.

## Setup and Installation

Clone the repository:
```
git clone https://github.com/your-repo/musegenai.git
cd musegenai
```
Install the required Python libraries:
```
pip install -r requirements.txt
```
Install Node.js dependencies:
```
cd client
npm install
```
Create a .env file in the root directory and fill in your OpenAI API key:
```
API_KEY=<Your OpenAI API Key>
```
## Running the application

Start the Flask backend:
```
python app.py
```
In another terminal, navigate to the client folder and start the React frontend:
```
npm start
```
The application should now be running on localhost:3000.

## Usage

1. Select the AI engine you want to use (GPT-4, GPT-3, or GPT-3 Turbo).
2. Enter the desired musical style and genre.
3. Select the instruments you want to include.
4. Input the number of notes to be generated.
5. Adjust the creativity level using the temperature slider.
6. Click on 'Generate MIDI' to create the MIDI file.
7. Once the MIDI file is generated, it will automatically download, and can be played directly in the application.

## License

This project is licensed under the MIT License. See the LICENSE.md file for details.
