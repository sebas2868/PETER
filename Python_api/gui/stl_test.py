import sys
import vtk
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor

class STLViewer(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Visor de Archivos STL")
        self.setGeometry(100, 100, 1360, 720)

        # Crear el layout principal
        layout = QVBoxLayout()

        # Crear un contenedor para el visor VTK (QWidget)
        self.render_widget = QWidget(self)  # Este será el widget de Qt donde se renderiza VTK
        layout.addWidget(self.render_widget)

        # Crear un contenedor central
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        # Configurar VTK para visualizar
        self.renderer = vtk.vtkRenderer()
        self.renderer.SetBackground(0.1, 0.1, 0.1)  # Fondo oscuro

        # Crear un interactor de VTK, pero sin una ventana de renderizado separada
        self.iren = QVTKRenderWindowInteractor(self.render_widget)
        self.iren.GetRenderWindow().AddRenderer(self.renderer)

        # Ruta del archivo STL
        self.stl_file_path = "gui/assets/My dear friend.stl"  # Cambiar esta ruta a tu archivo STL

        # Cargar el archivo STL directamente al iniciar
        self.load_stl()

        # Pedir los valores de orientación por la terminal
        self.get_orientation_from_terminal()

    def load_stl(self):
        file_path = self.stl_file_path

        if file_path:
            print(f"Cargando archivo STL: {file_path}")
            # Usar el lector de STL de VTK
            reader = vtk.vtkSTLReader()
            reader.SetFileName(file_path)

            # Crear un mapper y actor para visualizar la malla
            self.mapper = vtk.vtkPolyDataMapper()
            self.mapper.SetInputConnection(reader.GetOutputPort())
            self.actor = vtk.vtkActor()
            self.actor.SetMapper(self.mapper)

            # Añadir el actor al renderer
            self.renderer.AddActor(self.actor)
            self.renderer.ResetCamera()

            # Iniciar el interactivo para visualizar la malla
            self.iren.Initialize()
            self.iren.Start()

    def get_orientation_from_terminal(self):
        # Pedir valores de Roll, Pitch y Yaw al usuario en la terminal
        try:
            roll = float(input("Introduce el valor de Roll (-180 a 180): "))
            pitch = float(input("Introduce el valor de Pitch (-180 a 180): "))
            yaw = float(input("Introduce el valor de Yaw (-180 a 180): "))

            # Ajustar la orientación del objeto
            self.update_orientation(roll, pitch, yaw)
        except ValueError:
            print("Por favor ingresa un valor numérico válido.")

    def update_orientation(self, roll, pitch, yaw):
        # Ajustar la orientación del actor con los valores recibidos
        self.actor.SetOrientation(roll+90, pitch, yaw+180)
        self.iren.Render()

# Punto de entrada de la aplicación
if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Crear y mostrar la ventana principal
    window = STLViewer()
    window.show()

    # Ejecutar el bucle de eventos de la aplicación
    sys.exit(app.exec())
