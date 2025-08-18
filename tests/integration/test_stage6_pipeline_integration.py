"""
Integration tests for Stage 6: Full Pipeline Integration.

Tests complete end-to-end pipeline integration,
Colombian Spanish smart buffering, and error handling.
"""
import pytest
import tempfile
import numpy as np
from pathlib import Path
from unittest.mock import patch, MagicMock

from src.audio_to_json.pipeline import AudioToJsonPipeline, process_audio_to_json
from src.audio_to_json.audio_processor import ProcessedAudio
from src.audio_to_json.transcription import Word
from src.shared.config import Config
from src.shared.models import WordDatabase, Entity, AudioMetadata, SpeakerInfo
from src.shared.exceptions import PipelineError, AudioError, TranscriptionError


class TestFullPipelineIntegration:
    """Test complete pipeline integration from audio to database."""
    
    @patch('src.audio_to_json.pipeline.write_database')
    @patch('src.audio_to_json.pipeline.apply_quality_filters')
    @patch('src.audio_to_json.pipeline.create_entities')
    @patch('src.audio_to_json.pipeline.transcribe_audio')
    @patch('src.audio_to_json.pipeline.process_audio')
    def test_complete_pipeline_flow_integration(self,
                                              mock_process_audio,
                                              mock_transcribe,
                                              mock_create_entities,
                                              mock_apply_filters,
                                              mock_write_db):
        """Test complete pipeline flow integration."""
        config = Config()
        pipeline = AudioToJsonPipeline(config)
        
        # Mock audio processing
        audio_data = np.array([0.1, 0.2, 0.3], dtype=np.float32)
        metadata = AudioMetadata(
            path="test.wav", duration=1.5, sample_rate=16000,
            channels=1, format="wav", size_bytes=1500
        )
        processed_audio = ProcessedAudio(audio_data, 16000, 1.5, metadata)
        mock_process_audio.return_value = processed_audio
        
        # Mock transcription
        words = [
            Word("hola", 0.0, 0.5, 0.9),
            Word("mundo", 0.5, 1.0, 0.8),
            Word("español", 1.0, 1.5, 0.85)
        ]
        mock_transcribe.return_value = words
        
        # Mock entity creation
        entities = []
        for i, word in enumerate(words):
            entity = Entity(
                entity_id=f"word_{i+1:03d}", entity_type="word", text=word.text,
                start_time=word.start_time, end_time=word.end_time,
                duration=word.end_time - word.start_time,
                confidence=word.confidence, probability=word.confidence,
                syllables=[word.text], syllable_count=1, quality_score=0.8,
                speaker_id="speaker_0", recording_id="test_recording",
                recording_path="test.wav", processed=False,
                created_at="2023-01-01T00:00:00"
            )
            entities.append(entity)
        
        mock_create_entities.return_value = entities
        mock_apply_filters.return_value = entities
        mock_write_db.return_value = Path("output.json")
        
        # Execute pipeline
        result = pipeline.process_audio_to_json("test.wav", "output.json")
        
        # Verify all stages called in correct order
        mock_process_audio.assert_called_once_with("test.wav", config)
        mock_transcribe.assert_called_once_with(processed_audio, config.whisper)
        mock_create_entities.assert_called_once()
        mock_apply_filters.assert_called_once()
        mock_write_db.assert_called_once()
        
        # Verify final result
        assert isinstance(result, WordDatabase)
        assert len(result.entities) == 3
        assert result.entities[0].text == "hola"
        assert result.entities[1].text == "mundo"
        assert result.entities[2].text == "español"
    
    def test_pipeline_with_speaker_mapping_integration(self):
        """Test pipeline integration with speaker mapping."""
        config = Config()
        pipeline = AudioToJsonPipeline(config)
        
        speaker_mapping = {
            "0.0-1.0": "speaker_alice",
            "1.0-2.0": "speaker_bob"
        }
        
        with patch('src.audio_to_json.pipeline.process_audio') as mock_process, \
             patch('src.audio_to_json.pipeline.transcribe_audio') as mock_transcribe, \
             patch('src.audio_to_json.pipeline.create_entities') as mock_create, \
             patch('src.audio_to_json.pipeline.apply_quality_filters') as mock_filter:
            
            # Setup mocks
            mock_process.return_value = ProcessedAudio(
                np.array([0.1]), 16000, 1.0,
                AudioMetadata(path="test.wav", duration=1.0, sample_rate=16000,
                             channels=1, format="wav", size_bytes=100)
            )
            mock_transcribe.return_value = [Word("test", 0.5, 1.0, 0.9)]
            mock_create.return_value = []
            mock_filter.return_value = []
            
            pipeline.process_audio_to_json("test.wav", speaker_mapping=speaker_mapping)
            
            # Verify speaker mapping was passed to create_entities
            mock_create.assert_called_once()
            call_args = mock_create.call_args
            assert call_args[0][1] == speaker_mapping  # speaker_mapping argument
    
    def test_pipeline_without_output_integration(self):
        """Test pipeline integration without file output."""
        config = Config()
        pipeline = AudioToJsonPipeline(config)
        
        with patch('src.audio_to_json.pipeline.process_audio') as mock_process, \
             patch('src.audio_to_json.pipeline.transcribe_audio') as mock_transcribe, \
             patch('src.audio_to_json.pipeline.create_entities') as mock_create, \
             patch('src.audio_to_json.pipeline.apply_quality_filters') as mock_filter:
            
            # Setup mocks
            mock_process.return_value = ProcessedAudio(
                np.array([0.1]), 16000, 1.0,
                AudioMetadata(path="test.wav", duration=1.0, sample_rate=16000,
                             channels=1, format="wav", size_bytes=100)
            )
            mock_transcribe.return_value = [Word("test", 0.0, 0.5, 0.9)]
            mock_create.return_value = []
            mock_filter.return_value = []
            
            # Execute without output path
            result = pipeline.process_audio_to_json("test.wav")
            
            # Should still return database
            assert isinstance(result, WordDatabase)


class TestColombianSpanishIntegration:
    """Test Colombian Spanish specific integration features."""
    
    def test_smart_buffering_integration(self):
        """Test smart buffering integration for Colombian Spanish."""
        config = Config()
        pipeline = AudioToJsonPipeline(config)
        
        # Create entities with zero gaps (Colombian Spanish characteristic)
        entities = []
        for i in range(3):
            entity = Entity(
                entity_id=f"word_{i+1:03d}", entity_type="word", text=f"palabra{i+1}",
                start_time=float(i * 0.5), end_time=float((i+1) * 0.5),  # Consecutive words
                duration=0.5, confidence=0.9, probability=0.9,
                syllables=[f"pa{i+1}"], syllable_count=1, quality_score=0.8,
                speaker_id="speaker_0", recording_id="test",
                recording_path="test.wav", processed=False,
                created_at="2023-01-01T00:00:00"
            )
            entities.append(entity)
        
        # Create database with entities
        database = WordDatabase(
            metadata={"version": "1.0", "created_at": "2023-01-01T00:00:00"},
            speaker_map={"speaker_0": SpeakerInfo(name="Test Speaker")},
            entities=entities
        )
        
        # Apply smart buffering
        with patch.object(pipeline, 'log_progress') as mock_progress:
            result = pipeline._apply_smart_buffering(database)
        
        # Verify logging shows zero-gap detection
        mock_progress.assert_called()
        
        # Verify entities are unchanged (no buffer added due to zero gaps)
        assert len(result.entities) == 3
        for i, entity in enumerate(result.entities):
            assert entity.start_time == float(i * 0.5)
            assert entity.end_time == float((i+1) * 0.5)
    
    def test_overlap_detection_integration(self):
        """Test overlap detection integration."""
        config = Config()
        pipeline = AudioToJsonPipeline(config)
        
        # Create entities with overlaps
        entities = [
            Entity(
                entity_id="word_001", entity_type="word", text="overlap1",
                start_time=0.0, end_time=0.6, duration=0.6,  # ends at 0.6
                confidence=0.9, probability=0.9, syllables=["overlap1"],
                syllable_count=1, quality_score=0.8, speaker_id="speaker_0",
                recording_id="test", recording_path="test.wav", processed=False,
                created_at="2023-01-01T00:00:00"
            ),
            Entity(
                entity_id="word_002", entity_type="word", text="overlap2",
                start_time=0.5, end_time=1.0, duration=0.5,  # starts at 0.5 (overlap!)
                confidence=0.9, probability=0.9, syllables=["overlap2"],
                syllable_count=1, quality_score=0.8, speaker_id="speaker_0",
                recording_id="test", recording_path="test.wav", processed=False,
                created_at="2023-01-01T00:00:00"
            )
        ]
        
        database = WordDatabase(
            metadata={"version": "1.0", "created_at": "2023-01-01T00:00:00"},
            speaker_map={"speaker_0": SpeakerInfo(name="Test Speaker")},
            entities=entities
        )
        
        # Apply smart buffering
        with patch.object(pipeline.logger, 'warning') as mock_warning:
            pipeline._apply_smart_buffering(database)
        
        # Should log warning about overlap
        mock_warning.assert_called()
        warning_call = mock_warning.call_args
        assert "overlap" in str(warning_call).lower()


class TestErrorHandlingIntegration:
    """Test error handling integration across pipeline."""
    
    def test_audio_processing_error_integration(self):
        """Test audio processing error integration."""
        config = Config()
        pipeline = AudioToJsonPipeline(config)
        
        with patch('src.audio_to_json.pipeline.process_audio', side_effect=AudioError("Audio error")):
            with pytest.raises(AudioError, match="Audio error"):
                pipeline.process_audio_to_json("nonexistent.wav")
    
    def test_transcription_error_integration(self):
        """Test transcription error integration."""
        config = Config()
        pipeline = AudioToJsonPipeline(config)
        
        with patch('src.audio_to_json.pipeline.process_audio') as mock_process, \
             patch('src.audio_to_json.pipeline.transcribe_audio', side_effect=TranscriptionError("Transcription failed")):
            
            mock_process.return_value = ProcessedAudio(
                np.array([0.1]), 16000, 1.0,
                AudioMetadata(path="test.wav", duration=1.0, sample_rate=16000,
                             channels=1, format="wav", size_bytes=100)
            )
            
            with pytest.raises(TranscriptionError, match="Transcription failed"):
                pipeline.process_audio_to_json("test.wav")
    
    def test_entity_creation_error_integration(self):
        """Test entity creation error integration."""
        config = Config()
        pipeline = AudioToJsonPipeline(config)
        
        with patch('src.audio_to_json.pipeline.process_audio') as mock_process, \
             patch('src.audio_to_json.pipeline.transcribe_audio') as mock_transcribe, \
             patch('src.audio_to_json.pipeline.create_entities', side_effect=Exception("Entity error")):
            
            mock_process.return_value = ProcessedAudio(
                np.array([0.1]), 16000, 1.0,
                AudioMetadata(path="test.wav", duration=1.0, sample_rate=16000,
                             channels=1, format="wav", size_bytes=100)
            )
            mock_transcribe.return_value = [Word("test", 0.0, 0.5, 0.9)]
            
            with pytest.raises(PipelineError, match="Pipeline failed"):
                pipeline.process_audio_to_json("test.wav")
    
    def test_error_logging_integration(self):
        """Test error logging integration."""
        config = Config()
        pipeline = AudioToJsonPipeline(config)
        
        with patch('src.audio_to_json.pipeline.process_audio', side_effect=Exception("Test error")), \
             patch.object(pipeline, 'log_stage_error') as mock_error_log:
            
            with pytest.raises(PipelineError):
                pipeline.process_audio_to_json("test.wav")
            
            # Verify error was logged
            mock_error_log.assert_called_once()


class TestPerformanceIntegration:
    """Test performance-related integration aspects."""
    
    def test_large_audio_pipeline_integration(self):
        """Test pipeline integration with large audio processing."""
        config = Config()
        pipeline = AudioToJsonPipeline(config)
        
        with patch('src.audio_to_json.pipeline.process_audio') as mock_process, \
             patch('src.audio_to_json.pipeline.transcribe_audio') as mock_transcribe, \
             patch('src.audio_to_json.pipeline.create_entities') as mock_create, \
             patch('src.audio_to_json.pipeline.apply_quality_filters') as mock_filter:
            
            # Simulate large audio (10 minutes)
            large_audio = ProcessedAudio(
                np.array([0.1] * (16000 * 600)), 16000, 600.0,  # 10 minutes
                AudioMetadata(path="large.wav", duration=600.0, sample_rate=16000,
                             channels=1, format="wav", size_bytes=10000000)
            )
            mock_process.return_value = large_audio
            
            # Simulate many words (1 word per second)
            words = [Word(f"word{i}", float(i), float(i+0.5), 0.9) for i in range(600)]
            mock_transcribe.return_value = words
            
            # Simulate many entities
            entities = []
            for i, word in enumerate(words):
                entity = Entity(
                    entity_id=f"word_{i+1:04d}", entity_type="word", text=word.text,
                    start_time=word.start_time, end_time=word.end_time,
                    duration=0.5, confidence=0.9, probability=0.9,
                    syllables=[word.text], syllable_count=1, quality_score=0.8,
                    speaker_id="speaker_0", recording_id="large_test",
                    recording_path="large.wav", processed=False,
                    created_at="2023-01-01T00:00:00"
                )
                entities.append(entity)
            
            mock_create.return_value = entities
            mock_filter.return_value = entities
            
            # Execute pipeline
            result = pipeline.process_audio_to_json("large.wav")
            
            # Verify large dataset handling
            assert isinstance(result, WordDatabase)
            assert len(result.entities) == 600
            assert result.metadata is not None
    
    def test_memory_efficient_processing_integration(self):
        """Test memory efficient processing integration."""
        config = Config()
        pipeline = AudioToJsonPipeline(config)
        
        # Test that pipeline handles streaming/chunked processing concepts
        with patch('src.audio_to_json.pipeline.process_audio') as mock_process, \
             patch('src.audio_to_json.pipeline.transcribe_audio') as mock_transcribe, \
             patch('src.audio_to_json.pipeline.create_entities') as mock_create, \
             patch('src.audio_to_json.pipeline.apply_quality_filters') as mock_filter:
            
            # Setup mocks for efficient processing test
            mock_process.return_value = ProcessedAudio(
                np.array([0.1] * 1000), 16000, 1.0,
                AudioMetadata(path="test.wav", duration=1.0, sample_rate=16000,
                             channels=1, format="wav", size_bytes=1000)
            )
            mock_transcribe.return_value = [Word("test", 0.0, 0.5, 0.9)]
            mock_create.return_value = []
            mock_filter.return_value = []
            
            result = pipeline.process_audio_to_json("test.wav")
            
            # Should complete successfully without memory issues
            assert isinstance(result, WordDatabase)


class TestLoggingIntegration:
    """Test logging integration across pipeline."""
    
    def test_comprehensive_logging_integration(self):
        """Test comprehensive logging integration."""
        config = Config()
        pipeline = AudioToJsonPipeline(config)
        
        with patch('src.audio_to_json.pipeline.process_audio') as mock_process, \
             patch('src.audio_to_json.pipeline.transcribe_audio') as mock_transcribe, \
             patch('src.audio_to_json.pipeline.create_entities') as mock_create, \
             patch('src.audio_to_json.pipeline.apply_quality_filters') as mock_filter:
            
            # Setup mocks
            mock_process.return_value = ProcessedAudio(
                np.array([0.1]), 16000, 1.0,
                AudioMetadata(path="test.wav", duration=1.0, sample_rate=16000,
                             channels=1, format="wav", size_bytes=100)
            )
            mock_transcribe.return_value = [Word("test", 0.0, 0.5, 0.9)]
            mock_create.return_value = []
            mock_filter.return_value = []
            
            # Test logging throughout pipeline
            with patch.object(pipeline, 'log_stage_start') as mock_start, \
                 patch.object(pipeline, 'log_progress') as mock_progress, \
                 patch.object(pipeline, 'log_stage_complete') as mock_complete:
                
                pipeline.process_audio_to_json("test.wav")
                
                # Verify comprehensive logging
                mock_start.assert_called()
                assert mock_progress.call_count >= 4  # Multiple stages
                mock_complete.assert_called()
    
    def test_stage_timing_logging_integration(self):
        """Test stage timing logging integration."""
        config = Config()
        pipeline = AudioToJsonPipeline(config)
        
        with patch('src.audio_to_json.pipeline.process_audio') as mock_process, \
             patch('src.audio_to_json.pipeline.transcribe_audio') as mock_transcribe, \
             patch('src.audio_to_json.pipeline.create_entities') as mock_create, \
             patch('src.audio_to_json.pipeline.apply_quality_filters') as mock_filter:
            
            # Setup mocks
            mock_process.return_value = ProcessedAudio(
                np.array([0.1]), 16000, 1.0,
                AudioMetadata(path="test.wav", duration=1.0, sample_rate=16000,
                             channels=1, format="wav", size_bytes=100)
            )
            mock_transcribe.return_value = [Word("test", 0.0, 0.5, 0.9)]
            mock_create.return_value = []
            mock_filter.return_value = []
            
            # Execute and verify timing information is logged
            with patch.object(pipeline, 'log_stage_complete') as mock_complete:
                pipeline.process_audio_to_json("test.wav")
                
                # Final log should include timing information
                mock_complete.assert_called()
                final_call = mock_complete.call_args
                assert "total_time" in str(final_call)


class TestConvenienceFunctionIntegration:
    """Test convenience function integration."""
    
    def test_process_audio_to_json_function_integration(self):
        """Test process_audio_to_json convenience function integration."""
        config = Config()
        
        with patch('src.audio_to_json.pipeline.AudioToJsonPipeline') as mock_pipeline_class:
            mock_pipeline = MagicMock()
            mock_database = WordDatabase(
                metadata={"version": "1.0", "created_at": "2023-01-01"},
                speaker_map={}, entities=[]
            )
            mock_pipeline.process_audio_to_json.return_value = mock_database
            mock_pipeline_class.return_value = mock_pipeline
            
            # Test convenience function
            result = process_audio_to_json("test.wav", config, "output.json")
            
            # Verify function delegation
            mock_pipeline_class.assert_called_once_with(config)
            mock_pipeline.process_audio_to_json.assert_called_once_with(
                "test.wav", "output.json", None, None
            )
            assert result == mock_database
    
    def test_function_parameter_passing_integration(self):
        """Test parameter passing integration in convenience function."""
        config = Config()
        speaker_mapping = {"0.0-1.0": "speaker_a"}
        
        with patch('src.audio_to_json.pipeline.AudioToJsonPipeline') as mock_pipeline_class:
            mock_pipeline = MagicMock()
            mock_pipeline_class.return_value = mock_pipeline
            
            # Test with all parameters
            process_audio_to_json(
                "test.wav", config, "output.json", 
                speaker_mapping, "transcription"
            )
            
            # Verify all parameters passed correctly
            mock_pipeline.process_audio_to_json.assert_called_once_with(
                "test.wav", "output.json", speaker_mapping, "transcription"
            )


class TestEdgeCaseIntegration:
    """Test edge case integration scenarios."""
    
    def test_empty_transcription_integration(self):
        """Test integration with empty transcription results."""
        config = Config()
        pipeline = AudioToJsonPipeline(config)
        
        with patch('src.audio_to_json.pipeline.process_audio') as mock_process, \
             patch('src.audio_to_json.pipeline.transcribe_audio') as mock_transcribe, \
             patch('src.audio_to_json.pipeline.create_entities') as mock_create, \
             patch('src.audio_to_json.pipeline.apply_quality_filters') as mock_filter:
            
            # Setup mocks for empty transcription
            mock_process.return_value = ProcessedAudio(
                np.array([0.1]), 16000, 1.0,
                AudioMetadata(path="silent.wav", duration=1.0, sample_rate=16000,
                             channels=1, format="wav", size_bytes=100)
            )
            mock_transcribe.return_value = []  # No words transcribed
            mock_create.return_value = []
            mock_filter.return_value = []
            
            result = pipeline.process_audio_to_json("silent.wav")
            
            # Should handle gracefully
            assert isinstance(result, WordDatabase)
            assert len(result.entities) == 0
            assert len(result.speaker_map) >= 1  # Default speaker
    
    def test_all_entities_filtered_integration(self):
        """Test integration when all entities are filtered out."""
        config = Config()
        pipeline = AudioToJsonPipeline(config)
        
        with patch('src.audio_to_json.pipeline.process_audio') as mock_process, \
             patch('src.audio_to_json.pipeline.transcribe_audio') as mock_transcribe, \
             patch('src.audio_to_json.pipeline.create_entities') as mock_create, \
             patch('src.audio_to_json.pipeline.apply_quality_filters') as mock_filter:
            
            # Setup mocks
            mock_process.return_value = ProcessedAudio(
                np.array([0.1]), 16000, 1.0,
                AudioMetadata(path="test.wav", duration=1.0, sample_rate=16000,
                             channels=1, format="wav", size_bytes=100)
            )
            mock_transcribe.return_value = [Word("low", 0.0, 0.1, 0.1)]  # Low quality
            
            # Create entity but filter it out
            mock_entity = Entity(
                entity_id="test_001", entity_type="word", text="low",
                start_time=0.0, end_time=0.1, duration=0.1,
                confidence=0.1, probability=0.1, syllables=["low"],
                syllable_count=1, quality_score=0.1, speaker_id="speaker_0",
                recording_id="test", recording_path="test.wav", processed=False,
                created_at="2023-01-01T00:00:00"
            )
            mock_create.return_value = [mock_entity]
            mock_filter.return_value = []  # All filtered out
            
            result = pipeline.process_audio_to_json("low_quality.wav")
            
            # Should handle gracefully
            assert isinstance(result, WordDatabase)
            assert len(result.entities) == 0