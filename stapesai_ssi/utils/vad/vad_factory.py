# Path: ssi/utils/vad/vad_factory.py
# Description: This module contains a factory class for creating instances of different VAD strategies.

from .silero_vad import SileroVAD

class VADFactory:
    """
    A factory class for creating instances of different VAD strategies.

    This factory provides a centralized way to instantiate various VAD
    strategies based on the type specified. It abstracts the creation logic,
    making it easier to manage and extend with new VAD strategy types.

    Methods:
        create_vad_pipeline: Creates and returns an instance of a specified VAD strategy.
    """

    @staticmethod
    def create_vad_pipeline(type: str):
        """
        Creates an instance of a VAD strategy based on the specified type.

        This method acts as a factory for creating VAD strategy objects.
        It returns an instance of the strategy corresponding to the given type.
        If the type is not recognized, it raises a ValueError.

        Args:
            type (str): The type of VAD strategy to create. Currently supports 'silero'.

        Returns:
            An instance of the specified VAD strategy.

        Raises:
            ValueError: If the specified type is not recognized or supported.

        Example:
            strategy = VADFactory.create_vad_pipeline("silero")
        """
        if type == "silero":
            return SileroVAD()
        elif type == "pyannote":
            raise NotImplementedError("Pyannote VAD not implemented yet")
        else:
            raise ValueError(f"Unknown VAD strategy type: {type}")
