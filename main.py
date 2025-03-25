from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from typing import Dict

app = FastAPI(title='Real-time Chat API')

connections: Dict[WebSocket, str] = {}

@app.websocket("/chat/")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()

    await websocket.send_text("Пожалуйста введите свое имя:")
    username = await websocket.receive_text()

    connections[websocket] = username

    try:
        for connection in connections:
            await connection.send_text(f'{username} вошел в чат!')

        while True:
            data = await websocket.receive_text()
            for connection in connections:
                await connection.send_text(f'{username}: {data}')
    except WebSocketDisconnect:
        connections.pop(websocket)

        for connection in connections:
            await connection.send_text(f"{username} вышел из чата.")
