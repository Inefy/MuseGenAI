import React, { useState, useEffect } from "react";
import "./App.css";
import axios from "axios";
import { Container, Box, Typography, TextField, Select, MenuItem, FormControl, InputLabel, Slider, Button } from "@mui/material";
import { createTheme, ThemeProvider } from "@mui/material/styles";
import styled from "@emotion/styled";

const theme = createTheme({
  palette: {
    primary: {
      main: "#3f51b5",
    },
    secondary: {
      main: "#f44336",
    },
  },
});

const AppContainer = styled(Container)`
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100vh;
  background-color: #f5f5f5;
`;

const TitleTypography = styled(Typography)`
  color: #3f51b5;
  font-weight: bold;
  margin-bottom: 1rem;
`;

function App() {
  const [engine, setEngine] = useState("gpt-3");
  const [style, setStyle] = useState("");
  const [genre, setGenre] = useState("");
  const [instrument, setInstrument] = useState("Acoustic Grand Piano");
  const [numNotes, setNumNotes] = useState("");
  const [temperature, setTemperature] = useState(0.5);

  const [instrumentsList, setInstrumentsList] = useState([]);

  useEffect(() => {
    const fetchInstruments = async () => {
      // Replace this URL with the API endpoint of your Python backend
      const apiUrl = "http://localhost:5000/instruments";
      const response = await axios.get(apiUrl);
      setInstrumentsList(response.data);
    };

    fetchInstruments();
  }, []);

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
    <ThemeProvider theme={theme}>
      <AppContainer maxWidth="sm">
        <TitleTypography variant="h2" gutterBottom>
          Music Generator
        </TitleTypography>
        <Box width="100%" mb={3}>
          <FormControl fullWidth>
            <Select value={engine} onChange={(e) => setEngine(e.target.value)}>
              <MenuItem value="gpt-4">GPT-4</MenuItem>
              <MenuItem value="gpt-3">GPT-3</MenuItem>
              <MenuItem value="gpt-3-turbo">GPT-3 Turbo</MenuItem>
            </Select>
          </FormControl>
        </Box>
        <Box width="100%" mb={3}>
          <TextField fullWidth label="Style" value={style} onChange={(e) => setStyle(e.target.value)} />
        </Box>
        <Box width="100%" mb={3}>
          <TextField fullWidth label="Genre" value={genre} onChange={(e) => setGenre(e.target.value)} />
        </Box>
        <Box width="100%" mb={3}>
          <FormControl fullWidth>
            <InputLabel>Instrument</InputLabel>
            <Select value={instrument} onChange={(e) => setInstrument(e.target.value)}>
              {instrumentsList.map((instr) => (
                <MenuItem key={instr.id} value={instr.name}>
                  {instr.name}
                </MenuItem>
              ))}
            </Select>
          </FormControl>
        </Box>
        <Box width="100%" mb={3}>
          <TextField fullWidth label="Number of notes" type="number" value={numNotes} onChange={(e) => setNumNotes(e.target.value)} />
        </Box>
        <Box width="100%" mb={3}>
          <Typography id="temperature-slider" gutterBottom>
            Creativity level
          </Typography>
          <Slider
            value={temperature}
            onChange={(e, value) => setTemperature(value)}
            step={0.1}
            min={0.1}
            max={1}
            valueLabelDisplay="auto"
            aria-labelledby="temperature-slider"
          />
        </Box>
        <Box width="100%" mb={3}>
          <Button variant="contained" color="primary" onClick={generateMidi}>
            Generate MIDI
          </Button>
        </Box>
      </AppContainer>
    </ThemeProvider>
  );

}

export default App;
