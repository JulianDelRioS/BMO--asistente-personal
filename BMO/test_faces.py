import pygame
import sys

# =============================================================================
# 🎨 ZONA DE DISEÑO (Aquí modificas la cara para probar)
# =============================================================================
def dibujar_prueba(screen, eye_x, eye_y, is_blinking, esta_hablando):
    """
    Versión local de dibujo para pruebas rápidas.
    """
    # Centro de la pantalla
    cx, cy = 400, 240
    
    # 1. Fondo Verde BMO
    screen.fill((120, 200, 180)) 

    # 2. OJOS
    negro = (0, 0, 0)

    if esta_hablando:
        # Ojos felices ^ ^ (Más gruesos y definidos)
        grosor_ojos = 10
        # Ojo Izquierdo
        pygame.draw.lines(screen, negro, False, 
                          [(cx-110, cy-35), (cx-75, cy-75), (cx-40, cy-35)], grosor_ojos)
        # Ojo Derecho
        pygame.draw.lines(screen, negro, False, 
                          [(cx+40, cy-35), (cx+75, cy-75), (cx+110, cy-35)], grosor_ojos)
    
    elif is_blinking:
        # Ojos cerrados (Líneas rectas)
        pygame.draw.line(screen, negro, (cx-100, cy-40), (cx-60, cy-40), 6)
        pygame.draw.line(screen, negro, (cx+60, cy-40), (cx+100, cy-40), 6)
    
    else:
        # --- OJOS REDONDOS (CIRCULOS) ---
        # Calculamos el centro exacto sumando el movimiento (eye_x, eye_y)
        radio = 18 # Qué tan grandes son los círculos
        
        # Ojo Izquierdo
        pos_izq = (int(cx - 85 + eye_x), int(cy - 50 + eye_y))
        pygame.draw.circle(screen, negro, pos_izq, radio)
        
        # Ojo Derecho
        pos_der = (int(cx + 85 + eye_x), int(cy - 50 + eye_y))
        pygame.draw.circle(screen, negro, pos_der, radio)

    # 3. BOCA
    if esta_hablando:
        # Definiciones de geometría para la boca abierta
        rect_boca = pygame.Rect(cx-60, cy+10, 120, 70)
        
        # A. Fondo Oscuro
        pygame.draw.rect(screen, (10, 50, 30), rect_boca, border_radius=30)
        
        # B. Dientes
        rect_dientes = pygame.Rect(cx-45, cy+10, 90, 20)
        # Nota: Si tu versión de pygame es antigua, quita los border_radius específicos
        pygame.draw.rect(screen, (255,255,255), rect_dientes, 
                         border_bottom_left_radius=10, border_bottom_right_radius=10)
        
        # C. Lengua
        rect_lengua = pygame.Rect(cx-40, cy+45, 80, 35)
        pygame.draw.ellipse(screen, (60, 160, 80), rect_lengua)

        # D. Borde Negro
        pygame.draw.rect(screen, (0,0,0), rect_boca, 6, border_radius=30)

    else:
        # Sonrisa normal
        pygame.draw.arc(screen, negro, (cx-40, cy+30, 80, 40), 3.14, 0, 5)

# =============================================================================
# 🎮 LOOP DE PRUEBA (No necesitas tocar esto)
# =============================================================================
pygame.init()
ancho, alto = 800, 480
screen = pygame.display.set_mode((ancho, alto))
pygame.display.set_caption("🧪 LABORATORIO DE BMO (Modo Diseño)")
clock = pygame.time.Clock()

is_blinking = False
blink_timer = 0

print("--- CONTROLES ---")
print("MOUSE: Mover ojos")
print("ESPACIO: Hablar")
print("CLICK: Parpadear")

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False

    # Simular Inputs
    keys = pygame.key.get_pressed()
    esta_hablando = keys[pygame.K_SPACE] # Espacio para hablar

    # Mouse controla ojos
    mx, my = pygame.mouse.get_pos()
    eye_x = (mx - ancho/2) / 10 
    eye_y = (my - alto/2) / 15
    eye_x = max(-25, min(25, eye_x))
    eye_y = max(-15, min(15, eye_y))

    # Parpadeo
    click = pygame.mouse.get_pressed()
    curr_time = pygame.time.get_ticks()
    
    if click[0]: is_blinking = True
    elif not is_blinking and curr_time - blink_timer > 3000:
        is_blinking = True
        blink_start = curr_time
    
    if is_blinking and not click[0]:
        if curr_time - blink_start > 150:
            is_blinking = False
            blink_timer = curr_time

    # DIBUJAR USANDO LA FUNCIÓN DE ARRIBA
    dibujar_prueba(screen, eye_x, eye_y, is_blinking, esta_hablando)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()