# Path: ssi/utils/asr/whisper_transformers_asr.py
# Description: This module contains the WhisperTransformersASR class, which is an implementation of the ASRInterface using the Hugging Face Transformers library.

from stapesai_ssi.utils.asr.asr_interface import ASRInterface

class WhisperTransformersASR(ASRInterface):
    """
    An ASR model implementation using the Hugging Face Transformers library.
    
    This class provides an implementation of the ASRInterface using the
    Hugging Face Transformers library. It transcribes audio data into text
    using a pre-trained transformer model.
    """
    
    def __init__(self):
        pass
    
    def transcribe(self, audio: bytearray) -> str:
        return "test transcription"
