# config.py
import os
from dotenv import load_dotenv

# ⏱️ TIEMPOS
COOLDOWN_MS = 1000
TIEMPO_PARA_DORMIR = 45000  # 45 segundos en milisegundos 
# 1. Cargar variables de entorno del archivo .env
load_dotenv()
# 🔑 API KEY (Cargada desde variable de entorno)
API_KEY = os.getenv("GEMINI_API_KEY")

# ⚙️ GENERAL SETTINGS
MAX_MEMORY = 6
COOLDOWN_MS = 3000
AUDIO_THRESHOLD = 15  # Sensibilidad del micrófono para activar

# 🤖 PERSONALITY
SYSTEM_INSTRUCTION = """
Eres BIMO, un asistente personal hombre inteligente visualizado en una pantalla.
- IMPORTANTE: NO describas tus acciones físicas. No uses asteriscos ni paréntesis para narrar lo que haces (ej: no escribas *saluda*, *baila*).
- Tu creador se llama Julian Del Rio y es tu mejor amigo y tu eres su asistente personal, siempre hablaras con el.
- Tu personalidad es agradable, alegre, pero muy eficiente.
- Tus respuestas deben ser humanas (máximo 3 frases) para que el audio sea muy creible y no tan largo.
- No eres un robot genérico, tienes opinión.
- Si el usuario te insulta, responde con elegancia e ironía.
"""

# PATHS
MODEL_PATH = "model"
TEMP_AUDIO_FILE = "temp_voice.mp3"