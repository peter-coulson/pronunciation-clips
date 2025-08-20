"""
Entity creation and quality filtering module.

Converts Whisper transcription output to validated Entity objects with quality filtering
based on confidence, duration, and syllable count. Handles speaker assignment and
generates unique entity IDs for database storage.
"""
from typing import List, Dict, Any, Optional, Union
from datetime import datetime

from ..shared.models import Entity
from ..shared.config import QualityConfig
from ..shared.exceptions import EntityError
from ..shared.logging_config import LoggerMixin
from .transcription import Word


class EntityCreator(LoggerMixin):
    """Creates and filters Entity objects from transcription data."""
    
    def __init__(self, quality_config: QualityConfig):
        super().__init__()
        self.quality_config = quality_config
        
    def create_entities(self, words: List[Word], 
                       recording_id: str, 
                       recording_path: str,
                       speaker_mapping: Optional[Dict[str, str]] = None) -> List[Entity]:
        """
        Create Entity objects from Whisper word transcription data.
        
        Args:
            words: List of Word objects from Whisper
            recording_id: Identifier for the source recording
            recording_path: Path to the source audio file
            speaker_mapping: Optional mapping of time ranges to speaker IDs
            
        Returns:
            List of Entity objects
            
        Raises:
            EntityError: If entity creation fails
        """
        try:
            self.log_stage_start("entity_creation", 
                               word_count=len(words),
                               recording_id=recording_id)
            
            entities = []
            current_time = datetime.now().isoformat()
            
            for i, word_data in enumerate(words):
                try:
                    # Generate unique entity ID
                    entity_id = f"word_{i+1:03d}"
                    
                    # Calculate duration
                    start_time = float(word_data.start_time)
                    end_time = float(word_data.end_time)
                    duration = end_time - start_time
                    
                    # Determine speaker ID
                    speaker_id = self._get_speaker_id(start_time, end_time, speaker_mapping)
                    
                    # Basic syllable analysis (simple heuristic)
                    text = word_data.text.strip()
                    syllables = self._estimate_syllables(text)
                    
                    # Create entity
                    entity = Entity(
                        entity_id=entity_id,
                        entity_type="word",
                        text=text,
                        start_time=start_time,
                        end_time=end_time,
                        duration=duration,
                        confidence=float(word_data.confidence),
                        probability=float(word_data.confidence),  # Use confidence for both
                        syllables=syllables,
                        syllable_count=len(syllables),
                        phonetic=None,  # To be filled by future phonetic analysis
                        quality_score=self._calculate_quality_score(word_data, duration, syllables),
                        speaker_id=speaker_id,
                        recording_id=recording_id,
                        recording_path=recording_path,
                        processed=False,
                        clip_path=None,
                        selection_reason=None,
                        created_at=current_time
                    )
                    
                    entities.append(entity)
                    
                except Exception as e:
                    self.logger.warning("Failed to create entity for word", 
                                      word_index=i, 
                                      word_text=word_data.text if hasattr(word_data, 'text') else "",
                                      error=str(e))
                    continue
                    
            self.log_stage_complete("entity_creation", 
                                  entities_created=len(entities),
                                  original_words=len(words))
            
            return entities
            
        except Exception as e:
            self.log_stage_error("entity_creation", e)
            raise EntityError(f"Failed to create entities: {e}")
            
    def apply_quality_filters(self, entities: List[Entity]) -> List[Entity]:
        """
        Apply quality filtering based on configuration.
        
        Args:
            entities: List of Entity objects to filter
            
        Returns:
            Filtered list of Entity objects
        """
        try:
            self.log_stage_start("quality_filtering", 
                               total_entities=len(entities))
            
            original_count = len(entities)
            filtered_entities = []
            
            for entity in entities:
                # Confidence filter
                if entity.confidence < self.quality_config.min_confidence:
                    continue
                    
                # Duration filters
                if entity.duration < self.quality_config.min_word_duration:
                    continue
                if entity.duration > self.quality_config.max_word_duration:
                    continue
                    
                # Syllable count filter (allow common short words like "tal")
                min_syl, max_syl = self.quality_config.syllable_range
                if not (min_syl <= entity.syllable_count <= max_syl):
                    # Special exception for common Spanish words that are useful even if short
                    if entity.text.lower() not in ["tal", "que", "con", "por", "sin", "son"]:
                        continue
                    
                # Text validation
                if not entity.text or len(entity.text.strip()) == 0:
                    continue
                    
                filtered_entities.append(entity)
                
            filtered_count = len(filtered_entities)
            pass_rate = (filtered_count / original_count * 100) if original_count > 0 else 0
            
            self.log_stage_complete("quality_filtering",
                                  original_count=original_count,
                                  filtered_count=filtered_count,
                                  pass_rate=f"{pass_rate:.1f}%")
            
            return filtered_entities
            
        except Exception as e:
            self.log_stage_error("quality_filtering", e)
            raise EntityError(f"Quality filtering failed: {e}")
    
    def _get_speaker_id(self, start_time: float, end_time: float, 
                       speaker_mapping: Optional[Dict[str, str]]) -> int:
        """Determine speaker ID based on timing and mapping."""
        if not speaker_mapping:
            return 0
            
        # Find speaker based on time overlap
        word_center = (start_time + end_time) / 2
        for time_range, speaker_id in speaker_mapping.items():
            # Parse time range format "start-end"
            try:
                range_start, range_end = map(float, time_range.split("-"))
                if range_start <= word_center <= range_end:
                    # Convert speaker_id to integer (handle both "speaker_0" and "0" formats)
                    if isinstance(speaker_id, str) and speaker_id.startswith("speaker_"):
                        return int(speaker_id.replace("speaker_", ""))
                    return int(speaker_id)
            except (ValueError, AttributeError):
                continue
                
        return 0  # Default fallback
        
    def _estimate_syllables(self, text: str) -> List[str]:
        """
        Simple syllable estimation for Spanish words.
        
        This is a basic heuristic - could be improved with phonetic analysis.
        """
        text = text.lower().strip()
        if not text:
            return []
            
        # Special case handling for common Spanish words
        if text == "tal":
            return ["tal"]  # Keep as single syllable but accept in filtering
            
        # Basic Spanish vowel pattern recognition
        vowels = "aeiouáéíóúü"
        syllables = []
        current_syllable = ""
        
        i = 0
        while i < len(text):
            char = text[i]
            current_syllable += char
            
            # Check if this character starts a new syllable
            if char in vowels:
                # Look ahead for vowel clusters
                if i + 1 < len(text) and text[i + 1] in vowels:
                    # Handle diphthongs/vowel clusters
                    if char + text[i + 1] in ["ai", "au", "ei", "eu", "oi", "ou", "ia", "ie", "io", "iu", "ua", "ue", "ui", "uo"]:
                        current_syllable += text[i + 1]
                        i += 1
                
                # End syllable after vowel (+ optional consonant)
                if i + 1 < len(text) and text[i + 1] not in vowels:
                    current_syllable += text[i + 1]
                    i += 1
                    
                syllables.append(current_syllable)
                current_syllable = ""
            
            i += 1
            
        # Add any remaining characters
        if current_syllable:
            if syllables:
                syllables[-1] += current_syllable
            else:
                syllables.append(current_syllable)
                
        # Fallback: if no syllables detected, split by vowels
        if not syllables:
            syllables = [text]
            
        return syllables
        
    def _calculate_quality_score(self, word_data: Word, 
                                duration: float, 
                                syllables: List[str]) -> float:
        """Calculate overall quality score for a word."""
        confidence = float(word_data.confidence)
        
        # Duration score (prefer medium durations)
        duration_score = 1.0
        if duration < 0.2:
            duration_score = 0.5
        elif duration > 2.0:
            duration_score = 0.7
            
        # Syllable score (prefer 2-4 syllables)
        syllable_score = 1.0
        syllable_count = len(syllables)
        if syllable_count == 1:
            syllable_score = 0.6
        elif syllable_count > 5:
            syllable_score = 0.8
            
        # Weighted average
        quality_score = (confidence * 0.6 + duration_score * 0.2 + syllable_score * 0.2)
        
        return min(1.0, max(0.0, quality_score))


def create_entities(words: Union[List[Word], List[Dict[str, Any]]], 
                   speaker_mapping: Optional[Dict[str, str]], 
                   recording_id: str,
                   recording_path: str = "unknown.wav",
                   quality_config: Optional[QualityConfig] = None) -> List[Entity]:
    """
    Convenience function for creating entities.
    
    Args:
        words: Whisper transcription Word objects or dictionaries
        speaker_mapping: Optional speaker mapping
        recording_id: Recording identifier
        recording_path: Path to audio file
        quality_config: Quality configuration (uses defaults if None)
        
    Returns:
        List of Entity objects
    """
    if quality_config is None:
        # Create default quality config
        from ..shared.config import QualityConfig
        quality_config = QualityConfig()
    
    # Convert dictionaries to Word objects if needed (for E2E test compatibility)
    if words and isinstance(words[0], dict):
        word_objects = []
        for word_dict in words:
            word_obj = Word(
                text=word_dict["text"],
                start_time=word_dict.get("start", word_dict.get("start_time", 0.0)),
                end_time=word_dict.get("end", word_dict.get("end_time", 0.0)),
                confidence=word_dict.get("confidence", word_dict.get("probability", 0.0))
            )
            word_objects.append(word_obj)
        words = word_objects
        
    creator = EntityCreator(quality_config)
    return creator.create_entities(words, recording_id, recording_path, speaker_mapping)


def apply_quality_filters(entities: List[Entity], quality_config: QualityConfig) -> List[Entity]:
    """
    Convenience function for applying quality filters.
    
    Args:
        entities: List of entities to filter
        quality_config: Quality filtering configuration
        
    Returns:
        Filtered list of entities
    """
    creator = EntityCreator(quality_config)
    return creator.apply_quality_filters(entities)