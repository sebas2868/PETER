from fastapi import FastAPI, WebSocket
import json

app = FastAPI()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()  # Aceptar la conexión
    print("Cliente conectado")
    
    # Enviar mensaje de confirmación al cliente inmediatamente
    confirmation_message = {"status": "ok", "message": "CONFIRMATION"}
    await websocket.send_text(json.dumps(confirmation_message))
    print("Mensaje de confirmación enviado al cliente.")

    try:
        while True:
            # Recibir mensaje del cliente
            data = await websocket.receive_text()
            try:
                message = json.loads(data)  # Decodificar mensaje JSON
                print(f"Mensaje recibido: {message}")
                
                # Procesar y responder con JSON
                response = {
                    "status": "ok",
                    "echo": message,
                    "message": "Este es un mensaje de respuesta JSON desde el servidor."
                }
                await websocket.send_text(json.dumps(response))  # Enviar respuesta en formato JSON
            except json.JSONDecodeError:
                print("Mensaje recibido no es un JSON válido.")
                error_response = {"error": "El mensaje no es un JSON válido."}
                await websocket.send_text(json.dumps(error_response))
    except Exception as e:
        print(f"Cliente desconectado: {e}")
