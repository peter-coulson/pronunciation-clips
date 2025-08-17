"""
Main pipeline orchestration for audio-to-JSON processing.

Coordinates all stages of the pipeline from audio file to complete JSON database.
Provides resumability, error handling, and smart buffering for Colombian Spanish.
Implements the core workflow: Audio → Transcription → Entities → Database.
"""
import time
from pathlib import Path
from typing import Optional, Dict, Any
from datetime import datetime

from ..shared.config import Config
from ..shared.models import WordDatabase, SpeakerInfo
from ..shared.exceptions import PipelineError
from ..shared.logging_config import LoggerMixin

from .audio_processor import process_audio
from .transcription import transcribe_audio
from .entity_creation import create_entities, apply_quality_filters
from .database_writer import write_database


class AudioToJsonPipeline(LoggerMixin):
    """Main pipeline for processing audio files to JSON database."""
    
    def __init__(self, config: Config):
        super().__init__()
        self.config = config
        
    def process_audio_to_json(self, 
                             audio_path: str, 
                             output_path: Optional[str] = None,
                             speaker_mapping: Optional[Dict[str, str]] = None,
                             resume_from_stage: Optional[str] = None) -> WordDatabase:
        """
        Process audio file through complete pipeline to JSON database.
        
        Args:
            audio_path: Path to input audio file
            output_path: Optional output path for JSON file
            speaker_mapping: Optional speaker time mapping
            resume_from_stage: Optional stage to resume from
            
        Returns:
            WordDatabase object with all processed entities
            
        Raises:
            PipelineError: If pipeline processing fails
        """
        try:
            start_time = time.time()
            audio_file = Path(audio_path)
            
            self.log_stage_start("full_pipeline", 
                               audio_file=str(audio_file),
                               output_path=output_path,
                               resume_from=resume_from_stage)
            
            # Stage 1: Audio Processing
            if resume_from_stage not in ["transcription", "entities", "database"]:
                self.log_progress("Starting Stage 1: Audio Processing")
                processed_audio = process_audio(audio_path, self.config)
                self.log_progress("Stage 1 complete", 
                                duration=processed_audio.duration,
                                sample_rate=processed_audio.sample_rate)
            else:
                # For resume functionality (future implementation)
                raise NotImplementedError("Resume functionality not yet implemented")
            
            # Stage 2: Transcription
            if resume_from_stage not in ["entities", "database"]:
                self.log_progress("Starting Stage 2: Transcription")
                words = transcribe_audio(processed_audio, self.config.whisper)
                self.log_progress("Stage 2 complete", 
                                word_count=len(words),
                                avg_confidence=sum(w.confidence for w in words) / len(words) if words else 0.0)
            else:
                raise NotImplementedError("Resume functionality not yet implemented")
            
            # Stage 3: Entity Creation
            if resume_from_stage not in ["database"]:
                self.log_progress("Starting Stage 3: Entity Creation")
                recording_id = self._generate_recording_id(audio_file)
                entities = create_entities(
                    words, 
                    speaker_mapping, 
                    recording_id,
                    str(audio_file),
                    self.config.quality
                )
                
                # Apply quality filtering
                filtered_entities = apply_quality_filters(entities, self.config.quality)
                self.log_progress("Stage 3 complete",
                                original_entities=len(entities), 
                                filtered_entities=len(filtered_entities))
            else:
                raise NotImplementedError("Resume functionality not yet implemented")
            
            # Stage 4: Database Creation
            self.log_progress("Starting Stage 4: Database Creation")
            database = self._create_database(filtered_entities, processed_audio)
            
            # Apply smart buffering (Colombian Spanish requirement)
            database = self._apply_smart_buffering(database)
            
            # Stage 5: Database Writing
            if output_path:
                self.log_progress("Starting Stage 5: Database Writing")
                output_file = write_database(database, Path(output_path), self.config)
                self.log_progress("Stage 5 complete", output_file=str(output_file))
            
            total_time = time.time() - start_time
            self.log_stage_complete("full_pipeline",
                                  total_time=f"{total_time:.2f}s",
                                  entities_processed=len(database.entities),
                                  audio_duration=processed_audio.duration,
                                  processing_rate=f"{processed_audio.duration/total_time:.1f}x realtime")
            
            return database
            
        except Exception as e:
            self.log_stage_error("full_pipeline", e, audio_file=audio_path)
            if isinstance(e, (PipelineError, NotImplementedError)):
                raise
            raise PipelineError(f"Pipeline failed: {e}", {"audio_file": audio_path})
    
    def _generate_recording_id(self, audio_file: Path) -> str:
        """Generate unique recording ID from file path."""
        # Use filename + timestamp for uniqueness
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        clean_name = audio_file.stem.replace(" ", "_").replace("-", "_")
        return f"rec_{clean_name}_{timestamp}"
    
    def _create_database(self, entities, processed_audio) -> WordDatabase:
        """Create WordDatabase with entities and metadata."""
        
        # Create metadata
        metadata = {
            "version": "1.0",
            "created_at": datetime.now().isoformat(),
            "whisper_model": self.config.whisper.model,
            "audio_duration": processed_audio.duration,
            "audio_sample_rate": processed_audio.sample_rate,
            "entity_count": len(entities),
            "config_snapshot": {
                "min_confidence": self.config.quality.min_confidence,
                "min_word_duration": self.config.quality.min_word_duration,
                "max_word_duration": self.config.quality.max_word_duration,
                "syllable_range": self.config.quality.syllable_range
            }
        }
        
        # Create speaker map
        speaker_map = {}
        speaker_ids = set(entity.speaker_id for entity in entities)
        for speaker_id in speaker_ids:
            speaker_map[speaker_id] = SpeakerInfo(
                name=f"Speaker {speaker_id.split('_')[-1]}",
                gender="Unknown",
                region="Unknown"
            )
        
        # Ensure default speaker exists
        if not speaker_map:
            speaker_map["speaker_0"] = SpeakerInfo(
                name="Default Speaker",
                gender="Unknown", 
                region="Unknown"
            )
        
        return WordDatabase(
            metadata=metadata,
            speaker_map=speaker_map,
            entities=entities
        )
    
    def _apply_smart_buffering(self, database: WordDatabase) -> WordDatabase:
        """
        Apply smart buffering for Colombian Spanish continuous speech.
        
        Critical requirement: Check for zero-gap between words before adding buffer.
        Fixed 50ms buffer causes word overlap in Colombian Spanish.
        """
        self.log_progress("Applying smart buffering for Colombian Spanish")
        
        # Sort entities by start time
        sorted_entities = sorted(database.entities, key=lambda e: e.start_time)
        
        overlap_count = 0
        zero_gap_count = 0
        
        for i in range(len(sorted_entities) - 1):
            current = sorted_entities[i]
            next_entity = sorted_entities[i + 1]
            
            # Check for zero gap (Colombian Spanish characteristic)
            gap = next_entity.start_time - current.end_time
            
            if abs(gap) < 0.001:  # Essentially zero gap
                zero_gap_count += 1
                # Do NOT add buffer - would cause overlap
                continue
            
            # Check for existing overlap
            if current.end_time > next_entity.start_time:
                overlap_count += 1
                self.logger.warning("Word overlap detected",
                                  current_word=current.text,
                                  next_word=next_entity.text,
                                  current_end=current.end_time,
                                  next_start=next_entity.start_time)
        
        self.log_progress("Smart buffering analysis complete",
                        total_word_pairs=len(sorted_entities) - 1,
                        zero_gaps=zero_gap_count,
                        overlaps=overlap_count,
                        zero_gap_percentage=f"{zero_gap_count/(len(sorted_entities)-1)*100:.1f}%" if len(sorted_entities) > 1 else "0%")
        
        return database


def process_audio_to_json(audio_path: str, 
                         config: Config,
                         output_path: Optional[str] = None,
                         speaker_mapping: Optional[Dict[str, str]] = None,
                         resume_from_stage: Optional[str] = None) -> WordDatabase:
    """
    Convenience function for processing audio to JSON.
    
    Args:
        audio_path: Path to audio file
        config: Configuration object
        output_path: Optional output file path
        speaker_mapping: Optional speaker mapping
        resume_from_stage: Optional resume point
        
    Returns:
        WordDatabase object
        
    Raises:
        PipelineError: If processing fails
    """
    pipeline = AudioToJsonPipeline(config)
    return pipeline.process_audio_to_json(
        audio_path, 
        output_path, 
        speaker_mapping, 
        resume_from_stage
    )