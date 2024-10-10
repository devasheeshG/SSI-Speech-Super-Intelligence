# Path: ssi/utils/asr/asr_factory.py
# Description: This file will contain the factory class for the ASR models.

from .whisper_asr import WhisperASR

class ASRFactory:
    @staticmethod
    def get_asr(model_name: str):
        if model_name == "whisper":
            return WhisperASR()
        else:
            raise ValueError("Invalid model name")
