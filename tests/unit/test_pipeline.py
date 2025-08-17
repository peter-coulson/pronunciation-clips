"""
Unit tests for pipeline module.

Tests end-to-end pipeline orchestration, stage coordination,
error handling, and Colombian Spanish smart buffering.
"""
import pytest
import numpy as np
from pathlib import Path
from unittest.mock import patch, MagicMock
from datetime import datetime

from src.audio_to_json.pipeline import AudioToJsonPipeline, process_audio_to_json
from src.audio_to_json.audio_processor import ProcessedAudio
from src.audio_to_json.transcription import Word
from src.shared.config import Config
from src.shared.models import WordDatabase, Entity, SpeakerInfo, AudioMetadata
from src.shared.exceptions import PipelineError


class TestAudioToJsonPipeline:
    """Test AudioToJsonPipeline class."""
    
    def test_pipeline_creation(self):
        """Test creating pipeline with config."""
        config = Config()
        pipeline = AudioToJsonPipeline(config)
        
        assert pipeline.config == config
        assert pipeline.logger is not None
    
    @patch('src.audio_to_json.pipeline.write_database')
    @patch('src.audio_to_json.pipeline.apply_quality_filters')
    @patch('src.audio_to_json.pipeline.create_entities')
    @patch('src.audio_to_json.pipeline.transcribe_audio')
    @patch('src.audio_to_json.pipeline.process_audio')
    def test_process_audio_to_json_full_pipeline(self, 
                                               mock_process_audio,
                                               mock_transcribe,
                                               mock_create_entities,
                                               mock_apply_filters,
                                               mock_write_db):
        """Test complete pipeline execution."""
        # Setup mocks
        config = Config()
        pipeline = AudioToJsonPipeline(config)
        
        # Mock processed audio
        audio_data = np.array([0.1, 0.2, 0.3])
        audio_metadata = AudioMetadata(
            path="test.wav", duration=1.0, sample_rate=16000,
            channels=1, format="wav", size_bytes=1000
        )
        mock_processed_audio = ProcessedAudio(audio_data, 16000, 1.0, audio_metadata)
        mock_process_audio.return_value = mock_processed_audio
        
        # Mock transcription
        mock_words = [
            Word("hola", 0.0, 0.5, 0.9),
            Word("mundo", 0.5, 1.0, 0.8)
        ]
        mock_transcribe.return_value = mock_words
        
        # Mock entity creation
        mock_entities = [
            self._create_mock_entity("hola", 0.0, 0.5),
            self._create_mock_entity("mundo", 0.5, 1.0)
        ]
        mock_create_entities.return_value = mock_entities
        
        # Mock quality filtering
        mock_apply_filters.return_value = mock_entities  # All pass
        
        # Mock database writing
        mock_write_db.return_value = Path("output.json")
        
        # Execute pipeline
        result = pipeline.process_audio_to_json("test.wav", "output.json")
        
        # Verify all stages were called
        mock_process_audio.assert_called_once_with("test.wav", config)
        mock_transcribe.assert_called_once_with(mock_processed_audio, config.whisper)
        mock_create_entities.assert_called_once()
        mock_apply_filters.assert_called_once()
        mock_write_db.assert_called_once()
        
        # Verify result
        assert isinstance(result, WordDatabase)
        assert len(result.entities) == 2
        assert "hola" in [e.text for e in result.entities]
        assert "mundo" in [e.text for e in result.entities]
    
    @patch('src.audio_to_json.pipeline.apply_quality_filters')
    @patch('src.audio_to_json.pipeline.create_entities')
    @patch('src.audio_to_json.pipeline.transcribe_audio')
    @patch('src.audio_to_json.pipeline.process_audio')
    def test_process_audio_to_json_without_output(self,
                                                mock_process_audio,
                                                mock_transcribe,
                                                mock_create_entities,
                                                mock_apply_filters):
        """Test pipeline without writing to file."""
        # Setup mocks
        config = Config()
        pipeline = AudioToJsonPipeline(config)
        
        mock_processed_audio = self._create_mock_processed_audio()
        mock_process_audio.return_value = mock_processed_audio
        
        mock_words = [Word("test", 0.0, 0.5, 0.9)]
        mock_transcribe.return_value = mock_words
        
        mock_entities = [self._create_mock_entity("test", 0.0, 0.5)]
        mock_create_entities.return_value = mock_entities
        mock_apply_filters.return_value = mock_entities
        
        # Execute without output path
        result = pipeline.process_audio_to_json("test.wav")
        
        # Should still return database
        assert isinstance(result, WordDatabase)
        assert len(result.entities) == 1
    
    @patch('src.audio_to_json.pipeline.process_audio')
    def test_process_audio_to_json_audio_error(self, mock_process_audio):
        """Test pipeline handling of audio processing errors."""
        config = Config()
        pipeline = AudioToJsonPipeline(config)
        
        # Mock audio processing to fail
        mock_process_audio.side_effect = Exception("Audio processing failed")
        
        with pytest.raises(PipelineError, match="Pipeline failed"):
            pipeline.process_audio_to_json("test.wav")
    
    @patch('src.audio_to_json.pipeline.transcribe_audio')
    @patch('src.audio_to_json.pipeline.process_audio')
    def test_process_audio_to_json_transcription_error(self, 
                                                     mock_process_audio,
                                                     mock_transcribe):
        """Test pipeline handling of transcription errors."""
        config = Config()
        pipeline = AudioToJsonPipeline(config)
        
        mock_process_audio.return_value = self._create_mock_processed_audio()
        mock_transcribe.side_effect = Exception("Transcription failed")
        
        with pytest.raises(PipelineError, match="Pipeline failed"):
            pipeline.process_audio_to_json("test.wav")
    
    def test_process_audio_to_json_resume_not_implemented(self):
        """Test that resume functionality raises NotImplementedError."""
        config = Config()
        pipeline = AudioToJsonPipeline(config)
        
        with pytest.raises(NotImplementedError):
            pipeline.process_audio_to_json("test.wav", resume_from_stage="transcription")
    
    @patch('src.audio_to_json.pipeline.apply_quality_filters')
    @patch('src.audio_to_json.pipeline.create_entities')
    @patch('src.audio_to_json.pipeline.transcribe_audio')
    @patch('src.audio_to_json.pipeline.process_audio')
    def test_process_audio_to_json_with_speaker_mapping(self,
                                                      mock_process_audio,
                                                      mock_transcribe,
                                                      mock_create_entities,
                                                      mock_apply_filters):
        """Test pipeline with speaker mapping."""
        config = Config()
        pipeline = AudioToJsonPipeline(config)
        
        mock_process_audio.return_value = self._create_mock_processed_audio()
        mock_transcribe.return_value = [Word("test", 0.0, 0.5, 0.9)]
        mock_entities = [self._create_mock_entity("test", 0.0, 0.5)]
        mock_create_entities.return_value = mock_entities
        mock_apply_filters.return_value = mock_entities
        
        speaker_mapping = {"0.0-1.0": "speaker_a"}
        
        result = pipeline.process_audio_to_json("test.wav", 
                                              speaker_mapping=speaker_mapping)
        
        # Verify speaker mapping was passed to create_entities
        mock_create_entities.assert_called_once()
        call_args = mock_create_entities.call_args
        assert call_args[0][1] == speaker_mapping  # Second argument is speaker_mapping
    
    @patch('src.audio_to_json.pipeline.apply_quality_filters')
    @patch('src.audio_to_json.pipeline.create_entities')
    @patch('src.audio_to_json.pipeline.transcribe_audio')
    @patch('src.audio_to_json.pipeline.process_audio')
    def test_process_audio_to_json_logging(self,
                                         mock_process_audio,
                                         mock_transcribe,
                                         mock_create_entities,
                                         mock_apply_filters):
        """Test pipeline logging functionality."""
        config = Config()
        pipeline = AudioToJsonPipeline(config)
        
        mock_process_audio.return_value = self._create_mock_processed_audio()
        mock_transcribe.return_value = [Word("test", 0.0, 0.5, 0.9)]
        mock_entities = [self._create_mock_entity("test", 0.0, 0.5)]
        mock_create_entities.return_value = mock_entities
        mock_apply_filters.return_value = mock_entities
        
        with patch.object(pipeline, 'log_stage_start') as mock_start, \
             patch.object(pipeline, 'log_progress') as mock_progress, \
             patch.object(pipeline, 'log_stage_complete') as mock_complete:
            
            pipeline.process_audio_to_json("test.wav")
            
            # Verify logging calls
            mock_start.assert_called_once()
            assert mock_progress.call_count >= 4  # At least 4 progress logs
            mock_complete.assert_called_once()
    
    def test_generate_recording_id(self):
        """Test recording ID generation."""
        config = Config()
        pipeline = AudioToJsonPipeline(config)
        
        audio_file = Path("test-audio file.wav")
        recording_id = pipeline._generate_recording_id(audio_file)
        
        assert "rec_test_audio_file_" in recording_id
        assert len(recording_id) > 20  # Should include timestamp
    
    def test_create_database(self):
        """Test database creation with entities and metadata."""
        config = Config()
        pipeline = AudioToJsonPipeline(config)
        
        entities = [
            self._create_mock_entity("hello", 0.0, 0.5, speaker_id="speaker_1"),
            self._create_mock_entity("world", 0.5, 1.0, speaker_id="speaker_2")
        ]
        
        processed_audio = self._create_mock_processed_audio()
        
        database = pipeline._create_database(entities, processed_audio)
        
        assert isinstance(database, WordDatabase)
        assert len(database.entities) == 2
        assert len(database.speaker_map) == 2
        assert "speaker_1" in database.speaker_map
        assert "speaker_2" in database.speaker_map
        assert database.metadata["version"] == "1.0"
        assert database.metadata["entity_count"] == 2
        assert database.metadata["audio_duration"] == 1.0
    
    def test_create_database_no_entities(self):
        """Test database creation with no entities."""
        config = Config()
        pipeline = AudioToJsonPipeline(config)
        
        processed_audio = self._create_mock_processed_audio()
        
        database = pipeline._create_database([], processed_audio)
        
        assert isinstance(database, WordDatabase)
        assert len(database.entities) == 0
        assert len(database.speaker_map) == 1  # Default speaker
        assert "speaker_0" in database.speaker_map
    
    def test_apply_smart_buffering_zero_gaps(self):
        """Test smart buffering with zero gaps (Colombian Spanish characteristic)."""
        config = Config()
        pipeline = AudioToJsonPipeline(config)
        
        # Create entities with zero gaps (continuous speech)
        entities = [
            self._create_mock_entity("palabra", 0.0, 0.5),  # ends at 0.5
            self._create_mock_entity("siguiente", 0.5, 1.0),  # starts at 0.5 (zero gap)
            self._create_mock_entity("final", 1.0, 1.5)  # starts at 1.0 (zero gap)
        ]
        
        database = WordDatabase(
            metadata={"version": "1.0", "created_at": datetime.now().isoformat()},
            speaker_map={"speaker_0": SpeakerInfo(name="Test Speaker")},
            entities=entities
        )
        
        with patch.object(pipeline, 'log_progress') as mock_progress:
            result = pipeline._apply_smart_buffering(database)
        
        # Should detect zero gaps and log appropriately
        mock_progress.assert_called()
        
        # Database should be returned unchanged (no buffer applied)
        assert len(result.entities) == 3
        assert result.entities[0].end_time == 0.5
        assert result.entities[1].start_time == 0.5
    
    def test_apply_smart_buffering_overlaps(self):
        """Test smart buffering overlap detection."""
        config = Config()
        pipeline = AudioToJsonPipeline(config)
        
        # Create entities with overlaps
        entities = [
            self._create_mock_entity("overlap1", 0.0, 0.6),  # ends at 0.6
            self._create_mock_entity("overlap2", 0.5, 1.0)   # starts at 0.5 (overlap!)
        ]
        
        database = WordDatabase(
            metadata={"version": "1.0", "created_at": datetime.now().isoformat()},
            speaker_map={"speaker_0": SpeakerInfo(name="Test Speaker")},
            entities=entities
        )
        
        with patch.object(pipeline.logger, 'warning') as mock_warning:
            pipeline._apply_smart_buffering(database)
        
        # Should log warning about overlap
        mock_warning.assert_called_once()
        warning_call = mock_warning.call_args
        assert "overlap" in str(warning_call).lower()
    
    def test_apply_smart_buffering_normal_gaps(self):
        """Test smart buffering with normal gaps."""
        config = Config()
        pipeline = AudioToJsonPipeline(config)
        
        # Create entities with normal gaps
        entities = [
            self._create_mock_entity("word1", 0.0, 0.5),   # ends at 0.5
            self._create_mock_entity("word2", 0.8, 1.2)    # starts at 0.8 (0.3s gap)
        ]
        
        database = WordDatabase(
            metadata={"version": "1.0", "created_at": datetime.now().isoformat()},
            speaker_map={"speaker_0": SpeakerInfo(name="Test Speaker")},
            entities=entities
        )
        
        result = pipeline._apply_smart_buffering(database)
        
        # Should process normally without warnings
        assert len(result.entities) == 2
    
    def test_apply_smart_buffering_empty_database(self):
        """Test smart buffering with empty database."""
        config = Config()
        pipeline = AudioToJsonPipeline(config)
        
        database = WordDatabase(
            metadata={"version": "1.0", "created_at": datetime.now().isoformat()},
            speaker_map={"speaker_0": SpeakerInfo(name="Test Speaker")},
            entities=[]
        )
        
        result = pipeline._apply_smart_buffering(database)
        
        # Should handle empty database gracefully
        assert len(result.entities) == 0
    
    def _create_mock_entity(self, text: str, start_time: float, end_time: float, 
                           speaker_id: str = "speaker_0") -> Entity:
        """Helper to create mock Entity objects."""
        return Entity(
            entity_id=f"word_{text}",
            entity_type="word",
            text=text,
            start_time=start_time,
            end_time=end_time,
            duration=end_time - start_time,
            confidence=0.9,
            probability=0.9,
            syllables=[text],
            syllable_count=1,
            quality_score=0.8,
            speaker_id=speaker_id,
            recording_id="test_recording",
            recording_path="test.wav",
            processed=False,
            created_at=datetime.now().isoformat()
        )
    
    def _create_mock_processed_audio(self) -> ProcessedAudio:
        """Helper to create mock ProcessedAudio objects."""
        audio_data = np.array([0.1, 0.2, 0.3])
        metadata = AudioMetadata(
            path="test.wav", duration=1.0, sample_rate=16000,
            channels=1, format="wav", size_bytes=1000
        )
        return ProcessedAudio(audio_data, 16000, 1.0, metadata)


class TestProcessAudioToJsonFunction:
    """Test standalone process_audio_to_json function."""
    
    @patch('src.audio_to_json.pipeline.AudioToJsonPipeline')
    def test_process_audio_to_json_function(self, mock_pipeline_class):
        """Test convenience process_audio_to_json function."""
        # Setup mocks
        mock_pipeline = MagicMock()
        mock_database = MagicMock()
        mock_pipeline.process_audio_to_json.return_value = mock_database
        mock_pipeline_class.return_value = mock_pipeline
        
        config = Config()
        
        result = process_audio_to_json(
            "test.wav", 
            config,
            output_path="output.json",
            speaker_mapping={"0.0-1.0": "speaker_a"},
            resume_from_stage=None
        )
        
        # Verify function calls
        mock_pipeline_class.assert_called_once_with(config)
        mock_pipeline.process_audio_to_json.assert_called_once_with(
            "test.wav",
            "output.json",
            {"0.0-1.0": "speaker_a"},
            None
        )
        assert result == mock_database
    
    @patch('src.audio_to_json.pipeline.AudioToJsonPipeline')
    def test_process_audio_to_json_function_error_propagation(self, mock_pipeline_class):
        """Test that the function properly propagates errors."""
        # Setup mocks
        mock_pipeline = MagicMock()
        mock_pipeline.process_audio_to_json.side_effect = PipelineError("Test error")
        mock_pipeline_class.return_value = mock_pipeline
        
        config = Config()
        
        with pytest.raises(PipelineError, match="Test error"):
            process_audio_to_json("test.wav", config)


class TestPipelineEdgeCases:
    """Test edge cases and boundary conditions."""
    
    @patch('src.audio_to_json.pipeline.apply_quality_filters')
    @patch('src.audio_to_json.pipeline.create_entities')
    @patch('src.audio_to_json.pipeline.transcribe_audio')
    @patch('src.audio_to_json.pipeline.process_audio')
    def test_pipeline_with_no_words_transcribed(self,
                                              mock_process_audio,
                                              mock_transcribe,
                                              mock_create_entities,
                                              mock_apply_filters):
        """Test pipeline when no words are transcribed."""
        config = Config()
        pipeline = AudioToJsonPipeline(config)
        
        mock_process_audio.return_value = self._create_mock_processed_audio()
        mock_transcribe.return_value = []  # No words transcribed
        mock_create_entities.return_value = []
        mock_apply_filters.return_value = []
        
        result = pipeline.process_audio_to_json("silent.wav")
        
        # Should still create valid database
        assert isinstance(result, WordDatabase)
        assert len(result.entities) == 0
        assert len(result.speaker_map) >= 1  # Default speaker
    
    @patch('src.audio_to_json.pipeline.apply_quality_filters')
    @patch('src.audio_to_json.pipeline.create_entities')
    @patch('src.audio_to_json.pipeline.transcribe_audio')
    @patch('src.audio_to_json.pipeline.process_audio')
    def test_pipeline_all_entities_filtered_out(self,
                                               mock_process_audio,
                                               mock_transcribe,
                                               mock_create_entities,
                                               mock_apply_filters):
        """Test pipeline when all entities are filtered out by quality."""
        config = Config()
        pipeline = AudioToJsonPipeline(config)
        
        mock_process_audio.return_value = self._create_mock_processed_audio()
        mock_transcribe.return_value = [Word("low", 0.0, 0.1, 0.1)]  # Low quality
        
        # Create entity but filter it out
        mock_entity = self._create_mock_entity("low", 0.0, 0.1)
        mock_create_entities.return_value = [mock_entity]
        mock_apply_filters.return_value = []  # All filtered out
        
        result = pipeline.process_audio_to_json("low_quality.wav")
        
        # Should still create valid database
        assert isinstance(result, WordDatabase)
        assert len(result.entities) == 0
    
    @patch('src.audio_to_json.pipeline.apply_quality_filters')
    @patch('src.audio_to_json.pipeline.create_entities')
    @patch('src.audio_to_json.pipeline.transcribe_audio')
    @patch('src.audio_to_json.pipeline.process_audio')
    def test_pipeline_with_very_long_audio(self,
                                         mock_process_audio,
                                         mock_transcribe,
                                         mock_create_entities,
                                         mock_apply_filters):
        """Test pipeline with very long audio file."""
        config = Config()
        pipeline = AudioToJsonPipeline(config)
        
        # Mock very long audio (1 hour)
        long_audio_data = np.array([0.1] * (16000 * 3600))  # 1 hour at 16kHz
        metadata = AudioMetadata(
            path="long.wav", duration=3600.0, sample_rate=16000,
            channels=1, format="wav", size_bytes=100000000
        )
        mock_long_audio = ProcessedAudio(long_audio_data, 16000, 3600.0, metadata)
        mock_process_audio.return_value = mock_long_audio
        
        # Mock many words
        mock_words = [Word(f"word{i}", i, i+0.5, 0.9) for i in range(0, 100, 1)]
        mock_transcribe.return_value = mock_words
        
        # Mock entities
        mock_entities = [self._create_mock_entity(f"word{i}", i, i+0.5) for i in range(100)]
        mock_create_entities.return_value = mock_entities
        mock_apply_filters.return_value = mock_entities
        
        result = pipeline.process_audio_to_json("long.wav")
        
        # Should handle long audio successfully
        assert isinstance(result, WordDatabase)
        assert result.metadata["audio_duration"] == 3600.0
        assert len(result.entities) == 100
    
    def test_pipeline_error_logging(self):
        """Test error logging in pipeline."""
        config = Config()
        pipeline = AudioToJsonPipeline(config)
        
        with patch('src.audio_to_json.pipeline.process_audio', side_effect=Exception("Test error")), \
             patch.object(pipeline, 'log_stage_error') as mock_error:
            
            with pytest.raises(PipelineError):
                pipeline.process_audio_to_json("error.wav")
            
            # Verify error logging
            mock_error.assert_called_once()
    
    def _create_mock_entity(self, text: str, start_time: float, end_time: float) -> Entity:
        """Helper to create mock Entity objects."""
        return Entity(
            entity_id=f"word_{text}",
            entity_type="word",
            text=text,
            start_time=start_time,
            end_time=end_time,
            duration=end_time - start_time,
            confidence=0.9,
            probability=0.9,
            syllables=[text],
            syllable_count=1,
            quality_score=0.8,
            speaker_id="speaker_0",
            recording_id="test_recording",
            recording_path="test.wav",
            processed=False,
            created_at=datetime.now().isoformat()
        )
    
    def _create_mock_processed_audio(self) -> ProcessedAudio:
        """Helper to create mock ProcessedAudio objects."""
        audio_data = np.array([0.1, 0.2, 0.3])
        metadata = AudioMetadata(
            path="test.wav", duration=1.0, sample_rate=16000,
            channels=1, format="wav", size_bytes=1000
        )
        return ProcessedAudio(audio_data, 16000, 1.0, metadata)