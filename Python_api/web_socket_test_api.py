from fastapi import FastAPI, WebSocket
import json

app = FastAPI()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()  # Aceptar la conexión
    print("Cliente conectado")
    estado = 0

    try:
        while True:
            # Recibir mensaje del cliente
            data = await websocket.receive_text()
            try:
                message_json = json.loads(data)  # Decodificar mensaje JSON
                if estado == 0:
                    if "device" in message_json:
                        message = message_json["device"]

                        if message == "ESP32":                                   
                         estado =1


                elif estado==1:
                    print("conexion establecida con esp32")

            except json.JSONDecodeError:
                print("Mensaje recibido no es un JSON válido.")
                error_response = {"error": "El mensaje no es un JSON válido."}
                await websocket.send_text(json.dumps(error_response))
    except Exception as e:
        print(f"Cliente desconectado: {e}")
