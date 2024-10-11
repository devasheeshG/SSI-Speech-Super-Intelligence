# Path: ssi/utils/asr/asr_factory.py
# Description: This file will contain the factory class for the ASR models. We'll use this factory to create instances of different ASR models.

from .whisper_transformers_asr import WhisperTransformersASR

class ASRFactory:
    """
    A factory class for creating instances of different ASR models.

    This factory provides a centralized way to instantiate various ASR
    models based on the type specified. It abstracts the creation logic,
    making it easier to manage and extend with new ASR model types.
    
    Methods:
        create_asr_pipeline: Creates and returns an instance of a specified ASR model.
    """
    
    @staticmethod
    def create_asr_pipeline(type: str):
        """
        Creates an instance of an ASR model based on the specified type.

        This method acts as a factory for creating ASR model objects.
        It returns an instance of the model corresponding to the given type.
        If the type is not recognized, it raises a ValueError.

        Args:
            type (str): The type of ASR model to create. Currently supports 'whisper'.

        Returns:
            An instance of the specified ASR model.

        Raises:
            ValueError: If the specified type is not recognized or supported.

        Example:
            model = ASRFactory.create_asr_pipeline("whisper")
        """
        if type == "whisper_transformers":
            return WhisperTransformersASR()
        else:
            raise ValueError(f"Unknown ASR model type: {type}")
