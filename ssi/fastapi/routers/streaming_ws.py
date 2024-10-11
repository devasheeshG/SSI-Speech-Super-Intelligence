# Path: ssi/fastapi/routers/streaming_ws.py
# Description: This file will contain the WebSocket endpoint for streaming ASR.

from fastapi import APIRouter, WebSocket
from fastapi.websockets import WebSocketDisconnect

from ssi.utils.ws.connection_manager import ConnectionManager
from ssi.utils.ws.stream_client import StreamClient
from ssi.utils.asr.asr_factory import ASRFactory
from ssi.utils.vad.vad_factory import VADFactory
from ssi.logger import get_logger

router = APIRouter()
logger = get_logger()
connection_manager = ConnectionManager()

vad_pipeline = VADFactory.create_vad_pipeline("silero")
asr_pipeline = ASRFactory.create_asr_pipeline("whisper")

@router.websocket("/ws/transcribe")
async def websocket_endpoint(websocket: WebSocket):
    """This is the second version of the WebSocket endpoint for real-time audio transcription.
    This supports voice activity detection (VAD) and streaming transcription.
    This is supposed to be integrated with other `Stapes AI` services internally.

    Args:
        websocket (WebSocket): The WebSocket connection
    """
    client: StreamClient = connection_manager.connect(websocket)

    try:
        while True:
            data = await websocket.receive_bytes()
            
            # Client can only send audio data (bytes)
            if not isinstance(data, bytes):
                logger.warning(f"WebSocket client {client.client_id} sent an invalid data type: {type(data)}")
                continue
            
            # Append audio data to the buffer
            client.append_audio_data(data)
            
            # this is synchronous, any async operation is in BufferingStrategy
            client.process_audio(
                websocket, vad_pipeline, asr_pipeline
            )

    except WebSocketDisconnect:
        logger.info(f"WebSocket client {client.client_id} disconnected due to WebSocket disconnect")

    except Exception as e:
        logger.error(f"An error occurred while processing WebSocket client {client.client_id}: {e}")

    finally:
        await connection_manager.disconnect(client.client_id)
