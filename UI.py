import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import main

def generate_midi():
    engine_choice = engine_combo.get()
    style = style_entry.get()
    genre = genre_entry.get()
    num_notes = int(notes_entry.get())
    temperature = float(temperature_entry.get())

    engine_name = {
        "gpt-4": "gpt-4",
        "gpt-3": "text-davinci-003",
        "gpt-3-turbo": "gpt-3.5-turbo",
    }.get(engine_choice.lower(), "gpt-3.5-turbo")

    prompt = f"Generate a {style} {genre} piano song with individual notes and chords. Provide the melody in the following format: 'duration pitch1 pitch2 ...', with each note or chord on a separate line."

    notation = generate_music_notation(engine_name, prompt, num_notes, temperature)
    output_file = filedialog.asksaveasfilename(defaultextension=".mid")
    notation_to_midi(notation, output_file)
    print(f"MIDI file generated: {output_file}")

# Create the main window
root = tk.Tk()
root.title("Music Generator")

# Create and place UI elements
ttk.Label(root, text="Engine:").grid(column=0, row=0, sticky=tk.W)
engine_combo = ttk.Combobox(root, values=["gpt-4", "gpt-3", "gpt-3-turbo"])
engine_combo.set("gpt-3-turbo")
engine_combo.grid(column=1, row=0)

ttk.Label(root, text="Style:").grid(column=0, row=1, sticky=tk.W)
style_entry = ttk.Entry(root)
style_entry.grid(column=1, row=1)

ttk.Label(root, text="Genre:").grid(column=0, row=2, sticky=tk.W)
genre_entry = ttk.Entry(root)
genre_entry.grid(column=1, row=2)

ttk.Label(root, text="Number of notes:").grid(column=0, row=3, sticky=tk.W)
notes_entry = ttk.Entry(root)
notes_entry.grid(column=1, row=3)

ttk.Label(root, text="Creativity level:").grid(column=0, row=4, sticky=tk.W)
temperature_entry = ttk.Entry(root)
temperature_entry.grid(column=1, row=4)

generate_button = ttk.Button(root, text="Generate MIDI", command=generate_midi)
generate_button.grid(column=1, row=5)

# Run the main loop
root.mainloop()
