# Path: ssi/utils/ws/connection_manager.py
# Description: This module contains the WebSocket connection manager for handling WebSocket connections for real-time audio transcription.

from typing import Dict, Tuple, Union
import uuid
from fastapi import WebSocket, status

from ssi.utils.ws.stream_client import StreamClient
from ssi.logger import get_logger

class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}
        self.logger = get_logger()
        self.logger.info("ConnectionManager initialized")

    async def connect(self, websocket: WebSocket) -> StreamClient:
        """
        Establish a new WebSocket connection and initialize client information.
        """
        client_id = str(uuid.uuid4())  # Generate a unique client_id
        client = StreamClient(client_id)
        await websocket.accept()
        self.active_connections[client_id] = client
        self.logger.info(f"WebSocket client {client_id} connected")

        return client

    async def disconnect(self, client_id: str):
        """
        Disconnect a WebSocket client and clean up resources.
        """
        client = self.active_connections.pop(client_id)
        await client.websocket.close()
        self.logger.info(f"WebSocket client {client_id} disconnected")
