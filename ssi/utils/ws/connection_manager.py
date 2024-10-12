# Path: ssi/utils/ws/connection_manager.py
# Description: This module contains the WebSocket connection manager for handling WebSocket connections for real-time audio transcription.

from typing import Callable, Dict
import uuid
from fastapi import WebSocket, status
from ssi.utils.ws.stream_client import StreamClient
from ssi.logger import get_logger
from ssi.config import get_settings
from ssi.utils.asr.asr_interface import ASRInterface
from ssi.utils.vad.vad_factory import VADFactory
from ssi.utils.asr.asr_factory import ASRFactory
from ssi.utils.vad.vad_interface import VADInterface
from ssi.types.streaming_data_chunk import StreamingDataChunk

class ConnectionManager:
    def __init__(self, asr_callback: Callable[[StreamingDataChunk], None] = None) -> None:
        self.active_connections: Dict[str, StreamClient] = {}
        self.logger = get_logger()
        self.logger.info("ConnectionManager initialized")
        self.asr_callback = asr_callback
        self.settings = get_settings()
        
        # Initialize VAD and ASR pipelines
        self.vad_pipeline: VADInterface = VADFactory.create_vad_pipeline(self.settings.VAD_MODEL)
        self.asr_pipeline: ASRInterface = ASRFactory.create_asr_pipeline(self.settings.ASR_MODEL)

    async def connect(self, websocket: WebSocket) -> StreamClient:
        """
        Establish a new WebSocket connection and initialize client information.
        """
        client_id = str(uuid.uuid4())  # Generate a unique client_id
        client = StreamClient(client_id, websocket, self.asr_callback, self.vad_pipeline, self.asr_pipeline)
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