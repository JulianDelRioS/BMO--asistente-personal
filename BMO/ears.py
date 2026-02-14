import sounddevice as sd
import numpy as np
import json
import os
import sys
from google.cloud import speech
import config

# Configuración de la llave de Google
# Asegúrate de que el archivo se llame exactamente así en tu carpeta
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "google_keys.json"

# Variables globales para la detección de volumen (Bucle principal)
audio_level = 0.0
volume_stream = None

def audio_callback(indata, frames, time_info, status):
    """Callback para medir el volumen ambiental y despertar a BMO."""
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
    """Escucha activa usando Google Cloud Speech-to-Text."""
    # 1. Detenemos el medidor de volumen para no crear conflicto con el micrófono
    stop_volume_listener()
    
    print("🎧 BMO está procesando tu voz con Google...")
    
    detected_text = ""
    client = speech.SpeechClient()

    # Grabamos un pequeño segmento de audio (aprox 3.5 segundos)
    # Esto es más que suficiente para una orden clara
    fs = 16000  
    seconds = 3.5
    
    try:
        # Grabación directa desde sounddevice
        recording = sd.rec(int(seconds * fs), samplerate=fs, channels=1, dtype='int16')
        sd.wait()  # Espera a que termine la grabación
        
        # Convertimos la grabación a bytes
        content = recording.tobytes()
        audio = speech.RecognitionAudio(content=content)
        
        # Configuración de reconocimiento
        # Usamos es-CL por tu ubicación en Quilpué
        config_google = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=fs,
            language_code="es-CL", 
            enable_automatic_punctuation=True
        )

        # Enviamos a Google
        response = client.recognize(config=config_google, audio=audio)

        for result in response.results:
            detected_text = result.alternatives[0].transcript
            
    except Exception as e:
        print(f"❌ Error en los oídos (Google): {e}")
    
    finally:
        # 2. Reiniciamos el medidor de volumen para que BMO pueda volver a despertar
        start_volume_listener()
    
    return detected_text