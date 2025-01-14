import sys
import cv2
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QHBoxLayout, QWidget
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QImage, QPixmap


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Configuración básica de la ventana
        self.setWindowTitle("Ventana con Cámara Web")
        self.setGeometry(0, 0, 1920, 1080)  # x, y, ancho, alto

        # Crear un layout vertical para organizar los contenedores
        main_layout = QVBoxLayout()

        # Crear un layout horizontal para organizar la cámara y el contenedor azul
        video_layout = QHBoxLayout()

        # Crear el contenedor de la cámara (video)
        self.video_label = QLabel()
        self.video_label.setAlignment(Qt.AlignCenter)
        self.video_label.setText("Aquí se mostrará el video de la cámara")
        self.video_label.setStyleSheet("background-color: black; color: white;")

        # Crear un contenedor azul al lado del video
        self.blue_container = QWidget()
        self.blue_container.setStyleSheet("background-color: blue;")
        self.blue_container.resize(300, 600)  # Establecer el tamaño del contenedor azul

        # Añadir los widgets al layout horizontal
        video_layout.addWidget(self.video_label)  # Añadir el video
        video_layout.addWidget(self.blue_container)  # Añadir el contenedor azul

        # Añadir el layout de video al layout principal
        main_layout.addLayout(video_layout)

        # Crear un contenedor para el botón y colocarlo en la parte inferior
        self.button = QPushButton("Activar cámara")
        self.button.clicked.connect(self.toggle_camera)
        main_layout.addWidget(self.button)

        # Crear un contenedor central y configurar el layout principal
        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

        # Configurar la cámara y el temporizador
        self.cap = None
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)

    def toggle_camera(self):
        if self.cap is None:
            # Iniciar la cámara
            self.cap = cv2.VideoCapture(0)
            if not self.cap.isOpened():
                self.video_label.setText("Error: No se pudo acceder a la cámara")
                return
            self.timer.start(30)  # Actualizar el video cada 30 ms
            self.button.setText("Desactivar cámara")
        else:
            # Detener la cámara
            self.timer.stop()
            self.cap.release()
            self.cap = None
            self.video_label.setText("Aquí se mostrará el video de la cámara")
            self.button.setText("Activar cámara")

    def update_frame(self):
        ret, frame = self.cap.read()
        if ret:
            # Convertir la imagen de BGR a RGB
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            # Convertir la imagen de OpenCV a un QImage
            height, width, channel = frame.shape
            bytes_per_line = channel * width
            q_img = QImage(frame.data, width, height, bytes_per_line, QImage.Format_RGB888)
            # Mostrar la imagen en el QLabel
            self.video_label.setPixmap(QPixmap.fromImage(q_img))
        else:
            self.video_label.setText("Error: No se pudo leer el frame de la cámara")


# Punto de entrada de la aplicación
if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Crear y mostrar la ventana principal
    window = MainWindow()
    window.show()

    # Ejecutar el bucle de eventos de la aplicación
    sys.exit(app.exec())
