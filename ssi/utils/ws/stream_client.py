# Path: ssi/utils/ws/stream_client.py
# Description: This module contains the StreamClient class for representing a connected WebSocket client for real-time audio transcription.

from fastapi import WebSocket
from ssi.utils.buffering_strategy.buffering_strategy_factory import BufferingStrategyFactory
from ssi.utils.vad.vad_interface import VADInterface
from ssi.utils.asr.asr_interface import ASRInterface
from ssi.config import get_settings

settings = get_settings()

class StreamClient:
    """Represents a connected WebSocket client for real-time audio transcription.

    Attributes:
        client_id (str): The unique identifier for the client.
        buffer (bytearray): A buffer to store incoming audio data.
    """

    def __init__(self, client_id: str) -> None:
        self.client_id = client_id
        self.pre_buffer = bytearray()
        self.post_buffer = bytearray()
        self.processing_strategy = 'silence_at_end_of_chunk'
        self.buffering_strategy = (
            BufferingStrategyFactory.create_buffering_strategy(
                type=self.processing_strategy,
                client=self,
            )
        )

    def append_audio_data(self, audio_data: bytes) -> None:
        """Append audio data to the buffer.

        Args:
            audio_data (bytes): The audio data to append to the buffer.
        """
        BUFFER_BEFORE_SIZE = int(settings.BUFFER_SECONDS_BEFORE * settings.STREAM_SAMPLE_RATE * settings.STREAM_SAMPLE_WIDTH_BYTES * settings.STREAM_CHANNELS)
        BUFFER_AFTER_SIZE = int(settings.BUFFER_SECONDS_AFTER * settings.STREAM_SAMPLE_RATE * settings.STREAM_SAMPLE_WIDTH_BYTES * settings.STREAM_CHANNELS)
        
        self.post_buffer.extend(audio_data)
        
        if len(self.pre_buffer) < BUFFER_BEFORE_SIZE:
            self.pre_buffer.extend(audio_data)
        else:
            self.pre_buffer = self.pre_buffer[len(audio_data):] + audio_data
        
        if len(self.post_buffer) > BUFFER_AFTER_SIZE:
            self.post_buffer = self.post_buffer[-BUFFER_AFTER_SIZE:]
    
    def process_audio(
        self, 
        websocket: WebSocket,
        vad_pipeline: VADInterface,
        asr_pipeline: ASRInterface,
    ) -> None:
        """Process the audio data using the specified VAD and ASR pipelines.

        Args:
            vad_pipeline: The VAD pipeline to use for voice activity detection.
            asr_pipeline: The ASR pipeline to use for speech recognition.
        """
        self.buffering_strategy.process_audio(
            websocket, vad_pipeline, asr_pipeline
        )
