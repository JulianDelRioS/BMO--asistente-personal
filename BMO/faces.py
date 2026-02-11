import pygame
import os

# =============================================================================
# ⚙️ CONFIGURACIÓN DE CARAS
# =============================================================================
ANCHO, ALTO = 800, 480
VELOCIDAD_ANIMACION = 150  # Milisegundos por frame

# Diccionario donde guardaremos las imágenes en memoria
ANIMACIONES = {}
CARGADO = False

# Lista exacta de tus carpetas según la imagen
ESTADOS_VALIDOS = ["capturing", "error", "listening", "sleep", "speaking", "thinking"]

def cargar_carpeta(nombre_carpeta):
    """Carga imágenes de la carpeta BMO/Faces/{nombre_carpeta}"""
    # Nota: Respetamos la mayúscula de 'Faces' que vi en tu imagen
    ruta_base = os.path.join("Faces", nombre_carpeta)
    lista_imagenes = []

    if not os.path.exists(ruta_base):
        print(f"⚠️ AVISO: No encuentro la carpeta '{ruta_base}'")
        surf = pygame.Surface((ANCHO, ALTO))
        surf.fill((0, 0, 0)) # Negro si falta carpeta
        return [surf]

    # Ordenamos los archivos para que 01 vaya antes que 02, etc.
    archivos = sorted([f for f in os.listdir(ruta_base) if f.endswith(".png") or f.endswith(".jpg")])
    
    for archivo in archivos:
        try:
            ruta_completa = os.path.join(ruta_base, archivo)
            img = pygame.image.load(ruta_completa)
            img = pygame.transform.scale(img, (ANCHO, ALTO))
            lista_imagenes.append(img)
        except Exception as e:
            print(f"❌ Error en {archivo}: {e}")

    if not lista_imagenes:
        return [pygame.Surface((ANCHO, ALTO))] # Retorna negro si está vacía

    print(f"✅ '{nombre_carpeta}': {len(lista_imagenes)} frames.")
    return lista_imagenes

def inicializar():
    global CARGADO, ANIMACIONES
    if CARGADO: return
    
    print("--- CARGANDO TEXTURAS BMO ---")
    for estado in ESTADOS_VALIDOS:
        ANIMACIONES[estado] = cargar_carpeta(estado)
    CARGADO = True

# =============================================================================
# 🎨 FUNCIÓN DE DIBUJO POR ESTADO
# =============================================================================
# En faces.py

def dibujar(screen, estado_actual):
    """
    Dibuja el estado actual.
    - listening: Estático (solo frame 0).
    - otros: Animados (ciclo de frames).
    """
    if not CARGADO:
        inicializar()

    # Validación de seguridad
    if estado_actual not in ANIMACIONES:
        estado_actual = "sleep"
    
    frames = ANIMACIONES[estado_actual]
    
    if not frames:
        return # Evitar error si la lista está vacía

    # --- LÓGICA DE ANIMACIÓN ---
    if estado_actual == "listening":
        # 🛑 CASO ESPECIAL: Listening es ESTÁTICO
        # Forzamos siempre el índice 0 (listen 01.png)
        indice = 0
    else:
        # 🔄 RESTO DE ESTADOS: Animados
        # Calculamos qué frame toca según el tiempo
        tiempo = pygame.time.get_ticks()
        indice = (tiempo // VELOCIDAD_ANIMACION) % len(frames)
    
    # Dibujar
    screen.blit(frames[indice], (0, 0))