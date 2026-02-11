from gtts import gTTS
import pygame
import os
import time
import re  # <--- NUEVO: Para limpiar el texto
import config

# Variable interna para saber el nombre del archivo
ARCHIVO_TEMP = config.TEMP_AUDIO_FILE

def limpiar_texto(texto):
    """
    Elimina acciones entre asteriscos o paréntesis para que no se lean.
    Ej: "Hola *sonríe*" -> "Hola"
    """
    # Eliminar contenido entre asteriscos: *acción*
    texto_limpio = re.sub(r'\*.*?\*', '', texto)
    
    # Eliminar contenido entre paréntesis: (acción)
    texto_limpio = re.sub(r'\(.*?\)', '', texto_limpio)
    
    # Eliminar espacios dobles que puedan quedar
    return texto_limpio.strip()

def crear_archivo_audio(texto):
    """
    Solo conecta con Google y guarda el MP3.
    NO lo reproduce todavía.
    Retorna True si funcionó, False si falló.
    """
    if not texto:
        return False

    # --- PASO DE LIMPIEZA ---
    texto_para_leer = limpiar_texto(texto)
    
    # Si después de limpiar no queda nada (ej: solo era una acción), no hacemos nada
    if not texto_para_leer:
        return False

    print(f"🔊 Generando audio para: '{texto_para_leer}'")

    try:
        # Generamos el audio con el texto LIMPIO
        tts = gTTS(text=texto_para_leer, lang="es", tld='com.mx')
        tts.save(ARCHIVO_TEMP)
        return True
    except Exception as e:
        print(f"❌ Error generando audio: {e}")
        return False

def reproducir_ahora():
    """
    Reproduce el archivo que ya fue creado.
    """
    try:
        if not os.path.exists(ARCHIVO_TEMP):
            return

        pygame.mixer.music.load(ARCHIVO_TEMP)
        pygame.mixer.music.play()

        # Esperamos mientras suena para bloquear el hilo
        while pygame.mixer.music.get_busy():
            pygame.time.wait(100)

        pygame.mixer.music.unload()
        
        # Eliminamos el archivo al terminar
        time.sleep(0.1)
        if os.path.exists(ARCHIVO_TEMP):
            os.remove(ARCHIVO_TEMP)

    except Exception as e:
        print(f"❌ Error reproduciendo: {e}")

def is_speaking():
    return pygame.mixer.music.get_busy()