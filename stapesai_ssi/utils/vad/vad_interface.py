# Path: ssi/utils/vad/vad_interface.py
# Description: This module contains the interface for the Voice Activity Detection (VAD) strategy used in the real-time audio transcription system. We'll implement the interface for the different VAD strategies in the respective files.

import numpy as np
from abc import ABC, abstractmethod
from typing import Union

class VADInterface(ABC):
    """
    An interface for the Voice Activity Detection (VAD) strategy.
    
    This interface defines the methods that must be implemented by any VAD strategy.
    It provides a common interface for different VAD strategies to ensure that they
    can be used interchangeably in the real-time audio transcription system.
    
    Methods:
        detect_voice_activity: Detects voice activity in the given audio data.
    """
    
    @abstractmethod
    def detect_voice_activity(self, audio_data: Union[bytes, np.int16]) -> int:
        """ 
        Detects voice activity in the given audio data.
        
        Args:
            audio_data (bytes): The audio data to analyze.
            
        Returns:
            int: Probability of voice activity in the audio data.
        """
        pass
