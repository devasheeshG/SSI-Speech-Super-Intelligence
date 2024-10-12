# Path: ssi/config.py
# Description: This file contains code to load `.env` file and make a pydantic `BaseSettings` class which can be used to access environment variables in the application.

from functools import lru_cache
from typing import Union
from pydantic_settings import BaseSettings
from pydantic import Field, field_validator
from ssi.utils.whisper_language_codes import WHISPER_LANGUAGE_CODES

class Settings(BaseSettings):
    LOG_LEVEL: str = Field(
        default="INFO",
        env="LOG_LEVEL",
        description="The log level for the application.",
    )
    
    STREAM_SAMPLE_RATE: int = Field(
        default=16000,
        env="STREAM_SAMPLE_RATE",
        description="The sample rate of the audio stream which the client sends to the server.",
    )
    
    STREAM_CHANNELS: int = Field(
        default=1,
        env="STREAM_CHANNELS",
        description="The number of channels in the audio stream which the client sends to the server.",
    )
    @field_validator("STREAM_CHANNELS")
    def validate_stream_channels(cls, value):
        if value not in [1, 2]:
            raise ValueError("STREAM_CHANNELS must be 1 or 2.")
        if value == 2:
            raise ValueError("Stereo audio is not supported. Please use mono audio (1 channel).")
        return value
    
    STREAM_SAMPLE_WIDTH_BYTES: int = Field(
        default=2,
        env="STREAM_SAMPLE_WIDTH",
        description=(
            "The sample width of the audio stream which the client sends to the server. "
            "Example: 16-bit audio (2 bytes) (65,536 possible values). 1bit = 8 bytes."
        ),
    )
    
    # VAD
    VAD_MODEL: str = Field(
        default="silero",
        env="VAD_MODEL",
        description="The Voice Activity Detection (VAD) model to use for detecting voice activity.",
    )
    @field_validator("VAD_MODEL")
    def validate_vad_model(cls, value):
        if value not in ["silero"]:
            raise ValueError("Only 'silero' VAD model is supported.")
        return value
    
    VAD_MODEL_DOWNLOAD_DIR: Union[str, None] = Field(
        default=None,
        env="VAD_MODEL_DOWNLOAD_DIR",
        description="The directory to download the VAD model files.",
    )
    VAD_THRESHOLD: float = Field(
        default=0.70,
        env="VAD_THRESHOLD",
        description="The threshold value for voice activity detection.",
    )
    
    # in the final clip which will be sent to the ASR model, we need to include some audio before and after the detected speech to ensure that the ASR model can transcribe the speech accurately.
    BUFFER_SECONDS_BEFORE: float = Field(
        default=0.5,
        env="BUFFER_SECONDS_BEFORE",
        description="The number of seconds of audio before the detected speech to include in the final clip.",
    )
    BUFFER_SECONDS_AFTER: float = Field(
        default=1.0,
        env="BUFFER_SECONDS_AFTER",
        description="The number of seconds of audio after the detected speech to include in the final clip.",
    )

    # ASR
    ASR_MODEL: str = Field(
        default="whisper_transformers",
        env="ASR_MODEL",
        description="The Automatic Speech Recognition (ASR) model to use for speech recognition.",
    )
    @field_validator("ASR_MODEL")
    def validate_asr_model(cls, value):
        if value not in ["whisper_transformers"]:
            raise ValueError("ASR_MODEL must be 'whisper_transformers''.")
        return value
    
    ASR_MODEL_DOWNLOAD_DIR: Union[str, None] = Field(
        default=None,
        env="ASR_MODEL_DOWNLOAD_DIR",
        description="The directory to download the ASR model files.",
    )
    ASR_TARGET_LANG: str = Field(
        default="english",
        env="ASR_TARGET_LANG",
        description=(
            "The target language for speech recognition. "
            "You can specify the language code (e.g., 'english', 'hindi') or 'multilingual' for to output text in any language. "
            f"Available language codes: {', '.join(WHISPER_LANGUAGE_CODES.keys())}"
        ),
    )
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache
def get_settings():
    return Settings()
