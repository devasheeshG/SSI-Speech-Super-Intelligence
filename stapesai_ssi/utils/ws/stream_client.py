# Path: ssi/utils/ws/stream_client.py
# Description: This module contains the StreamClient class for representing a connected WebSocket client for real-time audio transcription.

import asyncio
from typing import Callable
import numpy as np
from fastapi import WebSocket
from stapesai_ssi.utils.asr.asr_interface import ASRInterface
from stapesai_ssi.utils.vad.vad_factory import VADFactory
from stapesai_ssi.utils.asr.asr_factory import ASRFactory
from stapesai_ssi.config import get_settings
from stapesai_ssi.logger import get_logger
from stapesai_ssi.utils.vad.vad_interface import VADInterface
from stapesai_ssi.types.streaming_data_chunk import StreamingDataChunk

settings = get_settings()
logger = get_logger()

# Initialize VAD and ASR pipelines
vad_pipeline: VADInterface = VADFactory.create_vad_pipeline(settings.VAD_MODEL)
asr_pipeline: ASRInterface = ASRFactory.create_asr_pipeline(settings.ASR_MODEL)

class StreamClient:
    """Represents a connected WebSocket client for real-time audio transcription.

    Attributes:
        client_id (str): The unique identifier for the client.
        buffer (bytearray): A buffer to store incoming audio data.
    """

    def __init__(self, client_id: str, websocket: WebSocket, asr_callback: Callable) -> None:
        self.client_id: str = client_id
        self.websocket: WebSocket = websocket
        self.asr_callback: Callable = asr_callback
        self.audio_queue: asyncio.Queue = asyncio.Queue()
        self.is_running: bool = True
        
        # Initialize buffers
        # NOTE: check if we should use np.int16 or bytearray
        logger.debug(f"Initializing pre-buffer with {settings.BUFFER_SECONDS_BEFORE} seconds of silence")
        self.pre_buffer: np.ndarray = np.zeros(int(settings.BUFFER_SECONDS_BEFORE * settings.STREAM_SAMPLE_RATE), dtype=np.int16)
        
        logger.debug(f"Initializing post-buffer with {settings.BUFFER_SECONDS_AFTER} seconds of silence")
        self.post_buffer: np.ndarray = np.zeros(int(settings.BUFFER_SECONDS_AFTER * settings.STREAM_SAMPLE_RATE), dtype=np.int16)

    async def append_audio_data(self, audio_data: bytes) -> None:
        # Convert bytes to numpy array and put it in the queue
        audio_array = np.frombuffer(audio_data, dtype=np.int16)
        await self.audio_queue.put(audio_array)
    
    async def process_audio(self) -> None:
        recording_buffer = np.array([], dtype=np.int16)
        is_recording = False
        silence_duration = 0

        while self.is_running:
            audio_chunk = await self.audio_queue.get()

            # Update pre-buffer
            self.pre_buffer = np.roll(self.pre_buffer, -len(audio_chunk))
            self.pre_buffer[-len(audio_chunk):] = audio_chunk

            # Detect voice activity
            voice_prob = vad_pipeline.detect_voice_activity(audio_chunk)

            if voice_prob >= settings.VAD_THRESHOLD:
                if not is_recording:
                    logger.info(f"Voice activity detected for client {self.client_id}. Starting recording.")
                    is_recording = True
                    recording_buffer = np.concatenate((self.pre_buffer, audio_chunk))
                else:
                    recording_buffer = np.concatenate((recording_buffer, audio_chunk))
                silence_duration = 0
            elif is_recording:
                recording_buffer = np.concatenate((recording_buffer, audio_chunk))
                silence_duration += len(audio_chunk) / settings.STREAM_SAMPLE_RATE

                if silence_duration >= settings.BUFFER_SECONDS_AFTER:
                    logger.info(f"Silence detected for client {self.client_id}. Stopping recording and transcribing.")
                    is_recording = False

                    # Prepare the final audio for transcription
                    final_audio = np.concatenate((recording_buffer, self.post_buffer))

                    # Transcribe the audio
                    transcription = asr_pipeline.transcribe(final_audio)

                    # Send the transcription to the client
                    self.asr_callback(StreamingDataChunk(
                        language="en",  # Assuming English, you might want to make this configurable
                        transcription=transcription,
                        server_process_time=0.0  # You might want to add timing logic here
                    ))
                    logger.info(f"Transcription sent for client {self.client_id}: {transcription}")

                    # Clear the recording buffer
                    recording_buffer = np.array([], dtype=np.int16)
                    silence_duration = 0
            else:
                # Update post-buffer
                self.post_buffer = np.roll(self.post_buffer, -len(audio_chunk))
                self.post_buffer[-len(audio_chunk):] = audio_chunk

    async def receive_audio(self) -> None:
        try:
            while self.is_running:
                data = await self.websocket.receive_bytes()
                await self.append_audio_data(data)
        except asyncio.CancelledError:
            self.is_running = False
        except Exception as e:
            logger.error(f"Error receiving audio for client {self.client_id}: {e}")
            self.is_running = False

    async def run(self) -> None:
        logger.info(f"Creating tasks for client {self.client_id}")
        receive_task = asyncio.create_task(self.receive_audio())
        process_task = asyncio.create_task(self.process_audio())
        
        try:
            await asyncio.gather(receive_task, process_task)
        except Exception as e:
            import traceback
            logger.error(traceback.format_exc())
            logger.error(f"Error in run() for client {self.client_id}: {e}")
        finally:
            self.is_running = False
            receive_task.cancel()
            process_task.cancel()
            logger.info(f"Tasks cancelled for client {self.client_id}")
