# brain.py
from google import genai
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
        
        # Build context
        chat_history = "\n".join(MEMORY)
        full_prompt = f"{config.SYSTEM_INSTRUCTION}\n\nHistory:\n{chat_history}\n\nUser: {user_text}\nBMO:"

        response = client.models.generate_content(
            model="gemini-2.0-flash", # Usamos flash por velocidad
            contents=full_prompt
        )
        
        reply = response.text.strip()
        add_memory("BMO", reply)
        return reply

    except Exception as e:
        print(f"❌ BRAIN ERROR: {e}")
        return "Lo siento, tuve un error de conexión."