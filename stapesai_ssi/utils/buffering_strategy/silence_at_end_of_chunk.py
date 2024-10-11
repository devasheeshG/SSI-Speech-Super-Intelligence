# Path: ssi/utils/buffering_strategy/silence_at_end_of_chunk.py
# Description: This module contains the SilenceAtEndOfChunk buffering strategy class. In this strategy, the audio chunks are buffered until a period of silence is detected at the end of the chunk. This is done by using VAD to detect the presence of speech in the audio data.

from fastapi import WebSocket
from stapesai_ssi.utils.buffering_strategy.buffering_strategy_interface import BufferingStrategyInterface
from stapesai_ssi.utils.vad.vad_interface import VADInterface
from stapesai_ssi.utils.asr.asr_interface import ASRInterface
from stapesai_ssi.utils.ws.stream_client import StreamClient
from stapesai_ssi.config import get_settings
from stapesai_ssi.logger import get_logger

settings = get_settings()
logger = get_logger()

class SilenceAtEndOfChunk(BufferingStrategyInterface):
    """
    A buffering strategy that processes audio at the end of each chunk with
    silence detection.

    This class is responsible for handling audio chunks, detecting silence at
    the end of each chunk, and initiating the transcription process for the
    chunk.

    Attributes:
        client (StreamClient): The client instance associated with this buffering strategy.
    """
    
    def __init__(self, client: StreamClient) -> None:
        self.client: StreamClient = client
        self.is_recording = False
        self.pre_buffer = bytearray()
        self.recording_buffer = bytearray()
        self.post_buffer = bytearray()
        self.silence_duration = 0
        self.processing_flag = False
        
    async def process_audio(
        self, 
        websocket: WebSocket,
        vad_pipeline: VADInterface,
        asr_pipeline: ASRInterface
    ) -> None:
        raise NotImplementedError("process_audio method must be implemented in subclass")
