# tts_generator.py

from gtts import gTTS
import os

def save_narration_as_mp3(narration, output_path="audio/narration.mp3"):
    os.makedirs("audio", exist_ok=True)
    full_text = " ".join(narration)
    tts = gTTS(full_text)
    tts.save(output_path)
    return output_path
