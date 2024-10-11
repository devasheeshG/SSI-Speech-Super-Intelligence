# Path: ssi/utils/asr/asr_interface.py
# Description: This file will contain the interface for the ASR models. We'll impliment the interface for the different ASR models in the respective files.

from abc import ABC, abstractmethod
import numpy as np

class ASRInterface(ABC):
    """
    An interface for the Automatic Speech Recognition (ASR) model.
    
    This interface defines the methods that must be implemented by any ASR model.
    It provides a common interface for different ASR models to ensure that they
    can be used interchangeably in the real-time audio transcription system.
    
    Methods:
        - transcribe: Transcribes the given audio data into text.
    """
    
    @abstractmethod
    def transcribe(self, audio: bytearray) -> str:
        """
        Transcribe the given audio data.
        """
        pass
