# Path: ssi/utils/buffering_strategy/silence_at_end_of_chunk.py
# Description: This module contains the SilenceAtEndOfChunk buffering strategy class. In this strategy, the audio chunks are buffered until a period of silence is detected at the end of the chunk. This is done by using VAD to detect the presence of speech in the audio data.

from fastapi import WebSocket
from ssi.utils.buffering_strategy.buffering_strategy_interface import BufferingStrategyInterface
from ssi.utils.vad.vad_interface import VADInterface
from ssi.utils.asr.asr_interface import ASRInterface
from ssi.utils.ws.stream_client import StreamClient
from ssi.config import get_settings
from ssi.logger import get_logger

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
        self.silence_counter = 0
        self.recorded_audio = bytearray()
        
    async def process_audio(
        self, 
        websocket: WebSocket,
        vad_pipeline: VADInterface,
        asr_pipeline: ASRInterface
    ) -> None:
        audio_data = self.client.pre_buffer + self.client.post_buffer
        voice_prob = vad_pipeline.detect_voice_activity(audio_data)

        if voice_prob >= settings.VAD_THRESHOLD:
            if not self.is_recording:
                logger.info(f"Voice activity detected for client {self.client.client_id}. Starting recording.")
                self.is_recording = True
                self.recorded_audio = self.client.pre_buffer.copy()
            
            self.recorded_audio.extend(self.client.post_buffer)
            self.silence_counter = 0
        elif self.is_recording:
            self.silence_counter += 1
            self.recorded_audio.extend(self.client.post_buffer)

            if self.silence_counter >= int(settings.BUFFER_SECONDS_AFTER * settings.STREAM_SAMPLE_RATE / len(self.client.post_buffer)):
                logger.info(f"Silence detected for client {self.client.client_id}. Stopping recording and transcribing.")
                self.is_recording = False
                
                # Transcribe the audio data
                transcription = asr_pipeline.transcribe(self.recorded_audio)
                
                # Send the transcription to the client
                await websocket.send_json({"transcription": transcription})
                
                # Clear the recorded audio
                self.recorded_audio = bytearray()
                self.silence_counter = 0

        # Clear the post buffer after processing
        self.client.post_buffer.clear()
