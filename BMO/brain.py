from google import genai
from datetime import datetime  # <--- NUEVO IMPORT
import config

# Init Client
client = genai.Client(api_key=config.API_KEY)

# Local Memory
MEMORY = []

def add_memory(role, text):
    """Adds message to history keeping the limit."""
    MEMORY.append(f"{role}: {text}")
    if len(MEMORY) > config.MAX_MEMORY:
        MEMORY.pop(0)

def think(user_text):
    """Sends prompt to Gemini and gets response."""
    try:
        print("🌐 BMO is thinking...")
        
        # 1. OBTENER HORA DEL SISTEMA
        # Formato ejemplo: "07:30 PM"
        hora_actual = datetime.now().strftime("%I:%M %p")
        fecha_actual = datetime.now().strftime("%d/%m/%Y")
        
        # 2. CONSTRUIR CONTEXTO TEMPORAL
        # Le decimos a BMO qué hora es "ahora mismo"
        datos_sistema = f"INFORMACIÓN ACTUAL: Hoy es {fecha_actual} y son las {hora_actual}."
        
        # 3. CONSTRUIR PROMPT
        chat_history = "\n".join(MEMORY)
        
        # Insertamos la hora dentro del prompt
        full_prompt = f"{config.SYSTEM_INSTRUCTION}\n\n{datos_sistema}\n\nHistory:\n{chat_history}\n\nUser: {user_text}\nBMO:"

        response = client.models.generate_content(
            model="gemini-2.0-flash", 
            contents=full_prompt
        )
        
        reply = response.text.strip()
        add_memory("BMO", reply)
        return reply

    except Exception as e:
        print(f"❌ BRAIN ERROR: {e}")
        return "Lo siento, mis circuitos temporales fallaron."