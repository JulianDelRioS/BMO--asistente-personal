import cv2
import time
import os
import config

# Archivo temporal donde se guardará la foto
FOTO_TEMP = config.resource_path("temp_vision.jpg")

def tomar_foto():
    """Enciende la cámara, toma una foto, la muestra y la guarda."""
    print("👁️ BMO está intentando ver...")
    
    # 0 es la webcam por defecto
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("❌ ERROR: No se detecta ninguna cámara.")
        return None

    # Esperamos un poco para que la cámara enfoque luz
    time.sleep(1.5)

    ret, frame = cap.read()
    cap.release()
    
    if ret:
        # --- MODO ESPEJO: TE MUESTRA LO QUE VIO ---
        # Esto abrirá una ventana por 2 segundos para que sepas que funcionó
        try:
            cv2.imshow("VISIÓN DE BMO", frame)
            cv2.waitKey(2000) # Espera 2000 ms (2 segundos)
            cv2.destroyAllWindows()
        except Exception:
            pass # Si falla mostrar la ventana, no importa, seguimos
        # ------------------------------------------

        cv2.imwrite(FOTO_TEMP, frame)
        print(f"✅ Foto guardada: {FOTO_TEMP}")
        return FOTO_TEMP
    else:
        print("❌ ERROR: No salió la foto.")
        return None

def borrar_foto():
    """Borra la foto después de usarla para no llenar el disco."""
    if os.path.exists(FOTO_TEMP):
        try:
            os.remove(FOTO_TEMP)
            print("🗑️ Foto temporal borrada.")
        except Exception as e:
            print(f"⚠️ No se pudo borrar la foto: {e}")