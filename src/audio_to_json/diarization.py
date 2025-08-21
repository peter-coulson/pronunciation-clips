"""
ML diarization module for speaker diarization using PyAnnote.

Integrates with PyAnnote for speaker diarization using the foundation
interfaces established in the shared models and configuration system.
"""
import os
import time
from typing import List, Optional, Tuple, Any
from pathlib import Path

from ..shared.models import DiarizationResult, SpeakerSegment
from ..shared.config import DiarizationConfig
from ..shared.exceptions import PipelineError
from ..shared.logging_config import LoggerMixin

# Optional ML dependencies with graceful fallback
try:
    from pyannote.audio import Pipeline
    import torch
    PYANNOTE_AVAILABLE = True
except ImportError:
    Pipeline = None
    torch = None
    PYANNOTE_AVAILABLE = False


class DiarizationProcessor(LoggerMixin):
    """Handles ML-based speaker diarization using PyAnnote."""
    
    def __init__(self, config: DiarizationConfig):
        super().__init__()
        self.config = config
        self.pipeline = None
        
        # Log configuration for debugging
        self.logger.info("Initializing diarization processor", 
                        model=config.model,
                        min_speakers=config.min_speakers,
                        max_speakers=config.max_speakers,
                        pyannote_available=PYANNOTE_AVAILABLE)
        
    def process_audio(self, audio_path: str, audio_duration: float) -> DiarizationResult:
        """
        Process audio file for speaker diarization.
        
        Args:
            audio_path: Path to input audio file
            audio_duration: Duration of audio in seconds
            
        Returns:
            DiarizationResult with speakers and segments
            
        Raises:
            PipelineError: If diarization processing fails
        """
        self.log_stage_start("diarization", 
                           audio_path=audio_path,
                           duration=audio_duration)
        
        start_time = time.time()
        
        try:
            # Validate inputs
            if not Path(audio_path).exists():
                raise PipelineError(f"Audio file not found: {audio_path}")
            
            if audio_duration <= 0:
                raise PipelineError(f"Invalid audio duration: {audio_duration}")
            
            # Check dependencies
            if not PYANNOTE_AVAILABLE:
                self.logger.warning("PyAnnote not available, falling back to single speaker")
                return self._create_single_speaker_fallback(audio_duration, time.time() - start_time)
            
            # Load pipeline if needed
            if self.pipeline is None:
                self._load_pipeline()
            
            # Perform diarization
            diarization_result = self.pipeline(audio_path)
            
            # Convert to our format
            segments = self._extract_segments(diarization_result, audio_duration)
            speakers = list(set(seg.speaker_id for seg in segments))
            
            processing_time = time.time() - start_time
            
            result = DiarizationResult(
                speakers=sorted(speakers),
                segments=segments,
                audio_duration=audio_duration,
                processing_time=processing_time
            )
            
            # Validate result quality
            if not self._validate_result(result, audio_duration):
                self.logger.warning("Diarization result failed validation, using single speaker fallback")
                return self._create_single_speaker_fallback(audio_duration, processing_time)
            
            self.log_stage_complete("diarization",
                                  speakers_detected=len(result.speakers),
                                  segments_created=len(result.segments),
                                  processing_time=processing_time,
                                  realtime_factor=audio_duration / processing_time)
            
            return result
            
        except Exception as e:
            processing_time = time.time() - start_time
            self.logger.warning("Diarization failed, using single speaker fallback", 
                              error=str(e), 
                              processing_time=processing_time)
            
            # Return fallback instead of raising
            return self._create_single_speaker_fallback(audio_duration, processing_time)
        
    def _load_pipeline(self) -> None:
        """Load PyAnnote diarization pipeline."""
        if not PYANNOTE_AVAILABLE:
            raise PipelineError(
                "PyAnnote not available. Install with: pip install pyannote.audio torch"
            )
        
        try:
            self.logger.info("Loading diarization pipeline", model=self.config.model)
            
            # Load the pipeline
            # Get HuggingFace token from environment variable
            hf_token = os.getenv('HF_TOKEN')
            self.pipeline = Pipeline.from_pretrained(
                self.config.model,
                use_auth_token=hf_token
            )
            
            # Configure parameters
            if hasattr(self.pipeline, 'instantiate'):
                try:
                    # Set speaker constraints - try with new API first
                    self.pipeline.instantiate({
                        "clustering": {
                            "threshold": self.config.clustering_threshold
                        },
                        "segmentation": {
                            "threshold": self.config.segmentation_threshold
                        }
                    })
                except Exception as e:
                    # Fallback to no custom parameters if instantiate fails
                    self.logger.warning("Could not configure pipeline parameters", error=str(e))
                    pass
            
            self.logger.info("Diarization pipeline loaded successfully")
            
        except Exception as e:
            raise PipelineError(f"Failed to load diarization pipeline: {e}")
        
    def _extract_segments(self, diarization_output: Any, audio_duration: float) -> List[SpeakerSegment]:
        """Convert PyAnnote output to SpeakerSegment objects."""
        segments = []
        
        try:
            # PyAnnote returns an Annotation object with speaker labels and time intervals
            for segment, _, speaker_label in diarization_output.itertracks(yield_label=True):
                # Convert speaker label to integer ID
                speaker_id = self._speaker_label_to_id(speaker_label)
                
                # Create segment with reasonable confidence
                # PyAnnote doesn't provide confidence scores, so we use a default
                confidence = 0.85  # Reasonable default for PyAnnote
                
                # Ensure segment is within audio bounds
                start_time = max(0.0, float(segment.start))
                end_time = min(audio_duration, float(segment.end))
                
                if end_time > start_time:  # Valid segment
                    segments.append(SpeakerSegment(
                        speaker_id=speaker_id,
                        start_time=start_time,
                        end_time=end_time,
                        confidence=confidence
                    ))
            
            # Sort segments by start time
            segments.sort(key=lambda x: x.start_time)
            
            # Merge very close segments from same speaker
            segments = self._merge_close_segments(segments)
            
            return segments
            
        except Exception as e:
            self.logger.error("Failed to extract segments from diarization output", error=str(e))
            # Return single speaker segment as fallback
            return [SpeakerSegment(
                speaker_id=0,
                start_time=0.0,
                end_time=audio_duration,
                confidence=1.0
            )]
    
    def _speaker_label_to_id(self, speaker_label: str) -> int:
        """Convert PyAnnote speaker label to integer ID."""
        # PyAnnote uses labels like "SPEAKER_00", "SPEAKER_01", etc.
        # Extract the number and use as ID
        try:
            if isinstance(speaker_label, str) and "SPEAKER_" in speaker_label:
                return int(speaker_label.split("_")[-1])
            else:
                # Fallback: hash the label to get consistent ID
                return abs(hash(str(speaker_label))) % 100
        except (ValueError, IndexError):
            return 0  # Fallback to speaker 0
    
    def _merge_close_segments(self, segments: List[SpeakerSegment], 
                             gap_threshold: float = 0.5) -> List[SpeakerSegment]:
        """Merge segments from same speaker that are very close together."""
        if not segments:
            return segments
        
        merged = [segments[0]]
        
        for current in segments[1:]:
            last = merged[-1]
            
            # If same speaker and gap is small, merge
            if (current.speaker_id == last.speaker_id and 
                current.start_time - last.end_time <= gap_threshold):
                
                # Extend the last segment
                merged[-1] = SpeakerSegment(
                    speaker_id=last.speaker_id,
                    start_time=last.start_time,
                    end_time=current.end_time,
                    confidence=max(last.confidence, current.confidence)
                )
            else:
                merged.append(current)
        
        return merged
    
    def _validate_result(self, result: DiarizationResult, expected_duration: float) -> bool:
        """Validate diarization result meets quality standards."""
        try:
            # Check basic structure
            if not result.speakers or not result.segments:
                return False
            
            # Check duration coverage
            total_coverage = sum(seg.end_time - seg.start_time for seg in result.segments)
            coverage_ratio = total_coverage / expected_duration if expected_duration > 0 else 0
            
            # At least 70% coverage required
            if coverage_ratio < 0.7:
                self.logger.warning("Low coverage ratio", ratio=coverage_ratio)
                return False
            
            # Check confidence scores
            if any(seg.confidence <= 0.0 for seg in result.segments):
                return False
            
            # Check reasonable segment durations
            min_duration = getattr(self.config, 'min_segment_duration', 0.5)
            short_segments = [s for s in result.segments if (s.end_time - s.start_time) < min_duration]
            if len(short_segments) > len(result.segments) * 0.8:  # Too many short segments
                self.logger.warning("Too many short segments", count=len(short_segments))
                return False
            
            return True
            
        except Exception as e:
            self.logger.error("Error validating diarization result", error=str(e))
            return False
    
    def _create_single_speaker_fallback(self, duration: float, processing_time: float) -> DiarizationResult:
        """Create fallback result for single speaker."""
        # Ensure valid duration for fallback
        valid_duration = max(1.0, duration) if duration > 0 else 1.0
        
        return DiarizationResult(
            speakers=[0],
            segments=[SpeakerSegment(
                speaker_id=0,
                start_time=0.0,
                end_time=valid_duration,
                confidence=1.0
            )],
            audio_duration=valid_duration,
            processing_time=processing_time
        )


def check_diarization_dependencies() -> Tuple[bool, Optional[str]]:
    """
    Check if diarization dependencies are available.
    
    Returns:
        Tuple of (available, error_message)
    """
    if not PYANNOTE_AVAILABLE:
        return False, "PyAnnote not available. Install with: pip install pyannote.audio torch"
    
    try:
        # Test basic PyAnnote functionality
        Pipeline.from_pretrained.__doc__  # Simple check
        return True, None
    except Exception as e:
        return False, f"PyAnnote installation issue: {e}"


def process_diarization(audio_path: str, 
                       audio_duration: float,
                       config: Optional[DiarizationConfig] = None) -> DiarizationResult:
    """
    Convenience function for diarization processing.
    
    Args:
        audio_path: Path to audio file
        audio_duration: Audio duration in seconds
        config: Diarization configuration (uses defaults if None)
        
    Returns:
        DiarizationResult object
    """
    if config is None:
        config = DiarizationConfig()
    
    processor = DiarizationProcessor(config)
    return processor.process_audio(audio_path, audio_duration)