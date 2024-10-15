# Path: ssi/utils/asr/whisper_transformers_asr.py
# Description: This module contains the WhisperTransformersASR class, which is an implementation of the ASRInterface using the Hugging Face Transformers library.

import numpy as np
import torch
import torch.nn.functional as F
from transformers import (
    WhisperForConditionalGeneration,
    WhisperProcessor,
    WhisperConfig,
)
import soundfile as sf
from ssi.utils.asr.asr_interface import ASRInterface
from ssi.utils.whisper_language_codes import WHISPER_LANGUAGE_CODES
from ssi.logger import get_logger
from ssi.config import get_settings

class WhisperTransformersASR(ASRInterface):
    """
    An ASR model implementation using the Hugging Face Transformers library.
    
    This class provides an implementation of the ASRInterface using the
    Hugging Face Transformers library. It transcribes audio data into text
    using a pre-trained transformer model.
    """
    
    def __init__(self):
        self.logger = get_logger()
        self.settings = get_settings()
        self.model_name = self.settings.ASR_MODEL
        self.model_download_dir = self.settings.ASR_MODEL_DOWNLOAD_DIR
        self.processor = WhisperProcessor.from_pretrained(self.model_name, cache_dir=self.model_download_dir)
        self.model = (
            WhisperForConditionalGeneration(
                config=WhisperConfig.from_pretrained(self.model_name, cache_dir=self.model_download_dir)
            )
            .from_pretrained(
                self.model_name,
                torch_dtype=torch.float16,
                cache_dir=self.model_download_dir,
                low_cpu_mem_usage=True, 
            )
        ).eval()

    def _pad_or_trim(self, array: np.ndarray, axis: int = -1):
        """
        Pad or trim the audio array to N_SAMPLES, as expected by the encoder.
        """
        CHUNK_LENGTH = 30  # 30-second chunks
        length: int = CHUNK_LENGTH * self.settings.STREAM_SAMPLE_RATE
        if torch.is_tensor(array):
            if array.shape[axis] > length:
                array = array.index_select(dim=axis, index=torch.arange(length, device=array.device))

            if array.shape[axis] < length:
                pad_widths = [(0, 0)] * array.ndim
                pad_widths[axis] = (0, length - array.shape[axis])
                array = F.pad(array, [pad for sizes in pad_widths[::-1] for pad in sizes])
        else:
            if array.shape[axis] > length:
                array = array.take(indices=range(length), axis=axis)

            if array.shape[axis] < length:
                pad_widths = [(0, 0)] * array.ndim
                pad_widths[axis] = (0, length - array.shape[axis])
                array = np.pad(array, pad_widths)

        return array
    
    def _int2float(self, sound: np.ndarray) -> np.ndarray:
        abs_max = np.abs(sound).max()
        sound = sound.astype('float32')
        if abs_max > 0:
            sound *= 1/32768
        sound = sound.squeeze()  # depends on the use case
        return sound
        
    def transcribe(self, audio: np.ndarray) -> str:
        audio = self._pad_or_trim(audio)
        audio = self._int2float(audio)
        input_features = self.processor(
            audio, 
            sampling_rate=self.settings.STREAM_SAMPLE_RATE, 
            return_tensors="pt"
        ).input_features.to(device=self.model.device, dtype=self.model.dtype)
        
        with torch.no_grad():
            logits = self.model.generate(
                input_features=input_features,
                language=WHISPER_LANGUAGE_CODES[self.settings.ASR_TARGET_LANG],
                forced_decoder_ids=None,
                use_cache=True,
                return_timestamps=False,
            )
        
        transcription = self.processor.batch_decode(logits, skip_special_tokens=True)[0]

        return transcription
