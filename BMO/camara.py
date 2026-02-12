import cv2

print("Probando cámara...")

# El '0' suele ser la webcam integrada. 
# Si no funciona, prueba cambiarlo por 1 o 2.
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("❌ Error: No se pudo abrir la cámara.")
else:
    print("✅ Cámara detectada. Presiona 'q' para salir.")

while True:
    ret, frame = cap.read()
    if not ret:
        print("Error al leer frame")
        break

    # Mostrar lo que ve la cámara en una ventana
    cv2.imshow('Prueba de Ojos BMO', frame)

    # Salir con la tecla 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()