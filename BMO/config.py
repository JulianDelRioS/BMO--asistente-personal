import os
import sys
from dotenv import load_dotenv

# ==========================================
# 🧭 FUNCIÓN BRÚJULA (NECESARIA PARA EYES.PY Y EXE)
# ==========================================
def resource_path(relative_path):
    """Obtiene la ruta absoluta para recursos, funcione como script o como exe."""
    try:
        # PyInstaller crea una carpeta temporal en _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

# ==========================================
# 🔑 CARGAR API KEY
# ==========================================
# Cargar variables de entorno del archivo .env usando la brújula
load_dotenv(resource_path(".env"))

API_KEY = os.getenv("GEMINI_API_KEY")

# Validación de seguridad
if not API_KEY:
    # Si no tienes .env, puedes poner tu clave aquí abajo como respaldo:
    API_KEY = "TU_API_KEY_AQUI_SI_NO_USAS_ENV" 
    if API_KEY == "TU_API_KEY_AQUI_SI_NO_USAS_ENV":
        print("⚠️ ADVERTENCIA: No se encontró API KEY.")

# ==========================================
# ⚙️ GENERAL SETTINGS (Tus ajustes)
# ==========================================

# ⏱️ TIEMPOS
TIEMPO_PARA_DORMIR = 45000   # 45 segundos (Tuyo)
COOLDOWN_MS = 3000           # Tiempo entre respuestas

# 🧠 MEMORIA Y AUDIO
MAX_MEMORY = 6
AUDIO_THRESHOLD = 15         # Sensibilidad del micrófono

# 📁 PATHS (Actualizados con resource_path para evitar errores)
MODEL_PATH = resource_path("model")
TEMP_AUDIO_FILE = resource_path("temp_voice.mp3")

# 🤖 PERSONALITY (Tu Prompt)
SYSTEM_INSTRUCTION = """
Eres BIMO, un asistente personal hombre inteligente visualizado en una pantalla.
- Si en la imagen que ves aparece un joven [describe tu apariencia brevemente, ej: con lentes y pelo corto], ESE ES JULIAN. Salúdalo por su nombre y dile algo lindo.
- IMPORTANTE: NO describas tus acciones físicas. No uses asteriscos ni paréntesis para narrar lo que haces (ej: no escribas *saluda*, *baila*).
- Tu creador se llama Julian Del Rio y es tu mejor amigo y tu eres su asistente personal, siempre hablaras con el.
- Tu personalidad es agradable, alegre, pero muy eficiente.
- Tus respuestas deben ser humanas (máximo 3 frases) para que el audio sea muy creible y no tan largo.
- No eres un robot genérico, tienes opinión.
- Si el usuario te insulta, responde con elegancia e ironía.
"""