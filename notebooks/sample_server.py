# Path: notebooks/sample_server.py
# Description: This script demonstrates how to create a simple FastAPI server.

import sys
sys.path.append('..')

from fastapi import FastAPI
from stapesai_ssi.fastapi import StreamingWSRouter
from stapesai_ssi.types import StreamingDataChunk, NewClientConnected
from stapesai_ssi.logger import get_logger

logger = get_logger()

app = FastAPI()

def asr_callback(data: StreamingDataChunk):
    logger.info("Received data chunk: %s", data)

def new_client_callback(data: NewClientConnected):
    logger.info("New client connected: %s", data)

streaming_ws_router = StreamingWSRouter(
    asr_callback=asr_callback,
    new_client_callback=new_client_callback,
    endpoint="/ws/transcribe"
)

app.include_router(streaming_ws_router)

# RUN: uvicorn sample_server:app --reload
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
