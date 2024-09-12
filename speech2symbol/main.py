
import pyaudio
import tkinter as tk
from tkinter import ttk, simpledialog, filedialog, scrolledtext
import speech_recognition as sr
from symbols import get as get_symbols
import winsound
import math
import re

# Global variables
TITLE_OF_PROJECT = "Speech To Math Converter"
SAVED_TEXT_FILE = r"./saved_text.txt"
ICON_PATH = "./assets/favicon.ico"

FONT = ("Arial", 12)
BUTTON_FONT = ("Arial", 14, "bold")

ENERGY_THRESHOLD = 1000
SAMPLE_RATE = 44100
CHUNK_SIZE = 512

# Define available languages
LANGUAGES = {
    "English": "en-IN",
    "Hindi": "hi-IN",
    "Spanish": "es-ES",
    "French": "fr-FR",
    "German": "de-DE",
    "Kannada": "kn-IN"
}

current_language = "English"
speaker_output = ""
symbols = get_symbols()

def replace_symbol(txt):
    words = txt.split()
    return ' '.join(symbols.get(word.lower(), word) for word in words)

def audio_feedback(success=True):
    if success:
        winsound.Beep(1000, 100)  # 1000 Hz for 100 milliseconds
    else:
        winsound.Beep(500, 300)   # 500 Hz for 300 milliseconds

def speech_to_text():
    global speaker_output
    r = sr.Recognizer()
    r.energy_threshold = ENERGY_THRESHOLD
    #codeium
    r.pause_threshold = 0.5
    r.non_speaking_duration = 0.5

    with sr.Microphone(sample_rate=SAMPLE_RATE, chunk_size=CHUNK_SIZE) as source:
        r.adjust_for_ambient_noise(source)
        print('Say Something!')
        audio = r.listen(source)
        try:
            text = r.recognize_google(audio, language=LANGUAGES[current_language])
            text = replace_symbol(text)
            print('You said: {}'.format(text))
            speaker_output += '\n' + text
            with open(SAVED_TEXT_FILE, "a+", encoding="utf-8") as file:
                file.write(text + '\n')
            update_display()
            audio_feedback(True)
            return text
        except sr.UnknownValueError:
            print("Speech is unintelligible")
            audio_feedback(False)
            return None
        except sr.RequestError:
            print("Could not request results from Google Speech Recognition service")
            audio_feedback(False)
            return None

def update_display():
    display_text.config(state=tk.NORMAL)
    display_text.delete(1.0, tk.END)
    display_text.insert(tk.END, speaker_output)
    display_text.config(state=tk.DISABLED)

""" def add_custom_symbol():
    symbol_word = simpledialog.askstring("Input", "Enter the word:")
    symbol_char = simpledialog.askstring("Input", "Enter the symbol:")
    if symbol_word and symbol_char:
        symbols[symbol_word.lower()] = symbol_char
        with open("symbols.py", "a") as sym_file:
            sym_file.write(f"    '{symbol_word.lower()}': '{symbol_char}',\n")
        audio_feedback(True) """

def export_text():
    export_format = simpledialog.askstring("Input", "Enter the format (txt/pdf/docx):")
    if export_format and export_format.lower() in ["txt", "pdf", "docx"]:
        filename = filedialog.asksaveasfilename(defaultextension=f".{export_format}")
        if filename:
            with open(filename, "w", encoding="utf-8") as file:
                file.write(speaker_output)
            audio_feedback(True)

def change_language():
    global current_language
    selected_language = simpledialog.askstring("Input", "Enter the language (English, Hindi, Spanish, French, German, Kannada):")
    if selected_language and selected_language in LANGUAGES:
        current_language = selected_language
        print(f"Language changed to {current_language}")
        audio_feedback(True)

def clear_output():
    global speaker_output
    speaker_output = ""
    update_display()
    audio_feedback(True)

# GUI setup
root = tk.Tk()
root.title(TITLE_OF_PROJECT)
try:
    root.iconbitmap(ICON_PATH)
except:
    print('Favicon is missing!!')
root.geometry("720x520")

main_frame = ttk.Frame(root, padding="10")
main_frame.pack(fill=tk.BOTH, expand=True)

display_text = scrolledtext.ScrolledText(main_frame, wrap=tk.WORD, font=FONT, state=tk.DISABLED)
display_text.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

button_frame = ttk.Frame(main_frame)
button_frame.pack(fill=tk.X)

record_button = ttk.Button(button_frame, text="Record", command=speech_to_text)
record_button.pack(side=tk.LEFT, padx=5)

export_button = ttk.Button(button_frame, text="Export", command=export_text)
export_button.pack(side=tk.LEFT, padx=5)

change_lang_button = ttk.Button(button_frame, text="Change Language", command=change_language)
change_lang_button.pack(side=tk.LEFT, padx=5)

"""custom_symbol_button = ttk.Button(button_frame, text="Add Custom Symbol", command=add_custom_symbol)
custom_symbol_button.pack(side=tk.LEFT, padx=5)"""

clear_button = ttk.Button(button_frame, text="Clear", command=clear_output)
clear_button.pack(side=tk.LEFT, padx=5)

root.mainloop()