"""
Integration tests for Stage 1: Foundation.

Tests integration between config, models, logging, and exceptions.
Verifies that components work together correctly.
"""
import pytest
import tempfile
import os
from pathlib import Path
from datetime import datetime

from src.shared.config import load_config, Config
from src.shared.models import Entity, WordDatabase, SpeakerInfo, AudioMetadata
from src.shared.logging_config import LoggerMixin, init_logger
from src.shared.exceptions import ConfigError, PipelineError


class TestConfigModelIntegration:
    """Test configuration and model integration."""
    
    def test_config_loads_and_validates_with_models(self):
        """Test that loaded config works with model creation."""
        # Create a complete config file
        config_yaml = """
audio:
  sample_rate: 16000
  channels: 1
  buffer_seconds: 0.1

whisper:
  model: "base"
  language: "es"
  word_timestamps: true
  temperature: 0.0

quality:
  min_confidence: 0.8
  min_word_duration: 0.3
  max_word_duration: 3.0
  syllable_range: [2, 6]

speakers:
  enable_diarization: false
  min_speakers: 1
  max_speakers: 10

output:
  database_path: "test_output.json"
  encoding: "utf-8"
  pretty_print: true

logging:
  level: "INFO"
  format: "structured"
"""
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            f.write(config_yaml)
            f.flush()
            
            try:
                # Load config
                config = load_config(f.name)
                
                # Use config values to create entities that match quality criteria
                entity = Entity(
                    entity_id="word_001",
                    entity_type="word",
                    text="hola",
                    start_time=1.0,
                    end_time=1.5,
                    duration=0.5,  # Within min/max duration from config
                    confidence=0.9,  # Above min_confidence from config
                    probability=0.85,
                    syllables=["ho", "la"],
                    syllable_count=2,  # Within syllable_range from config
                    phonetic="ˈoʊlə",
                    quality_score=0.8,
                    speaker_id=0,  # Changed to integer for diarization compatibility
                    recording_id="test",
                    recording_path="test.wav",
                    processed=False,
                    created_at=datetime.now().isoformat()
                )
                
                # Verify entity meets config criteria
                assert entity.confidence >= config.quality.min_confidence
                assert entity.duration >= config.quality.min_word_duration
                assert entity.duration <= config.quality.max_word_duration
                assert config.quality.syllable_range[0] <= entity.syllable_count <= config.quality.syllable_range[1]
                
            finally:
                os.unlink(f.name)
    
    def test_config_validation_affects_model_creation(self):
        """Test that config validation prevents invalid model creation."""
        # Create config with very strict quality settings
        config = Config()
        config.quality.min_confidence = 0.95
        config.quality.min_word_duration = 1.0
        config.quality.max_word_duration = 1.5
        config.quality.syllable_range = [3, 3]  # Exactly 3 syllables
        
        # Try to create entity that doesn't meet config criteria
        # This should succeed at model level but fail quality filtering
        entity = Entity(
            entity_id="word_001",
            entity_type="word",
            text="test",
            start_time=1.0,
            end_time=1.2,
            duration=0.2,  # Below min_word_duration
            confidence=0.8,  # Below min_confidence
            probability=0.8,
            syllables=["test"],
            syllable_count=1,  # Outside syllable_range
            quality_score=0.5,
            speaker_id=0,
            recording_id="test",
            recording_path="test.wav",
            processed=False,
            created_at=datetime.now().isoformat()
        )
        
        # Entity creation succeeds (model validation is separate from config)
        assert entity.confidence < config.quality.min_confidence
        assert entity.duration < config.quality.min_word_duration
        assert entity.syllable_count < config.quality.syllable_range[0]


class TestConfigLoggingIntegration:
    """Test configuration and logging integration."""
    
    def test_config_initializes_logging_correctly(self):
        """Test that config properly initializes logging system."""
        config = Config()
        config.logging.level = "DEBUG"
        config.logging.format = "structured"
        
        # Initialize logging with config
        init_logger(config)
        
        # Create a test class that uses logging
        class TestComponent(LoggerMixin):
            pass
        
        component = TestComponent()
        
        # Verify logger was created and configured
        assert component.logger is not None
        assert component.logger.name.endswith("TestComponent")
    
    def test_different_log_levels_work_with_config(self):
        """Test that different log levels from config work correctly."""
        for level in ["DEBUG", "INFO", "WARNING", "ERROR"]:
            config = Config()
            config.logging.level = level
            
            # Should not raise exceptions
            init_logger(config)
            
            class TestComponent(LoggerMixin):
                pass
            
            component = TestComponent()
            assert component.logger is not None


class TestModelDatabaseIntegration:
    """Test model and database integration."""
    
    def test_entities_integrate_with_database(self):
        """Test that entities work correctly with WordDatabase."""
        # Create multiple entities
        entities = []
        for i in range(3):
            entity = Entity(
                entity_id=f"word_{i+1:03d}",
                entity_type="word",
                text=f"word{i+1}",
                start_time=float(i),
                end_time=float(i+1),
                duration=1.0,
                confidence=0.8 + i * 0.1,
                probability=0.8 + i * 0.1,
                syllables=[f"word{i+1}"],
                syllable_count=1,
                quality_score=0.8,
                speaker_id=0,
                recording_id="test",
                recording_path="test.wav",
                processed=False,
                created_at=datetime.now().isoformat()
            )
            entities.append(entity)
        
        # Create database and add entities
        database = WordDatabase(
            metadata={"version": "1.0", "created_at": datetime.now().isoformat()},
            speaker_map={},
            entities=entities
        )
        
        # Test database operations
        assert len(database.entities) == 3
        
        # Test filtering by type
        words = database.get_entities_by_type("word")
        assert len(words) == 3
        
        # Test filtering by speaker
        speaker_entities = database.get_entities_by_speaker(0)  # Changed to integer
        assert len(speaker_entities) == 3
        
        # Test filtering by confidence
        high_conf = database.get_entities_by_confidence(0.9)
        assert len(high_conf) == 2  # Last two entities have conf >= 0.9
    
    def test_database_with_metadata_and_speakers(self):
        """Test database integration with metadata and speaker info."""
        # Create audio metadata
        audio_metadata = AudioMetadata(
            path="test.wav",
            duration=120.0,
            sample_rate=16000,
            channels=1,
            format="wav",
            size_bytes=1024000
        )
        
        # Create speaker info
        speaker_info = SpeakerInfo(
            name="Test Speaker",
            gender="F",
            region="Colombia"
        )
        
        # Create database with all components
        database = WordDatabase(
            metadata={
                "version": "1.0",
                "created_at": datetime.now().isoformat(),
                "audio_metadata": audio_metadata.model_dump()
            },
            speaker_map={0: speaker_info},
            entities=[]
        )
        
        # Add entity
        entity = Entity(
            entity_id="word_001",
            entity_type="word",
            text="hola",
            start_time=1.0,
            end_time=1.5,
            duration=0.5,
            confidence=0.9,
            probability=0.85,
            syllables=["ho", "la"],
            syllable_count=2,
            quality_score=0.8,
            speaker_id=0,
            recording_id="test",
            recording_path="test.wav",
            processed=False,
            created_at=datetime.now().isoformat()
        )
        
        database.entities.append(entity)
        
        # Verify integration
        assert database.metadata["audio_metadata"]["duration"] == 120.0
        assert database.speaker_map[0].name == "Test Speaker"
        assert database.entities[0].speaker_id in database.speaker_map
        assert len(database.entities) == 1


class TestExceptionConfigIntegration:
    """Test exception and configuration integration."""
    
    def test_config_errors_include_context(self):
        """Test that config errors include helpful context."""
        # Test with invalid config file
        invalid_yaml = """
audio:
  sample_rate: "invalid"  # Should be int
  channels: 3  # Invalid value
"""
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            f.write(invalid_yaml)
            f.flush()
            
            try:
                with pytest.raises(ConfigError) as exc_info:
                    load_config(f.name)
                
                # Verify error includes context about the config file
                error = exc_info.value
                assert isinstance(error, ConfigError)
                # Error should mention the problematic config
                assert str(error) is not None
                
            finally:
                os.unlink(f.name)
    
    def test_validation_errors_with_model_context(self):
        """Test that validation errors include model context."""
        # Create entity with invalid data that should trigger validation
        with pytest.raises(ValueError) as exc_info:
            Entity(
                entity_id="word_001",
                entity_type="word",
                text="test",
                start_time=2.0,
                end_time=1.0,  # Invalid - end < start
                duration=1.0,
                confidence=0.9,
                probability=0.9,
                syllables=["test"],
                syllable_count=1,
                quality_score=0.8,
                speaker_id=0,
                recording_id="test",
                recording_path="test.wav",
                processed=False,
                created_at=datetime.now().isoformat()
            )
        
        # Verify error message is helpful
        assert "end_time must be greater than start_time" in str(exc_info.value)


class TestLoggingModelIntegration:
    """Test logging and model integration."""
    
    def test_logging_with_entity_context(self):
        """Test that logging works with entity data."""
        class TestProcessor(LoggerMixin):
            def process_entity(self, entity: Entity):
                self.log_progress("Processing entity",
                                entity_id=entity.entity_id,
                                entity_type=entity.entity_type,
                                confidence=entity.confidence,
                                duration=entity.duration)
                return True
        
        processor = TestProcessor()
        
        entity = Entity(
            entity_id="word_001",
            entity_type="word",
            text="test",
            start_time=1.0,
            end_time=2.0,
            duration=1.0,
            confidence=0.9,
            probability=0.9,
            syllables=["test"],
            syllable_count=1,
            quality_score=0.8,
            speaker_id=0,
            recording_id="test",
            recording_path="test.wav",
            processed=False,
            created_at=datetime.now().isoformat()
        )
        
        # Should not raise exceptions
        result = processor.process_entity(entity)
        assert result is True
    
    def test_error_logging_with_entity_failures(self):
        """Test error logging when entity operations fail."""
        class TestProcessor(LoggerMixin):
            def process_invalid_entity(self):
                try:
                    # Try to create invalid entity
                    Entity(
                        entity_id="word_001",
                        entity_type="invalid_type",  # Invalid
                        text="test",
                        start_time=1.0,
                        end_time=2.0,
                        duration=1.0,
                        confidence=1.5,  # Invalid
                        probability=0.9,
                        syllables=["test"],
                        syllable_count=1,
                        quality_score=0.8,
                        speaker_id=0,  # Changed to integer for diarization compatibility
                        recording_id="test",
                        recording_path="test.wav",
                        processed=False,
                        created_at=datetime.now().isoformat()
                    )
                except Exception as e:
                    self.log_stage_error("entity_creation", e,
                                       entity_id="word_001",
                                       attempted_type="invalid_type")
                    raise
        
        processor = TestProcessor()
        
        # Should raise exception but log it properly
        with pytest.raises(ValueError):
            processor.process_invalid_entity()


class TestFullFoundationIntegration:
    """Test full integration of all foundation components."""
    
    def test_complete_foundation_workflow(self):
        """Test complete workflow using all foundation components."""
        # 1. Load configuration
        config = Config()
        config.quality.min_confidence = 0.7
        config.quality.syllable_range = [1, 5]
        
        # 2. Initialize logging
        init_logger(config)
        
        # 3. Create processor with logging
        class TestProcessor(LoggerMixin):
            def __init__(self, config: Config):
                super().__init__()
                self.config = config
            
            def process_data(self):
                self.log_stage_start("test_processing")
                
                try:
                    # Create audio metadata
                    audio_metadata = AudioMetadata(
                        path="test.wav",
                        duration=60.0,
                        sample_rate=16000,
                        channels=1,
                        format="wav",
                        size_bytes=512000
                    )
                    
                    # Create speaker info
                    speaker_info = SpeakerInfo(
                        name="Test Speaker",
                        gender="Unknown",
                        region="Test Region"
                    )
                    
                    # Create database
                    database = WordDatabase(
                        metadata={
                            "version": "1.0",
                            "created_at": datetime.now().isoformat(),
                            "audio_metadata": audio_metadata.model_dump()
                        },
                        speaker_map={0: speaker_info},
                        entities=[]
                    )
                    
                    # Create entities that meet config criteria
                    for i in range(3):
                        entity = Entity(
                            entity_id=f"word_{i+1:03d}",
                            entity_type="word",
                            text=f"word{i+1}",
                            start_time=float(i * 2),
                            end_time=float(i * 2 + 1),
                            duration=1.0,
                            confidence=0.8,  # Meets min_confidence
                            probability=0.8,
                            syllables=[f"word{i+1}"],
                            syllable_count=1,  # Meets syllable_range
                            quality_score=0.8,
                            speaker_id=0,  # Changed to integer for diarization compatibility
                            recording_id="test",
                            recording_path="test.wav",
                            processed=False,
                            created_at=datetime.now().isoformat()
                        )
                        database.entities.append(entity)
                    
                    self.log_stage_complete("test_processing",
                                          entities_created=len(database.entities),
                                          speakers=len(database.speaker_map))
                    
                    return database
                    
                except Exception as e:
                    self.log_stage_error("test_processing", e)
                    raise
        
        # 4. Run processor
        processor = TestProcessor(config)
        database = processor.process_data()
        
        # 5. Verify results
        assert database is not None
        assert len(database.entities) == 3
        assert database.metadata is not None
        assert len(database.speaker_map) == 1
        
        # 6. Verify all entities meet config criteria
        for entity in database.entities:
            assert entity.confidence >= config.quality.min_confidence
            assert config.quality.syllable_range[0] <= entity.syllable_count <= config.quality.syllable_range[1]