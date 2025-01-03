import asyncio
import websockets
import json

# Función para manejar conexiones entrantes
async def handle_connection(websocket, path):
    print(f"Cliente conectado desde: {websocket.remote_address}")
    try:
        async for message in websocket:
            print(f"Mensaje recibido: {message.strip()}")
            
            # Crear un mensaje de respuesta en formato JSON
            response_data = {
                "status": "ok",
                "received": message.strip(),
                "message": "¡Hola desde el servidor!",
            }
            
            # Convertir el mensaje a formato JSON y enviarlo
            response_json = json.dumps(response_data)
            await websocket.send(response_json)
    except websockets.exceptions.ConnectionClosed as e:
        print(f"Conexión cerrada: {e}")
    except Exception as e:
        print(f"Error: {e}")

# Dirección del servidor y puerto
SERVER_ADDRESS = "192.168.1.84"  # Cambia a la IP de tu servidor
SERVER_PORT = 8765               # Puerto del servidor

# Función principal para iniciar el servidor
async def main():
    print(f"Iniciando servidor WebSocket en ws://{SERVER_ADDRESS}:{SERVER_PORT}")
    # Crear el servidor WebSocket
    async with websockets.serve(handle_connection, SERVER_ADDRESS, SERVER_PORT):
        await asyncio.Future()  # Mantener el servidor corriendo

# Ejecutar el servidor
if __name__ == "__main__":
    asyncio.run(main())
