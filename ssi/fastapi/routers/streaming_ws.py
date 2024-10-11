# Path: ssi/fastapi/routers/streaming_ws.py
# Description: This file will contain the WebSocket endpoint for streaming ASR.

from fastapi import APIRouter, WebSocket
from fastapi.websockets import WebSocketDisconnect
from typing import Callable
from ssi.utils.ws.connection_manager import ConnectionManager
from ssi.utils.ws.stream_client import StreamClient
from ssi.logger import get_logger
from ssi.types.streaming_data_chunk import StreamingDataChunk
from ssi.types.new_client_connected import NewClientConnected

class StreamingWSRouter(APIRouter):
    def __init__(
        self,
        asr_callback: Callable[[StreamingDataChunk], None],
        new_client_callback: Callable[[NewClientConnected], None],
        endpoint: str = "/ws/transcribe"
    ):
        super().__init__()
        self.logger = get_logger()
        self.connection_manager = ConnectionManager(asr_callback)
        self.new_client_callback = new_client_callback
        self.add_api_route(endpoint, self.websocket_endpoint, methods=["websocket"])

    async def websocket_endpoint(self, websocket: WebSocket):
        client: StreamClient = await self.connection_manager.connect(websocket)
        self.new_client_callback(NewClientConnected(client_id=client.client_id))

        try:
            await client.run()
        except WebSocketDisconnect:
            self.logger.info(f"WebSocket client {client.client_id} disconnected due to WebSocket disconnect")
        except Exception as e:
            self.logger.error(f"An error occurred while processing WebSocket client {client.client_id}: {e}")
        finally:
            await self.connection_manager.disconnect(client.client_id)
