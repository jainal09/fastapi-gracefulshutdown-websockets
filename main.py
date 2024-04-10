import asyncio
import os

from api.api import api_router
from fastapi import WebSocket, WebSocketDisconnect
from handlers.signal_handler import SignalHandler
from services.db_ops.flag_ops import create_or_update_flag, read_flag
from settings import settings_config

print(f"Process id {os.getpid()}")
create_or_update_flag(True)

app = settings_config.app
signal_handler = SignalHandler()
queue = settings_config.queue
manager = settings_config.manager
server = settings_config.server

app.include_router(api_router)


@app.on_event("startup")
def chain_signals() -> None:
    signal_handler.register_signal_handler()


@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str) -> None:
    await manager.connect(websocket, client_id)
    if read_flag():
        try:
            while True:
                await websocket.receive_text()

        except WebSocketDisconnect:
            manager.disconnect(client_id)


if __name__ == "__main__":
    try:
        server.run()
    except asyncio.CancelledError:
        pass
