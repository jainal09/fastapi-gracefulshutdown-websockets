import uvicorn
from fastapi import FastAPI
from services.WebSocketConnectionsManager import ConnectionManager
from uvicorn.config import Config


class Settings:
    """
    Settings class to store the configuration
    """
    manager = ConnectionManager()
    app = FastAPI()
    queue = []
    # Define the host and port
    host = "0.0.0.0"
    port = 8000
    # Create a Uvicorn server instance
    server = uvicorn.Server(Config(app=app, host=host, port=port))


# forcing only 1 instance of the class
settings_config = Settings()
