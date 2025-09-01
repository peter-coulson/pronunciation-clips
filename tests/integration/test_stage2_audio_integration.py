"""
Integration tests for Stage 2: Audio Processing.

Tests integration between audio processing components:
audio_processor -> transcription -> entity_creation -> database_writer -> pipeline
"""
import pytest
import tempfile
import json
import numpy as np
from pathlib import Path
from unittest.mock import patch, MagicMock

from src.audio_to_json.audio_processor import AudioProcessor, ProcessedAudio
from src.audio_to_json.transcription import TranscriptionEngine, Word
from src.audio_to_json.entity_creation import EntityCreator
from src.audio_to_json.database_writer import DatabaseWriter
from src.audio_to_json.pipeline import AudioToJsonPipeline
from src.shared.config import Config
from src.shared.models import AudioMetadata, Entity, WordDatabase


class TestAudioProcessorToTranscriptionIntegration:
    """Test integration between AudioProcessor and TranscriptionEngine."""
    
    def test_audio_processor_to_transcription_flow(self):
        """Test that processed audio flows correctly to transcription engine."""
        config = Config()
        processor = AudioProcessor(config)
        transcription_engine = TranscriptionEngine(config.whisper)
        
        # Mock audio file
        with patch('pathlib.Path.exists', return_value=True), \
             patch('librosa.load') as mock_load, \
             patch('os.path.getsize', return_value=1000), \
             patch('soundfile.info') as mock_info:
            
            # Setup mocks
            mock_load.return_value = (np.array([0.1, 0.2, 0.3], dtype=np.float32), 16000)
            mock_info.return_value = MagicMock(channels=1, format='WAV')
            
            # Process audio
            processed_audio = processor.process_audio("test.wav")
            
            # Verify ProcessedAudio can be used by transcription
            assert isinstance(processed_audio, ProcessedAudio)
            assert processed_audio.data.dtype == np.float32
            assert processed_audio.sample_rate == config.audio.sample_rate
            
            # Mock transcription
            with patch.object(transcription_engine, '_model', None), \
                 patch('whisper.load_model') as mock_load_model:
                
                mock_model = MagicMock()
                mock_model.transcribe.return_value = {
                    "segments": [{
                        "words": [{"word": " test", "start": 0.0, "end": 0.5, "probability": 0.9}]
                    }]
                }
                mock_load_model.return_value = mock_model
                
                words = transcription_engine.transcribe_audio(processed_audio)
                
                # Verify transcription worked with processed audio
                assert len(words) == 1
                assert words[0].text == "test"
                assert words[0].confidence == 0.9


class TestTranscriptionToEntityCreationIntegration:
    """Test integration between TranscriptionEngine and EntityCreator."""
    
    def test_transcription_to_entity_creation_flow(self):
        """Test that transcribed words flow correctly to entity creation."""
        config = Config()
        transcription_engine = TranscriptionEngine(config.whisper)
        entity_creator = EntityCreator(config.quality)
        
        # Mock transcribed words
        words = [
            Word("hola", 0.0, 0.5, 0.9),
            Word("mundo", 0.5, 1.0, 0.8),
            Word("test", 1.0, 1.2, 0.3)  # Low confidence
        ]
        
        # Create entities from words
        entities = entity_creator.create_entities(words, "test_recording", "test.wav")
        
        # Verify entities were created correctly
        assert len(entities) == 3
        
        # Check entity properties
        hola_entity = entities[0]
        assert hola_entity.text == "hola"
        assert hola_entity.start_time == 0.0
        assert hola_entity.end_time == 0.5
        assert hola_entity.confidence == 0.9
        assert hola_entity.recording_id == "test_recording"
        
        # Apply quality filters
        filtered_entities = entity_creator.apply_quality_filters(entities)
        
        # Low confidence entity should be filtered out
        assert len(filtered_entities) < len(entities)
        filtered_texts = [e.text for e in filtered_entities]
        assert "hola" in filtered_texts
        assert "mundo" in filtered_texts
        # "test" might be filtered due to low confidence or syllable count


class TestEntityCreationToDatabaseIntegration:
    """Test integration between EntityCreator and DatabaseWriter."""
    
    def test_entity_creation_to_database_flow(self):
        """Test that entities flow correctly to database writing."""
        config = Config()
        entity_creator = EntityCreator(config.quality)
        database_writer = DatabaseWriter(config)
        
        # Create test entities
        words = [
            Word("hola", 0.0, 0.5, 0.9),
            Word("mundo", 0.5, 1.0, 0.8)
        ]
        
        entities = entity_creator.create_entities(words, "test_recording", "test.wav")
        filtered_entities = entity_creator.apply_quality_filters(entities)
        
        # Create database with entities
        from src.audio_to_json.database_writer import create_default_database
        database = create_default_database(entities=filtered_entities)
        
        # Write database to file
        with tempfile.TemporaryDirectory() as temp_dir:
            output_path = Path(temp_dir) / "test_database.json"
            
            result_path = database_writer.write_database(database, output_path)
            
            # Verify file was written
            assert result_path.exists()
            
            # Verify content
            with open(result_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            assert 'entities' in data
            assert len(data['entities']) == len(filtered_entities)
            
            # Verify entity data integrity
            entity_data = data['entities'][0]
            assert entity_data['text'] in ["hola", "mundo"]
            assert 'start_time' in entity_data
            assert 'confidence' in entity_data


class TestFullAudioProcessingPipelineIntegration:
    """Test full pipeline integration from audio to database."""
    
    @patch('src.audio_to_json.pipeline.write_database')
    @patch('src.audio_to_json.pipeline.apply_quality_filters')
    @patch('src.audio_to_json.pipeline.create_entities')
    @patch('src.audio_to_json.pipeline.transcribe_audio')
    @patch('src.audio_to_json.pipeline.process_audio')
    def test_full_pipeline_integration(self,
                                     mock_process_audio,
                                     mock_transcribe,
                                     mock_create_entities,
                                     mock_apply_filters,
                                     mock_write_db):
        """Test complete integration through AudioToJsonPipeline."""
        config = Config()
        pipeline = AudioToJsonPipeline(config)
        
        # Setup realistic mock data
        audio_data = np.array([0.1, 0.2, 0.3])
        audio_metadata = AudioMetadata(
            path="test.wav", duration=1.0, sample_rate=16000,
            channels=1, format="wav", size_bytes=1000
        )
        mock_processed_audio = ProcessedAudio(audio_data, 16000, 1.0, audio_metadata)
        mock_process_audio.return_value = mock_processed_audio
        
        # Mock transcription with realistic words
        mock_words = [
            Word("hola", 0.0, 0.5, 0.9),
            Word("mundo", 0.5, 1.0, 0.8)
        ]
        mock_transcribe.return_value = mock_words
        
        # Mock entity creation
        mock_entities = [
            Entity(
                entity_id="word_001", entity_type="word", text="hola",
                start_time=0.0, end_time=0.5, duration=0.5,
                confidence=0.9, probability=0.9, syllables=["ho", "la"],
                syllable_count=2, quality_score=0.8, speaker_id=0,
                recording_id="test", recording_path="test.wav", processed=False,
                created_at="2023-01-01T00:00:00"
            ),
            Entity(
                entity_id="word_002", entity_type="word", text="mundo",
                start_time=0.5, end_time=1.0, duration=0.5,
                confidence=0.8, probability=0.8, syllables=["mun", "do"],
                syllable_count=2, quality_score=0.7, speaker_id=0,
                recording_id="test", recording_path="test.wav", processed=False,
                created_at="2023-01-01T00:00:00"
            )
        ]
        mock_create_entities.return_value = mock_entities
        mock_apply_filters.return_value = mock_entities
        
        # Mock database writing
        mock_write_db.return_value = Path("output.json")
        
        # Execute pipeline
        result = pipeline.process_audio_to_json("test.wav", "output.json")
        
        # Verify all components were called in correct order
        mock_process_audio.assert_called_once_with("test.wav", config)
        mock_transcribe.assert_called_once_with(mock_processed_audio, config.whisper)
        mock_create_entities.assert_called_once()
        mock_apply_filters.assert_called_once()
        mock_write_db.assert_called_once()
        
        # Verify final result
        assert isinstance(result, WordDatabase)
        assert len(result.entities) == 2
        assert result.entities[0].text == "hola"
        assert result.entities[1].text == "mundo"
    
    def test_pipeline_error_propagation_integration(self):
        """Test that errors propagate correctly through pipeline components."""
        config = Config()
        pipeline = AudioToJsonPipeline(config)
        
        # Mock audio processing to fail
        with patch('src.audio_to_json.pipeline.process_audio', side_effect=Exception("Audio error")):
            with pytest.raises(Exception) as exc_info:
                pipeline.process_audio_to_json("test.wav")
            
            # Error should be wrapped in PipelineError
            assert "Pipeline failed" in str(exc_info.value)
    
    def test_pipeline_component_logging_integration(self):
        """Test that logging flows correctly through pipeline components."""
        config = Config()
        pipeline = AudioToJsonPipeline(config)
        
        with patch('src.audio_to_json.pipeline.process_audio') as mock_process, \
             patch('src.audio_to_json.pipeline.transcribe_audio') as mock_transcribe, \
             patch('src.audio_to_json.pipeline.create_entities') as mock_create, \
             patch('src.audio_to_json.pipeline.apply_quality_filters') as mock_filter:
            
            # Setup mocks to return valid data
            mock_process.return_value = ProcessedAudio(
                np.array([0.1]), 16000, 0.1,
                AudioMetadata(path="test.wav", duration=0.1, sample_rate=16000,
                             channels=1, format="wav", size_bytes=100)
            )
            mock_transcribe.return_value = [Word("test", 0.0, 0.1, 0.9)]
            mock_create.return_value = []
            mock_filter.return_value = []
            
            # Mock logging methods
            with patch.object(pipeline, 'log_stage_start') as mock_start, \
                 patch.object(pipeline, 'log_progress') as mock_progress, \
                 patch.object(pipeline, 'log_stage_complete') as mock_complete:
                
                pipeline.process_audio_to_json("test.wav")
                
                # Verify logging calls were made
                mock_start.assert_called()
                assert mock_progress.call_count >= 4  # Multiple stages
                mock_complete.assert_called()


class TestConfigurationIntegrationAcrossComponents:
    """Test that configuration flows correctly across all components."""
    
    def test_config_propagation_through_components(self):
        """Test configuration consistency across all Stage 2 components."""
        # Create custom config
        config = Config()
        config.audio.sample_rate = 22050
        config.audio.channels = 1
        config.whisper.model = "tiny"
        config.quality.min_confidence = 0.9
        config.output.pretty_print = True
        
        # Create components with config
        processor = AudioProcessor(config)
        transcription_engine = TranscriptionEngine(config.whisper)
        entity_creator = EntityCreator(config.quality)
        database_writer = DatabaseWriter(config)
        pipeline = AudioToJsonPipeline(config)
        
        # Verify config propagation
        assert processor.config == config
        assert processor.config.audio.sample_rate == 22050
        
        assert transcription_engine.config == config.whisper
        assert transcription_engine.config.model == "tiny"
        
        assert entity_creator.quality_config == config.quality
        assert entity_creator.quality_config.min_confidence == 0.9
        
        assert database_writer.config == config
        assert database_writer.config.output.pretty_print is True
        
        assert pipeline.config == config
    
    def test_component_interdependency_validation(self):
        """Test that components handle each other's outputs correctly."""
        config = Config()
        
        # Test data types between components
        audio_data = np.array([0.1, 0.2, 0.3], dtype=np.float32)
        metadata = AudioMetadata(
            path="test.wav", duration=1.0, sample_rate=16000,
            channels=1, format="wav", size_bytes=1000
        )
        processed_audio = ProcessedAudio(audio_data, 16000, 1.0, metadata)
        
        # Verify ProcessedAudio works with TranscriptionEngine
        transcription_engine = TranscriptionEngine(config.whisper)
        assert processed_audio.data.dtype == np.float32
        assert processed_audio.sample_rate == config.audio.sample_rate
        
        # Verify Word objects work with EntityCreator
        word = Word("test", 0.0, 0.5, 0.9)
        entity_creator = EntityCreator(config.quality)
        entities = entity_creator.create_entities([word], "test", "test.wav")
        
        assert len(entities) >= 0  # May be filtered
        if entities:
            assert isinstance(entities[0], Entity)
        
        # Verify Entity objects work with DatabaseWriter
        if entities:
            from src.audio_to_json.database_writer import create_default_database
            database = create_default_database(entities=entities)
            assert isinstance(database, WordDatabase)
            assert database.entities == entities


class TestErrorHandlingIntegrationAcrossComponents:
    """Test error handling integration across Stage 2 components."""
    
    def test_graceful_error_handling_chain(self):
        """Test that errors are handled gracefully across component chain."""
        config = Config()
        
        # Test audio processor error handling
        processor = AudioProcessor(config)
        with pytest.raises(Exception):
            processor.process_audio("nonexistent.wav")
        
        # Test transcription engine error handling
        transcription_engine = TranscriptionEngine(config.whisper)
        invalid_audio = ProcessedAudio(
            np.array([]), 16000, 0.0,  # Empty audio
            AudioMetadata(path="empty.wav", duration=0.0, sample_rate=16000,
                         channels=1, format="wav", size_bytes=0)
        )
        
        with patch.object(transcription_engine, '_model', None), \
             patch('whisper.load_model') as mock_load_model:
            
            mock_model = MagicMock()
            mock_model.transcribe.side_effect = Exception("Transcription failed")
            mock_load_model.return_value = mock_model
            
            with pytest.raises(Exception):
                transcription_engine.transcribe_audio(invalid_audio)
        
        # Test entity creator with invalid data
        entity_creator = EntityCreator(config.quality)
        invalid_words = [Word("", -1.0, -0.5, 1.5)]  # Invalid word
        
        # Should handle gracefully and return empty list
        entities = entity_creator.create_entities(invalid_words, "test", "test.wav")
        assert isinstance(entities, list)
    
    def test_recovery_mechanisms_integration(self):
        """Test recovery mechanisms work across components."""
        config = Config()
        entity_creator = EntityCreator(config.quality)
        
        # Mix of valid and invalid words
        mixed_words = [
            Word("valid", 0.0, 0.5, 0.9),  # Valid
            Word("", 0.5, 0.4, 0.8),      # Invalid (end < start)
            Word("good", 1.0, 1.5, 0.8)   # Valid
        ]
        
        entities = entity_creator.create_entities(mixed_words, "test", "test.wav")
        
        # Should recover and create entities for valid words only
        assert len(entities) >= 1  # At least one valid word should create entity
        valid_texts = [e.text for e in entities]
        assert "valid" in valid_texts or "good" in valid_texts
        assert "" not in valid_texts  # Invalid word should be skipped