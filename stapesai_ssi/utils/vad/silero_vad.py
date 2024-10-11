# Path: ssi/utils/vad/silero_vad.py
# Description: This module contains the implementation of the Silero VAD strategy for detecting voice activity in audio data.

from typing import Union
import torch
import numpy as np
from .vad_interface import VADInterface
from stapesai_ssi.config import get_settings

settings = get_settings()

class SileroVAD(VADInterface):
    def __init__(self):
        if settings.VAD_MODEL_DOWNLOAD_DIR:
            torch.hub.set_dir(settings.VAD_MODEL_DOWNLOAD_DIR)

        self.model, _ = torch.hub.load(
            repo_or_dir='snakers4/silero-vad',
            model='silero_vad',
            force_reload=True
        )
    
    def _get_probs(self, model, inputs: torch.Tensor, sample_rate: int):
        with torch.no_grad():
            outs = model(inputs, sample_rate)
        return outs.item()

    def _int2float(self, sound):
        abs_max = np.abs(sound).max()
        sound = sound.astype('float32')
        if abs_max > 0:
            sound *= 1/32768
        sound = sound.squeeze()  # depends on the use case
        return sound
    
    def detect_voice_activity(self, audio_data: Union[bytes, np.int16]) -> int:
        if isinstance(audio_data, bytes):
            audio_data = np.frombuffer(audio_data, dtype=np.int16)
        audio_data = self._int2float(audio_data)
        audio_tensor = torch.tensor(audio_data)
        return self._get_probs(self.model, audio_tensor, 16_000)
