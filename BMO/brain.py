from google import genai
from datetime import datetime
import time
import PIL.Image
import config
import eyes

# ==========================================
# 🧠 CONFIGURACIÓN
# ==========================================
try:
    client = genai.Client(api_key=config.API_KEY)
except Exception as e:
    print(f"❌ ERROR CLIENTE GEMINI: {e}")

MEMORY = []

# ==========================================
# 💾 GESTIÓN DE MEMORIA
# ==========================================
def add_memory(role, text):
    MEMORY.append({"role": role, "text": text})
    if len(MEMORY) > config.MAX_MEMORY:
        MEMORY.pop(0)

# ==========================================
# 🤔 PENSAMIENTO ROBUSTO
# ==========================================
def think(user_text, ruta_imagen=None):
    print("🌐 BMO is thinking...")

    # 1. Contexto
    hora_actual = datetime.now().strftime("%I:%M %p")
    fecha_actual = datetime.now().strftime("%d/%m/%Y")
    datos_sistema = f"INFORMACIÓN ACTUAL: Hoy es {fecha_actual} y son las {hora_actual}."

    # 2. Historial
    try:
        chat_history = "\n".join([f"{m['role']}: {m['text']}" for m in MEMORY])
    except Exception:
        MEMORY.clear()
        chat_history = ""

    full_prompt = config.SYSTEM_INSTRUCTION + "\n\n" + datos_sistema + "\n\nHistory:\n" + chat_history + f"\n\nUser: {user_text}"
    
    contenido = [full_prompt]

    if ruta_imagen:
        print("🖼️ ¡Procesando imagen con IA!")
        try:
            img = PIL.Image.open(ruta_imagen)
            contenido.append(img)
        except Exception as e:
            print(f"⚠️ Error cargando imagen: {e}")

    # 3. Enviar a Google (Con PACIENCIA para error 429)
    max_intentos = 3
    
    for intento in range(max_intentos):
        try:
            # Intentamos usar el modelo 2.0. Si falla mucho, cambia a "gemini-1.5-flash"
            response = client.models.generate_content(
                model="gemini-2.0-flash", 
                contents=contenido
            )
            
            reply = response.text.strip()
            add_memory("BMO", reply)
            
            if ruta_imagen:
                eyes.borrar_foto()
                
            return reply

        except Exception as e:
            error_str = str(e)
            print(f"⚠️ Error intento {intento+1}/{max_intentos}: {error_str}")
            
            # --- LÓGICA DE ESPERA MEJORADA ---
            
            # Error 429: Cuota excedida (Velocidad)
            if "429" in error_str or "RESOURCE_EXHAUSTED" in error_str:
                print("⏳ Límite de velocidad alcanzado. Esperando 30 segundos para enfriar...")
                time.sleep(30) # Espera larga para que Google nos perdone
            
            # Error 503: Servidor caído momentáneamente
            elif "503" in error_str or "UNAVAILABLE" in error_str:
                print("⏳ Servidor ocupado. Esperando 5 segundos...")
                time.sleep(5)
                
            else:
                # Otros errores (404, etc), no tiene caso reintentar
                break
    
    return "Lo siento Julián, estoy un poco mareado por tanta información visual. ¿Podemos intentar de nuevo en un minuto?"