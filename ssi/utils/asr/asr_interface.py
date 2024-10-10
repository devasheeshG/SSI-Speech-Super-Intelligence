# Path: ssi/utils/asr/asr_interface.py
# Description: This file will contain the interface for the ASR models. We'll impliment the interface for the different ASR models in the respective files.

from abc import ABC, abstractmethod
import numpy as np

class ASRInterface(ABC):
    @abstractmethod
    def load_model(self, model_path: str):
        pass
    
    @abstractmethod
    def transcribe(self, audio: np.ndarray) -> str:
        pass
