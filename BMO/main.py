import pygame
import sys
import threading
import time
import dj_bmo

# Tus módulos
import config
import brain
import ears
import mouth
import faces
import eyes

# =============================================================================
# 🏁 INICIALIZACIÓN
# =============================================================================
pygame.init()
pygame.mixer.init()

screen = pygame.display.set_mode((800, 480))
pygame.display.set_caption("BMO AI")
clock = pygame.time.Clock()

ears.start_volume_listener()

# ESTADO GLOBAL
ESTADO_BMO = "listening" 
IA_OCUPADA = False 

# TEMPORIZADOR DE SUEÑO
ultima_actividad = pygame.time.get_ticks() 

print("✅ BMO LISTO.")

# =============================================================================
# 🧵 PROCESO IA
# =============================================================================
def proceso_ia():
    global ESTADO_BMO, IA_OCUPADA, ultima_actividad
    
    IA_OCUPADA = True 
    estado_anterior = ESTADO_BMO  # 🧠 NUEVO: BMO anota qué estaba haciendo
    
    # 1. Escuchar
    ESTADO_BMO = "listening"
    texto_usuario = ears.listen()
    
    if texto_usuario:
        print(f"🗣️ Usuario: {texto_usuario}")
        ultima_actividad = pygame.time.get_ticks() 
        brain.add_memory("Usuario", texto_usuario)
        
        texto_lower = texto_usuario.lower()

        # ==========================================
        # 🎵 DETECTAR ORDEN DE MÚSICA Y CONTROL
        # ==========================================
        palabras_musica = ["reproduce", "pon la canción", "pon la cancion", "pon música", "pon musica", "quiero escuchar", "la canción", "la cancion", "toca", "reproducir","música", "pon", "on"]
        palabras_pausa = ["ausa","pausa la música", "pausa la musica", "pausar", "detén la música", "silencio bmo", "pausa", "para música", "para musica", "para la música", "para la musica", "detener música"]
        palabras_siguiente = ["siguiente canción", "siguiente cancion", "otra canción", "cambia la canción", "cambia de cancion", "siguiente"]

        # --- A. ¿QUIERES PAUSAR? ---
        if any(p in texto_lower for p in palabras_pausa):
            print("🎧 DJ BMO: Pausando música...")
            respuesta_spotify = dj_bmo.pausar_musica()
            
            ESTADO_BMO = "speaking"
            if mouth.crear_archivo_audio(respuesta_spotify):
                mouth.reproducir_ahora()
            
            ESTADO_BMO = "listening" 
            ultima_actividad = pygame.time.get_ticks()
            IA_OCUPADA = False
            return 

        # --- B. ¿QUIERES LA SIGUIENTE CANCIÓN? ---
        elif any(p in texto_lower for p in palabras_siguiente):
            print("🎧 DJ BMO: Siguiente canción...")
            respuesta_spotify = dj_bmo.siguiente_cancion()
            
            ESTADO_BMO = "speaking"
            if mouth.crear_archivo_audio(respuesta_spotify):
                mouth.reproducir_ahora()
            
            ESTADO_BMO = "music"
            ultima_actividad = pygame.time.get_ticks()
            IA_OCUPADA = False
            return 

        # --- C. ¿QUIERES REPRODUCIR ALGO NUEVO? ---
        elif any(p in texto_lower for p in palabras_musica):
            print("🎧 DJ BMO Activado...")
            ESTADO_BMO = "thinking" 
            faces.dibujar(screen, ESTADO_BMO)
            pygame.display.flip()

            busqueda = texto_lower
            for p in palabras_musica:
                busqueda = busqueda.replace(p, "")
            
            palabras_basura = ["on"]
            for basura in palabras_basura:
                busqueda = busqueda.replace(basura, "")
                
            busqueda = busqueda.strip()

            if not busqueda:
                busqueda = "Bad bunny" 

            respuesta_spotify = dj_bmo.reproducir_cancion(busqueda)
            
            ESTADO_BMO = "speaking"
            exito = mouth.crear_archivo_audio(respuesta_spotify)
            if exito:
                mouth.reproducir_ahora()
            
            ESTADO_BMO = "music"
            ultima_actividad = pygame.time.get_ticks()
            IA_OCUPADA = False
            return 

        # ==========================================
        # 👁️ DETECTAR SI QUIERES QUE VEA
        # ==========================================
        ruta_foto = None
        palabras_clave_vision = ["mira", "qué ves", "que ves", "observa", "toma una foto"]
        
        if any(p in texto_lower for p in palabras_clave_vision):
            print("👁️ Activando ojos...")
            ESTADO_BMO = "capturing"
            faces.dibujar(screen, ESTADO_BMO)
            pygame.display.flip() 
            
            ruta_foto = eyes.tomar_foto()

        # ==========================================
        # 🧠 PENSAR (Gemini)
        # ==========================================
        ESTADO_BMO = "thinking"
        respuesta = brain.think(texto_usuario, ruta_imagen=ruta_foto)

        exito = mouth.crear_archivo_audio(respuesta)

        if exito:
            ESTADO_BMO = "speaking"
            mouth.reproducir_ahora()
        
        ultima_actividad = pygame.time.get_ticks()
        
    else:
        # ⬇️ NUEVO: Si no entendió nada (falsa alarma por la música), vuelve a ser DJ
        ESTADO_BMO = estado_anterior
        
    IA_OCUPADA = False

# =============================================================================
# 🔁 BUCLE PRINCIPAL
# =============================================================================
running = True

while running:
    ahora = pygame.time.get_ticks()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if not IA_OCUPADA:
        tiempo_inactivo = ahora - ultima_actividad

        # ⬇️ NUEVA LÓGICA: Si NO está en modo DJ, aplicamos las reglas normales
        if ESTADO_BMO != "music":
            if tiempo_inactivo > config.TIEMPO_PARA_DORMIR:
                ESTADO_BMO = "sleep"
            else:
                ESTADO_BMO = "listening"
        # Si ESTADO_BMO es "music", simplemente lo deja así y no se duerme.

        nivel_ruido = ears.get_audio_level()
        
        if nivel_ruido > config.AUDIO_THRESHOLD:
            ultima_actividad = ahora 
            threading.Thread(target=proceso_ia, daemon=True).start()

    faces.dibujar(screen, ESTADO_BMO)
    pygame.display.flip()
    clock.tick(60)

ears.stop_volume_listener()
pygame.quit()
sys.exit()