"""
Transcription engine using faster-whisper for speech-to-text with word timestamps.

Provides Spanish language transcription with word-level timing information
for precise pronunciation clip extraction. Handles deterministic output
and confidence scoring for quality filtering.
"""
from typing import List, Dict, Any
import numpy as np
from dataclasses import dataclass

from ..shared.config import WhisperConfig
from ..shared.exceptions import TranscriptionError
from ..shared.logging_config import LoggerMixin
from .audio_processor import ProcessedAudio

try:
    from faster_whisper import WhisperModel
except ImportError:
    raise ImportError("faster-whisper is required. Install with: pip install faster-whisper")


@dataclass
class Word:
    """Represents a transcribed word with timing information."""
    text: str
    start_time: float
    end_time: float
    confidence: float


class TranscriptionEngine(LoggerMixin):
    """Handles Whisper-based transcription with word timestamps using faster-whisper."""
    
    def __init__(self, whisper_config: WhisperConfig):
        super().__init__()
        self.config = whisper_config
        self._model = None
        
    @property
    def model(self):
        """Lazy-load faster-whisper model."""
        if self._model is None:
            self._load_model()
        return self._model
    
    def _load_model(self):
        """Load faster-whisper model with CPU optimization."""
        self.log_progress("Loading faster-whisper model", model=self.config.model)
        # faster-whisper works best with CPU for M1 Macs currently
        self._model = WhisperModel(self.config.model, device="cpu", compute_type="int8")
        self.log_progress("Faster-whisper model loaded successfully")
        
    
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
            
            return self._transcribe(audio)
                
        except Exception as e:
            self.logger.error("Transcription failed", error=str(e))
            raise TranscriptionError(f"Transcription failed: {e}")
    
    def _transcribe(self, audio: ProcessedAudio) -> List[Word]:
        """Transcribe using faster-whisper."""
        self.log_progress("Starting transcription")
        
        # faster-whisper uses different API
        segments, info = self.model.transcribe(
            audio.data,
            language=self.config.language,
            word_timestamps=self.config.word_timestamps,
            temperature=self.config.temperature,
            condition_on_previous_text=False,
            compression_ratio_threshold=2.4,
            log_prob_threshold=-1.0,
            no_speech_threshold=0.6,
        )
        
        words = []
        for segment in segments:
            if hasattr(segment, 'words') and segment.words:
                for word_info in segment.words:
                    word = Word(
                        text=word_info.word.strip(),
                        start_time=word_info.start,
                        end_time=word_info.end,
                        confidence=word_info.probability
                    )
                    words.append(word)
            else:
                # Fallback: split segment text into words and estimate timing
                segment_words = segment.text.strip().split()
                if segment_words:
                    segment_duration = segment.end - segment.start
                    word_duration = segment_duration / len(segment_words)
                    
                    for i, word_text in enumerate(segment_words):
                        word_start = segment.start + (i * word_duration)
                        word_end = word_start + word_duration
                        
                        word = Word(
                            text=word_text,
                            start_time=word_start,
                            end_time=word_end,
                            confidence=0.8  # Default confidence for estimated timing
                        )
                        words.append(word)
        
        # Validate and filter results
        if not words:
            raise TranscriptionError("No words extracted from transcription")
        
        # Filter out empty words
        words = [w for w in words if w.text and len(w.text.strip()) > 0]
        
        self.log_stage_complete("transcription",
                              words_extracted=len(words),
                              avg_confidence=sum(w.confidence for w in words) / len(words) if words else 0)
        
        return words


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