"""
Transcription engine using OpenAI Whisper for speech-to-text with word timestamps.

Provides Spanish language transcription with word-level timing information
for precise pronunciation clip extraction. Handles deterministic output
and confidence scoring for quality filtering.
"""
from typing import List, Dict, Any
import whisper
import torch
import numpy as np
from dataclasses import dataclass

from ..shared.config import WhisperConfig
from ..shared.exceptions import TranscriptionError
from ..shared.logging_config import LoggerMixin
from .audio_processor import ProcessedAudio


@dataclass
class Word:
    """Represents a transcribed word with timing information."""
    text: str
    start_time: float
    end_time: float
    confidence: float


class TranscriptionEngine(LoggerMixin):
    """Handles Whisper-based transcription with word timestamps."""
    
    def __init__(self, whisper_config: WhisperConfig):
        super().__init__()
        self.config = whisper_config
        self._model = None
        
    @property
    def model(self):
        """Lazy-load Whisper model."""
        if self._model is None:
            self.log_progress("Loading Whisper model", model=self.config.model)
            self._model = whisper.load_model(self.config.model)
            self.log_progress("Whisper model loaded successfully")
        return self._model
    
    def transcribe_audio(self, audio: ProcessedAudio) -> List[Word]:
        """
        Transcribe audio with word-level timestamps.
        
        Args:
            audio: ProcessedAudio object with audio data
            
        Returns:
            List of Word objects with text, start_time, end_time, confidence
            
        Raises:
            TranscriptionError: If transcription fails
        """
        try:
            self.log_stage_start("transcription", 
                               duration=audio.duration,
                               sample_rate=audio.sample_rate)
            
            # Prepare transcription options
            options = {
                "language": self.config.language,
                "word_timestamps": self.config.word_timestamps,
                "temperature": self.config.temperature,
                "condition_on_previous_text": False,  # More deterministic
                "compression_ratio_threshold": 2.4,
                "logprob_threshold": -1.0,
                "no_speech_threshold": 0.6,
            }
            
            self.log_progress("Starting Whisper transcription", **options)
            
            # Transcribe audio
            result = self.model.transcribe(audio.data, **options)
            
            # Extract word-level information
            words = []
            if "segments" in result:
                for segment in result["segments"]:
                    if "words" in segment:
                        for word_info in segment["words"]:
                            word = Word(
                                text=word_info["word"].strip(),
                                start_time=word_info["start"],
                                end_time=word_info["end"],
                                confidence=word_info.get("probability", 0.0)
                            )
                            words.append(word)
            
            # Fallback: if no word timestamps, create from segments
            if not words and "segments" in result:
                self.log_progress("No word timestamps found, using segment-level timing")
                for segment in result["segments"]:
                    # Split segment text into words and estimate timing
                    segment_words = segment["text"].strip().split()
                    segment_duration = segment["end"] - segment["start"]
                    word_duration = segment_duration / len(segment_words) if segment_words else 0
                    
                    for i, word_text in enumerate(segment_words):
                        word_start = segment["start"] + (i * word_duration)
                        word_end = word_start + word_duration
                        
                        word = Word(
                            text=word_text.strip(),
                            start_time=word_start,
                            end_time=word_end,
                            confidence=segment.get("avg_logprob", 0.0)
                        )
                        words.append(word)
            
            # Validate results
            if not words:
                raise TranscriptionError("No words extracted from transcription")
            
            # Filter out empty words
            words = [w for w in words if w.text and len(w.text.strip()) > 0]
            
            self.log_stage_complete("transcription",
                                  words_extracted=len(words),
                                  avg_confidence=sum(w.confidence for w in words) / len(words) if words else 0)
            
            return words
            
        except Exception as e:
            self.log_stage_error("transcription", e)
            if isinstance(e, TranscriptionError):
                raise
            raise TranscriptionError(f"Transcription failed: {e}")


def transcribe_audio(audio: ProcessedAudio, whisper_config: WhisperConfig) -> List[Word]:
    """
    Convenience function for transcribing audio.
    
    Args:
        audio: ProcessedAudio object
        whisper_config: Whisper configuration
        
    Returns:
        List of Word objects
        
    Raises:
        TranscriptionError: If transcription fails
    """
    engine = TranscriptionEngine(whisper_config)
    return engine.transcribe_audio(audio)