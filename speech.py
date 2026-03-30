import subprocess
import pyperclip
import keyboard
import re
import threading

# ----- Configuration -----
PIPER_PATH = r"D:/piper/piper.exe"
MODEL_PATH = r"D:/piper/models/en_US-amy-medium.onnx"
OUTPUT_FILE = "out.wav"
HOTKEY = "ctrl+alt+s"

# ----- Functions -----
def speak(text):
    """Generate audio with Piper and play hidden."""
    # Start Piper process
    process = subprocess.Popen(
        [PIPER_PATH, "--model", MODEL_PATH, "--output_file", OUTPUT_FILE],
        stdin=subprocess.PIPE,
        text=True
    )
    process.communicate(text)

    # Play .wav hidden
    threading.Thread(
        target=lambda: subprocess.Popen(
            ["powershell", "-c", f"(New-Object Media.SoundPlayer '{OUTPUT_FILE}').PlaySync()"],
            creationflags=subprocess.CREATE_NO_WINDOW
        ),
        daemon=True
    ).start()

def clean_text_for_tts(text):
    """Strip unwanted characters and replace newlines with dot-space."""
    text = text.replace("\n", ". ")
    # Allow letters, numbers, spaces, and TTS-friendly punctuation
    text = re.sub(r"[^A-Za-z0-9 .,;:!?\'\"\-\+\(\)]+", "", text)
    return text.strip()

def speak_clipboard():
    """Speak current clipboard content."""
    text = pyperclip.paste()
    cleaned = clean_text_for_tts(text)
    if cleaned:
        print("Speaking:", cleaned[:50])
        speak(cleaned)
    else:
        print("Clipboard is empty or no valid characters.")

# ----- Hotkey -----
keyboard.add_hotkey(HOTKEY, speak_clipboard)
print(f"Ready: {HOTKEY} to speak clipboard content")
keyboard.wait()