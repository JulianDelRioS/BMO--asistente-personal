import asyncio
import edge_tts
import pygame
import os
import time
import re
import config

# =============================================================================
# ⚙️ CONFIGURACIÓN DE VOZ (Estilo BMO)
# =============================================================================
ARCHIVO_TEMP = config.TEMP_AUDIO_FILE

# VOZ: Usamos Dalia (México) como base porque es clara y alegre
VOZ = "es-MX-DaliaNeural"

# AJUSTES: 
# +30Hz = Hace la voz mucho más aguda (efecto niño/robot)
# +10%  = Habla un poquito más rápido
PARAMETROS_RATE = "+10%"
PARAMETROS_PITCH = "+30Hz"

# =============================================================================
# 🧹 LIMPIEZA DE TEXTO
# =============================================================================
def limpiar_texto(texto):
    """
    Elimina acciones entre asteriscos o paréntesis.
    Ej: "Hola *saluda*" -> "Hola"
    """
    if not texto: return ""
    
    # Eliminar *acción*
    texto_limpio = re.sub(r'\*.*?\*', '', texto)
    # Eliminar (acción)
    texto_limpio = re.sub(r'\(.*?\)', '', texto_limpio)
    
    return texto_limpio.strip()

# =============================================================================
# 🔊 GENERACIÓN DE AUDIO (Edge-TTS)
# =============================================================================
def crear_archivo_audio(texto):
    """
    Conecta con Microsoft Edge TTS y guarda el MP3 con tono modificado.
    Retorna True si funcionó.
    """
    texto_para_leer = limpiar_texto(texto)
    
    if not texto_para_leer:
        return False

    print(f"🔊 Generando voz de BMO: '{texto_para_leer}'")

    # Función asíncrona interna necesaria para edge-tts
    async def generar():
        communicate = edge_tts.Communicate(
            text=texto_para_leer, 
            voice=VOZ, 
            rate=PARAMETROS_RATE, 
            pitch=PARAMETROS_PITCH
        )
        await communicate.save(ARCHIVO_TEMP)

    try:
        # Ejecutamos la función asíncrona de forma síncrona
        asyncio.run(generar())
        return True
    except Exception as e:
        print(f"❌ Error Edge-TTS: {e}")
        return False

# =============================================================================
# 🎵 REPRODUCCIÓN
# =============================================================================
def reproducir_ahora():
    """
    Reproduce el archivo generado.
    """
    try:
        if not os.path.exists(ARCHIVO_TEMP):
            return

        pygame.mixer.music.load(ARCHIVO_TEMP)
        pygame.mixer.music.play()

        # Esperar mientras reproduce
        while pygame.mixer.music.get_busy():
            pygame.time.wait(100)

        pygame.mixer.music.unload()
        
        # Pequeña pausa para liberar el archivo del sistema
        time.sleep(0.1)
        
        if os.path.exists(ARCHIVO_TEMP):
            os.remove(ARCHIVO_TEMP)

    except Exception as e:
        print(f"❌ Error reproduciendo: {e}")

def is_speaking():
    return pygame.mixer.music.get_busy()