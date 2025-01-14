import cv2
# from ultralytics import YOLO



# Captura el video desde la cámara web (índice 0 para la cámara predeterminada)
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: No se pudo acceder a la cámara.")


while True:
    # Leer un frame de la cámara
    ret, frame = cap.read()

    if not ret:
        print("Error: No se pudo leer el frame de la cámara.")
        break

    # Mostrar el frame en una ventana
    cv2.imshow("Cámara Web", frame)

    # Salir si se presiona la tecla 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Liberar los recursos
cap.release()
cv2.destroyAllWindows()



