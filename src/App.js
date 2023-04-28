import React, { useState } from "react";
import "./App.css";
import axios from "axios";

function App() {
  const [engine, setEngine] = useState("gpt-3");
  const [style, setStyle] = useState("");
  const [genre, setGenre] = useState("");
  const [instrument, setInstrument] = useState("Acoustic Grand Piano");
  const [numNotes, setNumNotes] = useState("");
  const [temperature, setTemperature] = useState(0.5);

  const generateMidi = async () => {
    // Replace this URL with the API endpoint of your Python backend
    const apiUrl = "http://localhost:5000/generate-midi";

    const response = await axios.post(apiUrl, {
      engine,
      style,
      genre,
      instrument,
      num_notes: numNotes,
      temperature,
    });

    // Download the MIDI file
    const blob = new Blob([response.data], { type: "audio/midi" });
    const url = window.URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = url;
    link.setAttribute("download", "generated_music.mid");
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  return (
    <div className="App">
      <h1>Music Generator</h1>
      <div>
        <label>Engine:</label>
        <select value={engine} onChange={(e) => setEngine(e.target.value)}>
          <option value="gpt-4">GPT-4</option>
          <option value="gpt-3">GPT-3</option>
          <option value="gpt-3-turbo">GPT-3 Turbo</option>
        </select>
      </div>
      <div>
        <label>Style:</label>
        <input value={style} onChange={(e) => setStyle(e.target.value)} />
      </div>
      <div>
        <label>Genre:</label>
        <input value={genre} onChange={(e) => setGenre(e.target.value)} />
      </div>
      <div>
        <label>Instrument:</label>
        <input
          value={instrument}
          onChange={(e) => setInstrument(e.target.value)}
        />
      </div>
      <div>
        <label>Number of notes:</label>
        <input
          value={numNotes}
          onChange={(e) => setNumNotes(e.target.value)}
          type="number"
        />
      </div>
      <div>
        <label>Creativity level:</label>
        <input
          value={temperature}
          onChange={(e) => setTemperature(e.target.value)}
          type="range"
          min="0.1"
          max="1"
          step="0.1"
        />
      </div>
      <button onClick={generateMidi}>Generate MIDI</button>
    </div>
  );
}

export default App;
