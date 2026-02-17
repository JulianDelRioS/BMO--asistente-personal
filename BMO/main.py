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
intentos_fallidos = 0

# TEMPORIZADOR DE SUEÑO
ultima_actividad = pygame.time.get_ticks() 

print("✅ BMO LISTO.")

# =============================================================================
# 🧵 PROCESO IA
# =============================================================================
def proceso_ia():
    global ESTADO_BMO, IA_OCUPADA, ultima_actividad, intentos_fallidos
    
    IA_OCUPADA = True 
    estado_anterior = ESTADO_BMO  # 🧠 MEMORIA: Guardamos qué estaba haciendo (ej: music)
    
    # 1. Escuchar
    # Ponemos cara de escucha momentánea
    ESTADO_BMO = "listening"
    texto_usuario = ears.listen()
    
    if texto_usuario:
        # ¡ÉXITO! Si entendió algo, reseteamos los strikes a 0
        intentos_fallidos = 0 
        
        print(f"🗣️ Usuario: {texto_usuario}")
        ultima_actividad = pygame.time.get_ticks() 
        brain.add_memory("Usuario", texto_usuario)
        
        texto_lower = texto_usuario.lower()

        # ==========================================
        # 🎵 DETECTAR ORDEN DE MÚSICA Y CONTROL
        # ==========================================
        palabras_musica = ["reproduce", "pon la canción", "pon la cancion", "pon música", "pon musica", "quiero escuchar", "la canción", "la cancion", "toca", "reproducir","música", "pon"]
        palabras_pausa = ["ausa","pausa la música", "pausa la musica", "pausar", "detén la música", "silencio bmo", "pausa", "para música", "para musica", "para la música", "para la musica", "detener música"]
        palabras_siguiente = ["siguiente canción", "siguiente cancion", "otra canción", "cambia la canción", "cambia de cancion", "siguiente"]
        palabras_playlist = ["playlist", "lista de reproducción", "mi lista", "mis canciones"]

        # --- A. ¿QUIERES PAUSAR? ---
        if any(p in texto_lower for p in palabras_pausa):
            print("🎧 DJ BMO: Pausando música...")
            respuesta_spotify = dj_bmo.pausar_musica()
            
            ESTADO_BMO = "speaking"
            if mouth.crear_archivo_audio(respuesta_spotify):
                mouth.reproducir_ahora()
            
            ESTADO_BMO = "listening" # Al pausar, vuelve a estar atento
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
            
            ESTADO_BMO = "music" # Mantiene modo DJ
            ultima_actividad = pygame.time.get_ticks()
            IA_OCUPADA = False
            return 

# --- C. ¿QUIERES UNA PLAYLIST? (INTERACTIVO) ---
        elif any(p in texto_lower for p in palabras_playlist):
            print("🎧 DJ BMO: Revisando playlists...")
            ESTADO_BMO = "thinking"
            faces.dibujar(screen, ESTADO_BMO)
            pygame.display.flip()

            nombre_lista = ""
            
            # 1. Intentamos ver si ya dijiste el nombre (ej: "Pon mi playlist Rock")
            frases_activadoras = [
                "pon mi playlist", "pon la playlist", "reproduce mi playlist", 
                "reproduce la playlist", "escuchar playlist", "mi playlist", "playlist"
            ]
            
            for frase in frases_activadoras:
                if frase in texto_lower:
                    partes = texto_lower.split(frase, 1)
                    if len(partes) > 1:
                        nombre_lista = partes[1].strip()
                        break

            # ---------------------------------------------------------
            # CASO 1: NO DIJISTE NOMBRE -> BMO TE PREGUNTA
            # ---------------------------------------------------------
            if not nombre_lista:
                print("❓ No especificaste nombre. Preguntando...")
                
                # Obtenemos las 6 primeras
                nombres = dj_bmo.listar_mis_playlists(limite=6)
                
                if nombres:
                    # Preparamos el texto que dirá BMO
                    lista_texto = ", ".join(nombres)
                    respuesta_bmo = f"Tengo estas listas: {lista_texto}. ¿Cuál quieres escuchar?"
                    
                    # BMO habla
                    ESTADO_BMO = "speaking"
                    if mouth.crear_archivo_audio(respuesta_bmo):
                        mouth.reproducir_ahora()
                    
                    # BMO vuelve a escuchar tu respuesta
                    ESTADO_BMO = "listening"
                    faces.dibujar(screen, ESTADO_BMO)
                    pygame.display.flip()
                    
                    respuesta_usuario = ears.listen() # <--- Escucha de nuevo aquí
                    
                    if respuesta_usuario:
                        print(f"🗣️ Elegiste: {respuesta_usuario}")
                        nombre_lista = respuesta_usuario # Usamos tu respuesta como nombre
                    else:
                        print("❌ No escuché respuesta.")
                        IA_OCUPADA = False
                        return
                else:
                    respuesta_bmo = "No encontré playlists en tu biblioteca."
                    mouth.crear_archivo_audio(respuesta_bmo)
                    mouth.reproducir_ahora()
                    IA_OCUPADA = False
                    return

            # ---------------------------------------------------------
            # CASO 2: YA TENEMOS NOMBRE (O LO ACABAS DE DECIR) -> REPRODUCIR
            # ---------------------------------------------------------
            print(f"🔍 Buscando playlist: '{nombre_lista}'")
            
            respuesta_spotify = dj_bmo.reproducir_playlist(nombre_lista)
            
            ESTADO_BMO = "speaking"
            if mouth.crear_archivo_audio(respuesta_spotify):
                mouth.reproducir_ahora()
            
            ESTADO_BMO = "music"
            ultima_actividad = pygame.time.get_ticks()
            IA_OCUPADA = False
            return

        # --- D. ¿QUIERES REPRODUCIR UNA CANCIÓN? ---
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
            
            ESTADO_BMO = "music" # Activa modo DJ
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
        # -----------------------------------------------------------
        # ❌ FALLO: SE ESCUCHÓ RUIDO PERO NO TEXTO (STRIKE SYSTEM)
        # -----------------------------------------------------------
        intentos_fallidos += 1
        print(f"⚠️ Ruido detectado sin voz ({intentos_fallidos}/4)")

        # Si llegamos a 4 fallos seguidos (ruido constante)...
        if intentos_fallidos >= 4:
            print("💤 Demasiado ruido ambiente. Ignorando micrófono por 10 segundos...")
            ESTADO_BMO = estado_anterior # Volvemos a la cara de DJ
            faces.dibujar(screen, ESTADO_BMO) # Forzamos actualización visual
            pygame.display.flip()
            
            # Bloqueamos el hilo 10 segundos para que no vuelva a escuchar
            time.sleep(10) 
            
            # Al despertar, reseteamos el contador para dar otra oportunidad
            intentos_fallidos = 0 
        else:
            # Si son menos de 4, simplemente volvemos al estado anterior rápido
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

        # ⬇️ LÓGICA ANTI-SUEÑO EN MODO DJ
        if ESTADO_BMO != "music":
            if tiempo_inactivo > config.TIEMPO_PARA_DORMIR:
                ESTADO_BMO = "sleep"
            else:
                ESTADO_BMO = "listening"
        # Si es "music", se queda así y no hace nada más (ignora listening y sleep)

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