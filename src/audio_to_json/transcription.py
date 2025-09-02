"""
Transcription engine using OpenAI Whisper or faster-whisper for speech-to-text with word timestamps.

Provides Spanish language transcription with word-level timing information
for precise pronunciation clip extraction. Handles deterministic output
and confidence scoring for quality filtering.
"""
from typing import List, Dict, Any, Union
import torch
import numpy as np
from dataclasses import dataclass
import os

from ..shared.config import WhisperConfig
from ..shared.exceptions import TranscriptionError
from ..shared.logging_config import LoggerMixin
from .audio_processor import ProcessedAudio

# Try to import both whisper implementations
try:
    import whisper as openai_whisper
    OPENAI_WHISPER_AVAILABLE = True
except ImportError:
    openai_whisper = None
    OPENAI_WHISPER_AVAILABLE = False

try:
    from faster_whisper import WhisperModel
    FASTER_WHISPER_AVAILABLE = True
except ImportError:
    WhisperModel = None
    FASTER_WHISPER_AVAILABLE = False

# Expose whisper for backward compatibility with tests
whisper = openai_whisper


@dataclass
class Word:
    """Represents a transcribed word with timing information."""
    text: str
    start_time: float
    end_time: float
    confidence: float


class TranscriptionEngine(LoggerMixin):
    """Handles Whisper-based transcription with word timestamps using faster-whisper or OpenAI Whisper."""
    
    def __init__(self, whisper_config: WhisperConfig):
        super().__init__()
        self.config = whisper_config
        self._model = None
        self._use_faster_whisper = FASTER_WHISPER_AVAILABLE and os.getenv("USE_FASTER_WHISPER", "true").lower() == "true"
        
    @property
    def model(self):
        """Lazy-load Whisper model with optimal implementation."""
        if self._model is None:
            if self._use_faster_whisper:
                self._load_faster_whisper()
            else:
                self._load_openai_whisper()
        return self._model
    
    def _load_faster_whisper(self):
        """Load faster-whisper model with CPU optimization."""
        self.log_progress("Loading faster-whisper model", model=self.config.model, implementation="faster-whisper")
        # faster-whisper works best with CPU for M1 Macs currently
        self._model = WhisperModel(self.config.model, device="cpu", compute_type="int8")
        self.log_progress("Faster-whisper model loaded successfully", implementation="faster-whisper")
        
    def _load_openai_whisper(self):
        """Load OpenAI Whisper model with MPS acceleration."""
        if not OPENAI_WHISPER_AVAILABLE:
            raise TranscriptionError("OpenAI Whisper not available. Install with: pip install openai-whisper")
        
        device = "mps" if torch.backends.mps.is_available() else "cpu"
        self.log_progress("Loading OpenAI Whisper model", model=self.config.model, device=device, implementation="openai-whisper")
        self._model = openai_whisper.load_model(self.config.model, device=device)
        self.log_progress("OpenAI Whisper model loaded successfully", device=device, implementation="openai-whisper")
    
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
                               sample_rate=audio.sample_rate,
                               implementation="faster-whisper" if self._use_faster_whisper else "openai-whisper")
            
            if self._use_faster_whisper:
                return self._transcribe_with_faster_whisper(audio)
            else:
                return self._transcribe_with_openai_whisper(audio)
                
        except Exception as e:
            self.logger.error("Transcription failed", error=str(e), 
                            implementation="faster-whisper" if self._use_faster_whisper else "openai-whisper")
            raise TranscriptionError(f"Transcription failed: {e}")
    
    def _transcribe_with_faster_whisper(self, audio: ProcessedAudio) -> List[Word]:
        """Transcribe using faster-whisper implementation."""
        self.log_progress("Starting faster-whisper transcription")
        
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
        
        return words
    
    def _transcribe_with_openai_whisper(self, audio: ProcessedAudio) -> List[Word]:
        """Transcribe using OpenAI Whisper implementation."""
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
        
        self.log_progress("Starting OpenAI Whisper transcription", **options)
        
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
        
            # Handle fallback for segments without word timestamps
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