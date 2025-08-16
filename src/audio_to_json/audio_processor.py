"""
Audio processing module for loading, validation, and resampling.

Handles audio file loading with format validation, metadata extraction, and
automatic resampling to target sample rate for consistent pipeline processing.
"""
import os
from pathlib import Path
from typing import Optional

import librosa
import soundfile as sf
import numpy as np

from ..shared.models import AudioMetadata
from ..shared.config import Config
from ..shared.exceptions import AudioError
from ..shared.logging_config import LoggerMixin


class AudioProcessor(LoggerMixin):
    """Handles audio file processing and validation."""
    
    def __init__(self, config: Config):
        super().__init__()
        self.config = config
        
    def process_audio(self, audio_path: str) -> 'ProcessedAudio':
        """
        Load and process audio file with validation and resampling.
        
        Args:
            audio_path: Path to the audio file
            
        Returns:
            ProcessedAudio object with audio data and metadata
            
        Raises:
            AudioError: If audio processing fails
        """
        try:
            self.log_stage_start("audio_processing", file=audio_path)
            
            # Validate file exists
            if not Path(audio_path).exists():
                raise AudioError(f"Audio file not found: {audio_path}")
            
            # Load audio file
            self.log_progress("Loading audio file", file=audio_path)
            audio_data, original_sr = librosa.load(
                audio_path, 
                sr=None,  # Keep original sample rate initially
                mono=True if self.config.audio.channels == 1 else False
            )
            
            # Get file metadata
            file_info = sf.info(audio_path)
            file_size = os.path.getsize(audio_path)
            
            # Create metadata
            metadata = AudioMetadata(
                path=audio_path,
                duration=len(audio_data) / original_sr,
                sample_rate=original_sr,
                channels=file_info.channels,
                format=file_info.format.lower(),
                size_bytes=file_size
            )
            
            self.log_progress("Audio loaded", 
                            duration=metadata.duration,
                            original_sr=original_sr,
                            channels=metadata.channels)
            
            # Resample if necessary
            target_sr = self.config.audio.sample_rate
            if original_sr != target_sr:
                self.log_progress("Resampling audio", 
                                from_sr=original_sr, 
                                to_sr=target_sr)
                audio_data = librosa.resample(
                    audio_data, 
                    orig_sr=original_sr, 
                    target_sr=target_sr
                )
                
            # Ensure correct number of channels
            if self.config.audio.channels == 1 and len(audio_data.shape) > 1:
                audio_data = np.mean(audio_data, axis=0)
            
            # Create processed audio object
            processed = ProcessedAudio(
                data=audio_data,
                sample_rate=target_sr,
                duration=len(audio_data) / target_sr,
                metadata=metadata
            )
            
            self.log_stage_complete("audio_processing",
                                  final_duration=processed.duration,
                                  final_sr=processed.sample_rate)
            
            return processed
            
        except Exception as e:
            self.log_stage_error("audio_processing", e, file=audio_path)
            if isinstance(e, AudioError):
                raise
            raise AudioError(f"Failed to process audio file: {e}", {"file": audio_path})


class ProcessedAudio:
    """Container for processed audio data and metadata."""
    
    def __init__(self, data: np.ndarray, sample_rate: int, duration: float, metadata: AudioMetadata):
        self.data = data
        self.sample_rate = sample_rate
        self.duration = duration
        self.metadata = metadata
        self.channels = 1 if len(data.shape) == 1 else data.shape[0]
        
    def __repr__(self):
        return f"ProcessedAudio(duration={self.duration:.2f}s, sr={self.sample_rate}Hz, channels={self.channels})"


def process_audio(audio_path: str, config: Config) -> ProcessedAudio:
    """
    Convenience function for processing audio files.
    
    Args:
        audio_path: Path to the audio file
        config: Configuration object
        
    Returns:
        ProcessedAudio object
        
    Raises:
        AudioError: If audio processing fails
    """
    processor = AudioProcessor(config)
    return processor.process_audio(audio_path)