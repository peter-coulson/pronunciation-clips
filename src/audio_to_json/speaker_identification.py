"""
Speaker identification and mapping module.

Handles speaker assignment based on provided time mappings.
Supports multi-speaker scenarios and default speaker assignment.
Integrates speaker information into entity metadata for pronunciation analysis.
"""
from typing import List, Dict, Any, Optional, Tuple, Union
from copy import deepcopy

from ..shared.models import Entity, SpeakerInfo
from ..shared.exceptions import SpeakerError
from ..shared.logging_config import LoggerMixin


class SpeakerMapper(LoggerMixin):
    """Handles speaker identification and mapping for entities."""
    
    def __init__(self):
        super().__init__()
    
    def apply_speaker_mapping(self, 
                            entities: List[Entity], 
                            speaker_mapping: Optional[Union[List[Dict[str, Any]], Dict[str, str]]]) -> Tuple[List[Entity], Dict[str, Dict[str, Any]]]:
        """
        Apply speaker mapping to entities based on timestamp ranges.
        
        Args:
            entities: List of Entity objects to process
            speaker_mapping: Speaker mapping data (various formats supported)
                - List of dicts with start/end/speaker/speaker_id
                - Dict with time ranges as keys ("start-end": "speaker_id")
                - None for default speaker assignment
        
        Returns:
            Tuple of (updated_entities, speaker_map_dict)
            
        Raises:
            SpeakerError: If speaker mapping fails
        """
        try:
            self.log_stage_start("speaker_mapping", 
                               entity_count=len(entities),
                               has_speaker_mapping=speaker_mapping is not None)
            
            # Create deep copy of entities to avoid modifying originals
            updated_entities = deepcopy(entities)
            
            # Handle different speaker mapping formats
            if speaker_mapping is None:
                return self._apply_default_speaker(updated_entities)
            elif isinstance(speaker_mapping, list):
                return self._apply_list_mapping(updated_entities, speaker_mapping)
            elif isinstance(speaker_mapping, dict):
                return self._apply_dict_mapping(updated_entities, speaker_mapping)
            else:
                raise SpeakerError(f"Unsupported speaker mapping format: {type(speaker_mapping)}")
                
        except Exception as e:
            self.log_stage_error("speaker_mapping", e)
            if isinstance(e, SpeakerError):
                raise
            raise SpeakerError(f"Speaker mapping failed: {e}")
    
    def _apply_default_speaker(self, entities: List[Entity]) -> Tuple[List[Entity], Dict[str, Dict[str, Any]]]:
        """Apply default speaker assignment."""
        self.log_progress("Applying default speaker assignment")
        
        # Ensure all entities have default speaker
        for entity in entities:
            if not entity.speaker_id or entity.speaker_id == "":
                entity.speaker_id = 0
        
        # Create default speaker map
        speaker_map = {
            0: {
                "name": "Test Speaker",
                "gender": "Unknown",
                "region": "Unknown"
            }
        }
        
        self.log_stage_complete("speaker_mapping",
                              entities_updated=len(entities),
                              speakers_assigned=1)
        
        return entities, speaker_map
    
    def _apply_list_mapping(self, entities: List[Entity], 
                          speaker_mapping: List[Dict[str, Any]]) -> Tuple[List[Entity], Dict[str, Dict[str, Any]]]:
        """Apply list-based speaker mapping."""
        self.log_progress("Applying list-based speaker mapping", 
                        mapping_count=len(speaker_mapping))
        
        speaker_map = {}
        speakers_updated = 0
        
        for entity in entities:
            entity_center_time = (entity.start_time + entity.end_time) / 2
            
            # Find matching speaker range
            for mapping in speaker_mapping:
                start_time = mapping.get("start", 0.0)
                end_time = mapping.get("end", float('inf'))
                
                if start_time <= entity_center_time <= end_time:
                    speaker_id = mapping.get("speaker_id", 0)
                    speaker_name = mapping.get("speaker", "Unknown Speaker")
                    
                    # Update entity
                    entity.speaker_id = speaker_id
                    speakers_updated += 1
                    
                    # Add to speaker map
                    if speaker_id not in speaker_map:
                        speaker_map[speaker_id] = {
                            "name": speaker_name,
                            "gender": mapping.get("gender", "Unknown"),
                            "region": mapping.get("region", "Unknown")
                        }
                    break
            else:
                # No matching range found - use default
                if not entity.speaker_id:
                    entity.speaker_id = 0
                    if 0 not in speaker_map:
                        speaker_map[0] = {
                            "name": "Default Speaker",
                            "gender": "Unknown",
                            "region": "Unknown"
                        }
        
        self.log_stage_complete("speaker_mapping",
                              entities_updated=speakers_updated,
                              speakers_assigned=len(speaker_map))
        
        return entities, speaker_map
    
    def _apply_dict_mapping(self, entities: List[Entity], 
                          speaker_mapping: Dict[str, str]) -> Tuple[List[Entity], Dict[str, Dict[str, Any]]]:
        """Apply dictionary-based speaker mapping (time ranges as keys)."""
        self.log_progress("Applying dict-based speaker mapping", 
                        mapping_count=len(speaker_mapping))
        
        speaker_map = {}
        speakers_updated = 0
        
        for entity in entities:
            entity_center_time = (entity.start_time + entity.end_time) / 2
            
            # Find matching time range
            for time_range, speaker_id in speaker_mapping.items():
                try:
                    # Parse time range format "start-end"
                    start_str, end_str = time_range.split("-")
                    start_time = float(start_str)
                    end_time = float(end_str)
                    
                    if start_time <= entity_center_time <= end_time:
                        entity.speaker_id = speaker_id
                        speakers_updated += 1
                        
                        # Add to speaker map if not exists
                        if speaker_id not in speaker_map:
                            speaker_map[speaker_id] = {
                                "name": f"Speaker {speaker_id.split('_')[-1]}",
                                "gender": "Unknown",
                                "region": "Unknown"
                            }
                        break
                        
                except (ValueError, AttributeError):
                    self.logger.warning("Invalid time range format", 
                                      time_range=time_range)
                    continue
            else:
                # No matching range - use default
                if not entity.speaker_id:
                    entity.speaker_id = 0
                    if 0 not in speaker_map:
                        speaker_map[0] = {
                            "name": "Default Speaker",
                            "gender": "Unknown",
                            "region": "Unknown"
                        }
        
        self.log_stage_complete("speaker_mapping",
                              entities_updated=speakers_updated,
                              speakers_assigned=len(speaker_map))
        
        return entities, speaker_map


def apply_speaker_mapping(entities: List[Entity], 
                         speaker_mapping: Optional[Union[List[Dict[str, Any]], Dict[str, str]]]) -> Tuple[List[Entity], Dict[str, Dict[str, Any]]]:
    """
    Convenience function for applying speaker mapping.
    
    Args:
        entities: List of Entity objects
        speaker_mapping: Speaker mapping data (various formats)
        
    Returns:
        Tuple of (updated_entities, speaker_map_dict)
        
    Raises:
        SpeakerError: If speaker mapping fails
    """
    mapper = SpeakerMapper()
    return mapper.apply_speaker_mapping(entities, speaker_mapping)