import serial
import json
import math
import matplotlib.pyplot as plt

def calculate_coordinates(angle, distance):
    """
    Convierte un ángulo y una distancia en coordenadas cartesianas (x, y).
    """
    radians = math.radians(angle)
    x = distance * math.cos(radians)
    y = distance * math.sin(radians)
    return x / 100, y / 100  # Escalar a metros

# Configuración del puerto serial
SERIAL_PORT = '/dev/ttyUSB0'  # Cambia esto según tu puerto
BAUD_RATE = 115200

# Variables globales para almacenar coordenadas
laser_1 = []
laser_2 = []
max_dis = 500  # (mm)

# Conexión al puerto serial
try:
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
    print(f"Conectado al puerto {SERIAL_PORT}")
except Exception as e:
    print(f"Error al conectar con el puerto {SERIAL_PORT}: {e}")
    exit()

def process_serial_data():
    """
    Lee datos del puerto serial, los interpreta como JSON, y los almacena en listas.
    """
    global laser_1, laser_2
    try:
        line = ser.readline().decode('utf-8', errors='ignore').strip()
        if line:
            try:
                # Interpretar el mensaje como JSON
                data = json.loads(line)

                # Limpiar datos anteriores
                laser_1.clear()
                laser_2.clear()

                # Procesar lecturas del JSON
                if "laser_1" in data:
                    for reading in data["laser_1"]:
                        angle = reading["angle"]
                        distance = reading["distance"]
                        if distance < max_dis:  # Filtrar por distancia
                            x, y = calculate_coordinates(angle, distance)
                            laser_1.append((x, y))  # Agregar como tupla

                if "laser_2" in data:
                    for reading in data["laser_2"]:
                        angle = reading["angle"]
                        distance = reading["distance"]
                        if distance < max_dis:  # Filtrar por distancia
                            x, y = calculate_coordinates(angle, distance)
                            laser_2.append((x, y))  # Agregar como tupla

            except json.JSONDecodeError:
                pass
    except Exception as e:
        print(f"Error en la lectura de datos seriales: {e}")

def plot_data():
    """
    Graficar los datos en tiempo real.
    """
    global laser_1, laser_2

    plt.ion()  # Modo interactivo
    fig, ax = plt.subplots()
    scatter = ax.scatter([], [], c='blue', s=10)
    ax.set_xlim(-8, 8)
    ax.set_ylim(-8, 8)
    ax.set_title("Coordenadas en Tiempo Real")
    ax.set_xlabel("X (10*cm)")
    ax.set_ylabel("Y (10*cm)")

    try:
        while True:
            try:
                # Procesar datos seriales
                process_serial_data()

                # Combinar puntos de laser_1 y laser_2
                puntos = laser_1+ laser_2[::-1]

                # Actualizar la gráfica si hay puntos
                if puntos:
                    scatter.set_offsets(puntos)
                else:
                    scatter.set_offsets([])  # Limpia la gráfica si no hay puntos

                plt.pause(0.05)  # Pausa breve para actualizar la gráfica
            except:
                pass
    except KeyboardInterrupt:
        print("Saliendo...")
        plt.close()
        ser.close()

# Ejecutar el programa
plot_data()
