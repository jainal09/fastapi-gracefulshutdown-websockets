import asyncio
from typing import Dict

from fastapi import WebSocket

from services.db_ops.flag_ops import read_flag
from services.kubernetes_services import get_pod_name


class ConnectionManager:
    """
    Connection Manager class to manage the WebSocket connections
    """
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}

    async def connect(self, websocket: WebSocket, id: str) -> None:
        """
        Connect the WebSocket
        Args:
            websocket: WebSocket
            id: Client ID
        Returns:
            None
        """
        if read_flag():  # Check if the flag is True for the server to accept connections
            await websocket.accept()
            await websocket.send_text(get_pod_name())
            self.active_connections[id] = websocket
        else:
            await websocket.close(code=1000)  # Close the connection without accepting

    def disconnect(self, id: str):
        """
        Disconnect the WebSocket
        Args:
            id: Client ID
        Returns:
            None
        """
        del self.active_connections[id]

    async def close_all_connections(self):
        """
        Close all the WebSocket connections
        Args:
            None
        Returns:
            None
        """
        for connection in list(self.active_connections.values()).copy():
            await connection.send_text("Server shutting down")
            await connection.close(code=1000)

    async def send_socket_message(self, message: str):
        """
        Send a message to all the WebSocket connections
        Args:
            message: Message to be sent
        Returns:
            None
        """
        for client_id, websocket in self.active_connections.items():
            await websocket.send_text(f"Client id {client_id} Message: {message}")

    async def wait_for_connections_to_close(self):
        """
        Wait for all the WebSocket connections to close
        Args:
            None
        Returns:
            None
        """
        while self.active_connections:
            await asyncio.sleep(1)  # Wait for connections to close
