# ears.py
import sounddevice as sd
import numpy as np
import json
import os
import sys
from vosk import Model, KaldiRecognizer
import config

# Check Model
if not os.path.exists(config.MODEL_PATH):
    print(f"❌ ERROR: Folder '{config.MODEL_PATH}' not found.")
    sys.exit()

vosk_model = Model(config.MODEL_PATH)
recognizer = KaldiRecognizer(vosk_model, 16000)

# Global variables for volume detection
audio_level = 0.0
volume_stream = None

def audio_callback(indata, frames, time_info, status):
    """Callback to measure ambient volume."""
    global audio_level
    audio_level = np.linalg.norm(indata) * 20

def start_volume_listener():
    global volume_stream
    if volume_stream is None or not volume_stream.active:
        volume_stream = sd.InputStream(callback=audio_callback)
        volume_stream.start()

def stop_volume_listener():
    global volume_stream
    if volume_stream and volume_stream.active:
        volume_stream.stop()
        volume_stream.close()

def get_audio_level():
    return audio_level

def listen():
    """Active listening for speech to text."""
    # 1. Stop background volume listener (conflict prevention)
    stop_volume_listener()
    
    detected_text = ""
    print("🎧 BMO is listening...")
    
    try:
        with sd.RawInputStream(samplerate=16000, blocksize=8000, dtype="int16", channels=1) as stream:
            # Simple timeout or loop mechanism could be added here
            while True:
                data, overflow = stream.read(4000)
                if recognizer.AcceptWaveform(bytes(data)):
                    result = json.loads(recognizer.Result())
                    text = result.get("text", "")
                    if text:
                        detected_text = text
                        break # Stop after one sentence
    except Exception as e:
        print(f"❌ Ears Error: {e}")
    finally:
        # 2. Restart volume listener
        start_volume_listener()
    
    return detected_text