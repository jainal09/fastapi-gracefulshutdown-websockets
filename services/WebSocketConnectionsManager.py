import asyncio
from typing import Dict

from fastapi import WebSocket

from services.db_ops.flag_ops import read_flag


class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}

    async def connect(self, websocket: WebSocket, id: str):
        print(read_flag())
        if read_flag():
            await websocket.accept()
            self.active_connections[id] = websocket
        else:
            await websocket.close(code=1000)  # Close the connection without accepting

    def disconnect(self, id: str):
        del self.active_connections[id]

    async def close_all_connections(self):
        for connection in list(self.active_connections.values()).copy():
            await connection.send_text("Server shutting down")
            await connection.close(code=1000)

    async def send_personal_message(self, message: str):
        for client_id, websocket in self.active_connections.items():
            await websocket.send_text(f"Client id {client_id} Message: {message}")

    async def wait_for_connections_to_close(self):
        while self.active_connections:
            await asyncio.sleep(1)  # Wait for connections to close
