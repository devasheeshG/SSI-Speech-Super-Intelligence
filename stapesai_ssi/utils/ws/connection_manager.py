# Path: ssi/utils/ws/connection_manager.py
# Description: This module contains the WebSocket connection manager for handling WebSocket connections for real-time audio transcription.

from typing import Callable, Dict
import uuid
from fastapi import WebSocket, status
from stapesai_ssi.utils.ws.stream_client import StreamClient
from stapesai_ssi.logger import get_logger
from stapesai_ssi.types.streaming_data_chunk import StreamingDataChunk

class ConnectionManager:
    def __init__(self, asr_callback: Callable[[StreamingDataChunk], None] = None) -> None:
        self.active_connections: Dict[str, StreamClient] = {}
        self.logger = get_logger()
        self.logger.info("ConnectionManager initialized")
        self.asr_callback = asr_callback

    async def connect(self, websocket: WebSocket) -> StreamClient:
        """
        Establish a new WebSocket connection and initialize client information.
        """
        client_id = str(uuid.uuid4())  # Generate a unique client_id
        client = StreamClient(client_id, websocket, self.asr_callback)
        await websocket.accept()
        self.active_connections[client_id] = client
        self.logger.info(f"WebSocket client {client_id} connected")

        return client

    async def disconnect(self, client_id: str):
        """
        Disconnect a WebSocket client and clean up resources.
        """
        client: StreamClient = self.active_connections.pop(client_id, None)
        if client:
            await client.websocket.close(code=status.WS_1001_GOING_AWAY)
            self.logger.info(f"WebSocket client {client_id} disconnected")
        else:
            self.logger.warning(f"Attempted to disconnect non-existent client {client_id}")