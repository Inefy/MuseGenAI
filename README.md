# MuseGenAI

MuseGenAI is a Music Generator powered by GPT-4 and GPT-3-turbo from OpenAI. This application is designed to create a MIDI file based on a chosen musical style, genre, instruments, the number of notes, and the creativity level defined by the temperature parameter. 

## Features

- Selection of AI engine: GPT-4 and GPT-3 Turbo.
- Input of musical style, genre, and the number of notes to be generated.
- Multi-selection of instruments from a comprehensive list.
- Adjustable creativity level via the temperature slider.
- Generation of a MIDI file, which can be downloaded and played in the application.

## Setup and Installation

1. Clone the repository:

   ```
   git clone https://github.com/your-repo/musegenai.git
   cd musegenai
   ```

2. Install the required Python libraries:

   ```
   pip install -r requirements.txt
   ```

3. Install Node.js dependencies:

   ```
   cd client
   npm install
   ```

4. Create a `.env` file in the root directory and fill in your OpenAI API key:

   ```
   API_KEY=<Your OpenAI API Key>
   ```

## Running the application

1. Start the Flask backend:

   ```
   python app.py
   ```

2. In another terminal, navigate to the `client` folder and start the React frontend:

   ```
   npm start
   ```

The application should now be running on `localhost:3000`.

## Usage

1. Select the AI engine you want to use.
2. Enter the desired musical style and genre.
3. Select the instruments you want to include.
4. Input the number of notes to be generated.
5. Adjust the creativity level using the temperature slider.
6. Click on 'Generate MIDI' to create the MIDI file.
7. Once the MIDI file is generated, you can download it and it will also be played automatically in the application.


## License

This project is licensed under the MIT License. See the [LICENSE.md](LICENSE.md) file for details.

