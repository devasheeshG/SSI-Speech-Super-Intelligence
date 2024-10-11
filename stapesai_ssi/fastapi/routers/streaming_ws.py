# Path: ssi/fastapi/routers/streaming_ws.py
# Description: This file will contain the WebSocket endpoint for streaming ASR.

import logging
from fastapi import APIRouter, WebSocket
from fastapi.websockets import WebSocketDisconnect
from typing import Callable
from stapesai_ssi.utils.ws.connection_manager import ConnectionManager
from stapesai_ssi.utils.ws.stream_client import StreamClient
from stapesai_ssi.logger import get_logger
from stapesai_ssi.types.streaming_data_chunk import StreamingDataChunk
from stapesai_ssi.types.new_client_connected import NewClientConnected

class StreamingWSRouter(APIRouter):
    def __init__(
        self,
        asr_callback: Callable[[StreamingDataChunk], None],
        new_client_callback: Callable[[NewClientConnected], None],
        endpoint: str = "/ws/transcribe",
        *args, **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.logger = get_logger(logging.INFO)
        self.connection_manager = ConnectionManager(asr_callback)
        self.new_client_callback = new_client_callback
        self.add_websocket_route(endpoint, self.websocket_endpoint)
        self.logger.info(f"StreamingWSRouter initialized with endpoint: {endpoint}")

    async def websocket_endpoint(self, websocket: WebSocket):
        client: StreamClient = await self.connection_manager.connect(websocket)
        self.logger.info(f"New WebSocket connection established: {client.client_id}")
        self.new_client_callback(NewClientConnected(client_id=client.client_id))

        try:
            self.logger.info(f"Starting StreamClient run for {client.client_id}")
            await client.run()
        except WebSocketDisconnect:
            self.logger.info(f"WebSocket client {client.client_id} disconnected due to WebSocket disconnect")
        except Exception as e:
            self.logger.error(f"An error occurred while processing WebSocket client {client.client_id}: {e}")
        finally:
            self.logger.info(f"Disconnecting client {client.client_id}")
            await self.connection_manager.disconnect(client.client_id)
