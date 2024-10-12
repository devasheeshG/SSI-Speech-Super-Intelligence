# Path: ssi/types/streaming_data_chunk.py
# Description: This module contains the StreamingDataChunk pydantic model, which represents a chunk of streaming data.

from pydantic import BaseModel

class StreamingDataChunk(BaseModel):
    """
    """
    language: str
    transcription: str
    server_process_time: float
