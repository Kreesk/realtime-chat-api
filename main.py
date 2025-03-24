from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from typing import List

app = FastAPI(title='Real-time Chat API')

connections: List[WebSocket] = []

@app.websocket("/chat/")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    connections.append(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            for connection in connections:
                await connection.send_text(f'Message: {data}')
    except WebSocketDisconnect:
        connections.remove(websocket)