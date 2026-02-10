import pygame
import sys
import random
import sounddevice as sd
import numpy as np
import threading
from google import genai
from gtts import gTTS
import os
import time
import json
from vosk import Model, KaldiRecognizer

# =============================================================================
# 🔑 GOOGLE GEMINI CONFIG
# =============================================================================
API_KEY = "" 

client = genai.Client(api_key=API_KEY)

# =============================================================================
# 🧠 MEMORIA Y PERSONALIDAD
# =============================================================================
MEMORIA = []
MAX_MEMORIA = 6
hablando = False
ULTIMA_RESPUESTA = 0
COOLDOWN_MS = 3000
audio_level = 0.0

# Instrucciones para bmo
SYSTEM_INSTRUCTION = """
Eres bimo se escribe BMO, un asistente personal hombre inteligente visualizado en una pantalla.
- Tu creador se llama Julian Del Rio y es tu mejor amigo.
- Tu personalidad es agradable, alegre, pero muy eficiente.
- Tus respuestas deben ser humanas (máximo 6 frases) para que el audio sea muy creible.
- No eres un robot genérico, tienes opinión.
- Si el usuario te insulta, responde con elegancia e ironía.
"""

def agregar_memoria(rol, texto):
    MEMORIA.append(f"{rol}: {texto}")
    if len(MEMORIA) > MAX_MEMORIA:
        MEMORIA.pop(0)

# =============================================================================
# 🎤 VOSK (Reconocimiento de voz)
# =============================================================================
if not os.path.exists("model"):
    print("❌ ERROR: No se encuentra la carpeta 'model'")
    print("Descarga el modelo de: https://alphacephei.com/vosk/models")
    sys.exit()

vosk_model = Model("model")
recognizer = KaldiRecognizer(vosk_model, 16000)

def escuchar_voz():
    with sd.RawInputStream(samplerate=16000, blocksize=8000, dtype="int16", channels=1) as stream:
        print("🎧 bmo está escuchando...")
        while True:
            data, overflow = stream.read(4000)
            if recognizer.AcceptWaveform(bytes(data)):
                resultado = json.loads(recognizer.Result())
                texto = resultado.get("text", "")
                if texto:
                    return texto

# =============================================================================
# 🔊 TTS (Texto a Voz)
# =============================================================================
def hablar_gtts(texto):
    if not texto:
        return
    print(f"🔊 bmo dice: {texto}")
    try:
        tts = gTTS(text=texto, lang="es", tld='com.mx')
        tts.save("temp_voice.mp3")

        pygame.mixer.music.load("temp_voice.mp3")
        pygame.mixer.music.play()

        # Esperar mientras reproduce
        while pygame.mixer.music.get_busy():
            pygame.time.wait(100)

        pygame.mixer.music.unload()
        time.sleep(0.1)
        os.remove("temp_voice.mp3")

    except Exception as e:
        print(f"❌ Error en audio: {e}")

# =============================================================================
# 🎤 DETECTOR DE VOLUMEN
# =============================================================================
def audio_callback(indata, frames, time_info, status):
    global audio_level
    if not hablando:
        audio_level = np.linalg.norm(indata) * 20
    else:
        audio_level = 0

detector_stream = sd.InputStream(callback=audio_callback)

# =============================================================================
# 🧠 CEREBRO (GEMINI WORKER)
# =============================================================================
def proceso_ia_worker():
    global hablando
    try:
        hablando = True
        if detector_stream.active:
            detector_stream.stop()

        texto_usuario = escuchar_voz()
        
        if not texto_usuario or len(texto_usuario) < 2:
            return

        print(f"🗣️ Tú: {texto_usuario}")
        agregar_memoria("Usuario", texto_usuario)

        print("🌐 bmo está pensando...")
        
        historial_chat = "\n".join(MEMORIA)
        prompt_completo = f"{SYSTEM_INSTRUCTION}\n\nHistorial:\n{historial_chat}\n\nUsuario: {texto_usuario}\bmo:"

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt_completo
        )

        respuesta = response.text.strip()
        agregar_memoria("bmo", respuesta)
        hablar_gtts(respuesta)

    except Exception as e:
        print(f"❌ ERROR EN CEREBRO: {e}")
        hablar_gtts("Error de conexión.")
    
    finally:
        hablando = False
        if not detector_stream.active:
            detector_stream.start()
        print("👂 Esperando comando...")

# =============================================================================
# 🎮 PYGAME (Visuales Restauradas)
# =============================================================================
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((800, 480))
pygame.display.set_caption("bmo AI")
clock = pygame.time.Clock()

eye_x = eye_y = 0
target_x = target_y = 0
blink_time = pygame.time.get_ticks()
is_blinking = False

detector_stream.start()
print("✅ bmo INICIADO (Modo Réplica Exacta).")

# =============================================================================
# 🔁 LOOP PRINCIPAL
# =============================================================================
running = True
while running:
    curr_time = pygame.time.get_ticks()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Detectar voz usuario
    if audio_level > 15 and not hablando and (curr_time - ULTIMA_RESPUESTA > COOLDOWN_MS):
        ULTIMA_RESPUESTA = curr_time
        threading.Thread(target=proceso_ia_worker, daemon=True).start()

    # Movimiento aleatorio de ojos
    if random.randint(0, 70) == 0:
        target_x = random.randint(-15, 15)
        target_y = random.randint(-8, 8)

    eye_x += (target_x - eye_x) * 0.1
    eye_y += (target_y - eye_y) * 0.1

    # Parpadeo
    if not is_blinking and curr_time - blink_time > 3500:
        is_blinking = True
        blink_start = curr_time

    if is_blinking and curr_time - blink_start > 150:
        is_blinking = False
        blink_time = curr_time

    # --- DIBUJO ---
    
    # 1. Fondo Verde BMO
    screen.fill((120, 200, 180)) 
    cx, cy = 400, 240
    
    # Variable clave: ¿Está hablando?
    esta_hablando = pygame.mixer.music.get_busy()

    # 2. OJOS
    if esta_hablando:
        # Ojos felices ^ ^ (Más gruesos y definidos como en la imagen)
        grosor_ojos = 10
        # Ojo Izquierdo
        pygame.draw.lines(screen, (0,0,0), False, 
                         [(cx-110, cy-35), (cx-75, cy-75), (cx-40, cy-35)], grosor_ojos)
        # Ojo Derecho
        pygame.draw.lines(screen, (0,0,0), False, 
                         [(cx+40, cy-35), (cx+75, cy-75), (cx+110, cy-35)], grosor_ojos)
    
    elif is_blinking:
        pygame.draw.line(screen, (0,0,0), (cx-100, cy-40), (cx-60, cy-40), 6)
        pygame.draw.line(screen, (0,0,0), (cx+60, cy-40), (cx+100, cy-40), 6)
    
    else:
        pygame.draw.ellipse(screen, (0,0,0), (cx-100+eye_x, cy-60+eye_y, 25, 40))
        pygame.draw.ellipse(screen, (0,0,0), (cx+75+eye_x, cy-60+eye_y, 25, 40))

    # 3. BOCA (Réplica de la imagen)
    if esta_hablando:
        # Definiciones de geometría para coincidir con la foto
        rect_boca = pygame.Rect(cx-60, cy+10, 120, 70)
        
        # A. Fondo Oscuro (Verde muy oscuro, casi negro, como en la imagen)
        pygame.draw.rect(screen, (10, 50, 30), rect_boca, border_radius=30)
        
        # B. Dientes (Bloque blanco arriba, centrado, bordes redondeados)
        rect_dientes = pygame.Rect(cx-45, cy+10, 90, 20)
        pygame.draw.rect(screen, (255,255,255), rect_dientes, 
                         border_bottom_left_radius=10, border_bottom_right_radius=10)
        
        # C. Lengua (Verde - "colina" abajo)
        # Usamos una elipse recortada visualmente por el borde negro posterior
        rect_lengua = pygame.Rect(cx-40, cy+45, 80, 35)
        pygame.draw.ellipse(screen, (60, 160, 80), rect_lengua)

        # D. Borde Negro (Grueso para definir la forma final)
        pygame.draw.rect(screen, (0,0,0), rect_boca, 6, border_radius=30)

    else:
        # Sonrisa normal
        pygame.draw.arc(screen, (0,0,0), (cx-40, cy+30, 80, 40), 3.14, 0, 5)

    pygame.display.flip()
    clock.tick(60)

try:
    detector_stream.stop()
    detector_stream.close()
except:
    pass
pygame.quit()
sys.exit()