import pygame
import sys
import threading
import time

# Tus módulos
import config
import brain
import ears
import mouth
import faces

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
# Empezamos en "listening" como pediste
ESTADO_BMO = "listening" 
IA_OCUPADA = False # Para saber si está procesando y no interrumpir

# TEMPORIZADOR DE SUEÑO
ultima_actividad = pygame.time.get_ticks() # Marca el tiempo de inicio

print("✅ BMO LISTO.")

# =============================================================================
# 🧵 PROCESO IA
# =============================================================================
def proceso_ia():
    global ESTADO_BMO, IA_OCUPADA, ultima_actividad
    
    IA_OCUPADA = True 
    
    # 1. Escuchar
    ESTADO_BMO = "listening" # (Recuerda: faces.py lo mostrará estático)
    texto_usuario = ears.listen()
    
    if texto_usuario:
        print(f"🗣️ Usuario: {texto_usuario}")
        ultima_actividad = pygame.time.get_ticks() # Reiniciar contador sueño
        brain.add_memory("Usuario", texto_usuario)

        # 2. Pensar (Gemini)
        ESTADO_BMO = "thinking"
        respuesta = brain.think(texto_usuario)

        # --- AQUÍ ESTÁ EL CAMBIO CLAVE ---
        
        # BMO SIGUE EN "THINKING" MIENTRAS DESCARGA EL AUDIO
        # (Esto tarda esos 3 segundos que notabas)
        exito = mouth.crear_archivo_audio(respuesta)

        if exito:
            # 3. Hablar (Solo cambiamos la cara AHORA que el audio está listo)
            ESTADO_BMO = "speaking"
            mouth.reproducir_ahora()
        
        # ---------------------------------
        
        ultima_actividad = pygame.time.get_ticks()
    
    IA_OCUPADA = False 
    # Al terminar, el loop principal lo pondrá en listening o sleep según corresponda

# =============================================================================
# 🔁 BUCLE PRINCIPAL
# =============================================================================
running = True

while running:
    # Tiempo actual en este frame
    ahora = pygame.time.get_ticks()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # --- LÓGICA DE COMPORTAMIENTO ---
    
    if not IA_OCUPADA:
        # 1. Calcular cuánto tiempo ha pasado desde la última vez que habló/escuchó
        tiempo_inactivo = ahora - ultima_actividad

        # 2. Decidir estado según tiempo
        if tiempo_inactivo > config.TIEMPO_PARA_DORMIR:
            ESTADO_BMO = "sleep"
        else:
            # Si no ha pasado el tiempo, se mantiene en listening (tu default)
            ESTADO_BMO = "listening"

        # 3. Detectar sonido para "Despertar" o "Atender"
        nivel_ruido = ears.get_audio_level()
        
        if nivel_ruido > config.AUDIO_THRESHOLD:
            # Si hay ruido, ¡SE DESPIERTA! Reiniciamos contador
            ultima_actividad = ahora 
            
            # Lanzamos la IA
            threading.Thread(target=proceso_ia, daemon=True).start()

    # --- DIBUJAR ---
    # faces.py se encarga de animar la carpeta que le digamos
    faces.dibujar(screen, ESTADO_BMO)

    pygame.display.flip()
    clock.tick(60)

ears.stop_volume_listener()
pygame.quit()
sys.exit()