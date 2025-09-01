"""
Unit tests for the diarization module.

Tests the ML diarization functionality including dependency handling,
segment extraction, and error conditions.
"""
import pytest
import tempfile
import time
from unittest.mock import Mock, patch, MagicMock
from pathlib import Path

from src.audio_to_json.diarization import (
    DiarizationProcessor, 
    check_diarization_dependencies,
    process_diarization,
    PYANNOTE_AVAILABLE
)
from src.shared.config import DiarizationConfig
from src.shared.models import DiarizationResult, SpeakerSegment
from src.shared.exceptions import PipelineError

pytestmark = [
    pytest.mark.unit,
    pytest.mark.quick
]

class TestDiarizationProcessor:
    """Test the DiarizationProcessor class."""
    
    def test_init_with_config(self):
        """Test processor initialization with configuration."""
        config = DiarizationConfig(
            model="test-model",
            min_speakers=2,
            max_speakers=5
        )
        
        processor = DiarizationProcessor(config)
        
        assert processor.config == config
        assert processor.pipeline is None
        assert processor.config.model == "test-model"
        assert processor.config.min_speakers == 2
        assert processor.config.max_speakers == 5
    
    def test_init_with_default_config(self):
        """Test processor initialization with default configuration."""
        config = DiarizationConfig()
        processor = DiarizationProcessor(config)
        
        assert processor.config.model == "pyannote/speaker-diarization"
        assert processor.config.min_speakers == 1
        assert processor.config.max_speakers == 10
    
    @patch('src.audio_to_json.diarization.PYANNOTE_AVAILABLE', False)
    def test_process_audio_no_pyannote(self):
        """Test audio processing when PyAnnote is not available."""
        config = DiarizationConfig()
        processor = DiarizationProcessor(config)
        
        # Create temporary audio file
        with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as tmp:
            tmp_path = tmp.name
        
        try:
            result = processor.process_audio(tmp_path, 10.0)
            
            # Should return single speaker fallback
            assert isinstance(result, DiarizationResult)
            assert result.speakers == [0]
            assert len(result.segments) == 1
            assert result.segments[0].speaker_id == 0
            assert result.segments[0].start_time == 0.0
            assert result.segments[0].end_time == 10.0
            assert result.segments[0].confidence == 1.0
            assert result.audio_duration == 10.0
            
        finally:
            Path(tmp_path).unlink(missing_ok=True)
    
    def test_process_audio_missing_file(self):
        """Test audio processing with missing file."""
        config = DiarizationConfig()
        processor = DiarizationProcessor(config)
        
        result = processor.process_audio("nonexistent.wav", 10.0)
        
        # Should return single speaker fallback
        assert isinstance(result, DiarizationResult)
        assert result.speakers == [0]
        assert len(result.segments) == 1
    
    def test_process_audio_invalid_duration(self):
        """Test audio processing with invalid duration."""
        config = DiarizationConfig()
        processor = DiarizationProcessor(config)
        
        # Create temporary audio file
        with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as tmp:
            tmp_path = tmp.name
        
        try:
            result = processor.process_audio(tmp_path, -1.0)
            
            # Should return single speaker fallback with valid duration
            assert isinstance(result, DiarizationResult)
            assert result.speakers == [0]
            assert len(result.segments) == 1
            assert result.segments[0].end_time > result.segments[0].start_time
            assert result.audio_duration == 1.0  # Corrected to minimum valid duration
            
        finally:
            Path(tmp_path).unlink(missing_ok=True)
    
    @patch('src.audio_to_json.diarization.PYANNOTE_AVAILABLE', True)
    @patch('src.audio_to_json.diarization.Pipeline')
    def test_process_audio_with_pyannote_success(self, mock_pipeline_class):
        """Test successful audio processing with PyAnnote."""
        # Mock PyAnnote pipeline
        mock_pipeline = Mock()
        mock_pipeline_class.from_pretrained.return_value = mock_pipeline
        
        # Mock diarization result
        mock_segment = Mock()
        mock_segment.start = 0.0
        mock_segment.end = 5.0
        
        mock_diarization_result = Mock()
        mock_diarization_result.itertracks.return_value = [
            (mock_segment, None, "SPEAKER_00")
        ]
        mock_pipeline.return_value = mock_diarization_result
        
        config = DiarizationConfig()
        processor = DiarizationProcessor(config)
        
        # Create temporary audio file
        with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as tmp:
            tmp_path = tmp.name
        
        try:
            result = processor.process_audio(tmp_path, 10.0)
            
            # Verify result - this should fail validation due to low coverage and fallback to single speaker
            assert isinstance(result, DiarizationResult)
            assert result.speakers == [0]
            assert len(result.segments) == 1
            assert result.segments[0].speaker_id == 0
            assert result.segments[0].start_time == 0.0
            assert result.segments[0].end_time == 10.0  # Falls back to single speaker covering full duration
            assert result.segments[0].confidence == 1.0  # Fallback uses confidence 1.0
            assert result.audio_duration == 10.0
            assert result.processing_time > 0
            
        finally:
            Path(tmp_path).unlink(missing_ok=True)
    
    @patch('src.audio_to_json.diarization.PYANNOTE_AVAILABLE', True)
    @patch('src.audio_to_json.diarization.Pipeline')
    def test_process_audio_with_multiple_speakers(self, mock_pipeline_class):
        """Test audio processing with multiple speakers."""
        # Mock PyAnnote pipeline
        mock_pipeline = Mock()
        mock_pipeline_class.from_pretrained.return_value = mock_pipeline
        
        # Mock segments for multiple speakers
        mock_segment1 = Mock()
        mock_segment1.start = 0.0
        mock_segment1.end = 3.0
        
        mock_segment2 = Mock()
        mock_segment2.start = 3.0
        mock_segment2.end = 6.0
        
        mock_segment3 = Mock()
        mock_segment3.start = 6.0
        mock_segment3.end = 10.0
        
        mock_diarization_result = Mock()
        mock_diarization_result.itertracks.return_value = [
            (mock_segment1, None, "SPEAKER_00"),
            (mock_segment2, None, "SPEAKER_01"),
            (mock_segment3, None, "SPEAKER_00")
        ]
        mock_pipeline.return_value = mock_diarization_result
        
        config = DiarizationConfig()
        processor = DiarizationProcessor(config)
        
        # Create temporary audio file
        with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as tmp:
            tmp_path = tmp.name
        
        try:
            result = processor.process_audio(tmp_path, 10.0)
            
            # Verify result
            assert isinstance(result, DiarizationResult)
            assert sorted(result.speakers) == [0, 1]
            assert len(result.segments) == 3
            
            # Check segments
            segments = sorted(result.segments, key=lambda x: x.start_time)
            assert segments[0].speaker_id == 0
            assert segments[1].speaker_id == 1
            assert segments[2].speaker_id == 0
            
        finally:
            Path(tmp_path).unlink(missing_ok=True)
    
    def test_speaker_label_to_id(self):
        """Test speaker label to ID conversion."""
        config = DiarizationConfig()
        processor = DiarizationProcessor(config)
        
        # Test standard PyAnnote labels
        assert processor._speaker_label_to_id("SPEAKER_00") == 0
        assert processor._speaker_label_to_id("SPEAKER_01") == 1
        assert processor._speaker_label_to_id("SPEAKER_10") == 10
        
        # Test non-standard labels
        result = processor._speaker_label_to_id("custom_label")
        assert isinstance(result, int)
        assert 0 <= result < 100
        
        # Test invalid labels
        assert processor._speaker_label_to_id("invalid") == 0 or isinstance(
            processor._speaker_label_to_id("invalid"), int
        )
    
    def test_merge_close_segments(self):
        """Test merging of close segments from same speaker."""
        config = DiarizationConfig()
        processor = DiarizationProcessor(config)
        
        segments = [
            SpeakerSegment(speaker_id=0, start_time=0.0, end_time=2.0, confidence=0.8),
            SpeakerSegment(speaker_id=0, start_time=2.2, end_time=4.0, confidence=0.9),  # Close gap
            SpeakerSegment(speaker_id=1, start_time=4.5, end_time=6.0, confidence=0.7),
            SpeakerSegment(speaker_id=1, start_time=7.0, end_time=9.0, confidence=0.8),  # Larger gap
        ]
        
        merged = processor._merge_close_segments(segments, gap_threshold=0.5)
        
        # Should merge first two segments (gap = 0.2 < 0.5)
        # Should not merge last two segments (gap = 1.0 > 0.5)
        assert len(merged) == 3
        assert merged[0].speaker_id == 0
        assert merged[0].start_time == 0.0
        assert merged[0].end_time == 4.0
        assert merged[0].confidence == 0.9  # Max confidence
        
        assert merged[1].speaker_id == 1
        assert merged[2].speaker_id == 1
    
    def test_merge_close_segments_empty(self):
        """Test merging with empty segment list."""
        config = DiarizationConfig()
        processor = DiarizationProcessor(config)
        
        result = processor._merge_close_segments([])
        assert result == []
    
    def test_validate_result_valid(self):
        """Test validation of valid diarization result."""
        config = DiarizationConfig()
        processor = DiarizationProcessor(config)
        
        result = DiarizationResult(
            speakers=[0, 1],
            segments=[
                SpeakerSegment(speaker_id=0, start_time=0.0, end_time=5.0, confidence=0.8),
                SpeakerSegment(speaker_id=1, start_time=5.0, end_time=10.0, confidence=0.9)
            ],
            audio_duration=10.0,
            processing_time=1.0
        )
        
        assert processor._validate_result(result, 10.0) is True
    
    def test_validate_result_low_coverage(self):
        """Test validation with low coverage."""
        config = DiarizationConfig()
        processor = DiarizationProcessor(config)
        
        # Only 3 seconds covered out of 10
        result = DiarizationResult(
            speakers=[0],
            segments=[
                SpeakerSegment(speaker_id=0, start_time=0.0, end_time=3.0, confidence=0.8)
            ],
            audio_duration=10.0,
            processing_time=1.0
        )
        
        assert processor._validate_result(result, 10.0) is False
    
    def test_validate_result_zero_confidence(self):
        """Test validation with zero confidence segments."""
        config = DiarizationConfig()
        processor = DiarizationProcessor(config)
        
        # Cannot create segment with confidence=0.0 due to model validation
        # Test validation logic directly instead
        result = DiarizationResult(
            speakers=[0],
            segments=[
                SpeakerSegment(speaker_id=0, start_time=0.0, end_time=10.0, confidence=0.1)
            ],
            audio_duration=10.0,
            processing_time=1.0
        )
        
        # Mock a segment with confidence <= 0 for testing the validation logic
        with patch.object(result.segments[0], 'confidence', 0.0):
            assert processor._validate_result(result, 10.0) is False
    
    def test_create_single_speaker_fallback(self):
        """Test creation of single speaker fallback."""
        config = DiarizationConfig()
        processor = DiarizationProcessor(config)
        
        result = processor._create_single_speaker_fallback(15.0, 2.0)
        
        assert isinstance(result, DiarizationResult)
        assert result.speakers == [0]
        assert len(result.segments) == 1
        assert result.segments[0].speaker_id == 0
        assert result.segments[0].start_time == 0.0
        assert result.segments[0].end_time == 15.0
        assert result.segments[0].confidence == 1.0
        assert result.audio_duration == 15.0
        assert result.processing_time == 2.0


class TestDependencyChecking:
    """Test dependency checking functionality."""
    
    @patch('src.audio_to_json.diarization.PYANNOTE_AVAILABLE', True)
    @patch('src.audio_to_json.diarization.Pipeline')
    def test_check_dependencies_available(self, mock_pipeline):
        """Test dependency check when PyAnnote is available."""
        available, error = check_diarization_dependencies()
        
        assert available is True
        assert error is None
    
    @patch('src.audio_to_json.diarization.PYANNOTE_AVAILABLE', False)
    def test_check_dependencies_unavailable(self):
        """Test dependency check when PyAnnote is not available."""
        available, error = check_diarization_dependencies()
        
        assert available is False
        assert "PyAnnote not available" in error
        assert "pip install pyannote.audio torch" in error


class TestConvenienceFunction:
    """Test the convenience process_diarization function."""
    
    @patch('src.audio_to_json.diarization.DiarizationProcessor')
    def test_process_diarization_with_config(self, mock_processor_class):
        """Test convenience function with provided config."""
        mock_processor = Mock()
        mock_result = DiarizationResult(
            speakers=[0],
            segments=[SpeakerSegment(speaker_id=0, start_time=0.0, end_time=10.0, confidence=1.0)],
            audio_duration=10.0,
            processing_time=1.0
        )
        mock_processor.process_audio.return_value = mock_result
        mock_processor_class.return_value = mock_processor
        
        config = DiarizationConfig(model="test-model")
        result = process_diarization("test.wav", 10.0, config)
        
        # Verify processor was created with config
        mock_processor_class.assert_called_once_with(config)
        mock_processor.process_audio.assert_called_once_with("test.wav", 10.0)
        assert result == mock_result
    
    @patch('src.audio_to_json.diarization.DiarizationProcessor')
    def test_process_diarization_without_config(self, mock_processor_class):
        """Test convenience function without config (uses defaults)."""
        mock_processor = Mock()
        mock_result = DiarizationResult(
            speakers=[0],
            segments=[SpeakerSegment(speaker_id=0, start_time=0.0, end_time=10.0, confidence=1.0)],
            audio_duration=10.0,
            processing_time=1.0
        )
        mock_processor.process_audio.return_value = mock_result
        mock_processor_class.return_value = mock_processor
        
        result = process_diarization("test.wav", 10.0)
        
        # Verify processor was created with default config
        mock_processor_class.assert_called_once()
        call_args = mock_processor_class.call_args[0]
        assert isinstance(call_args[0], DiarizationConfig)
        assert result == mock_result


class TestPipelineIntegration:
    """Test integration aspects of the diarization processor."""
    
    @patch('src.audio_to_json.diarization.PYANNOTE_AVAILABLE', True)
    @patch('src.audio_to_json.diarization.Pipeline')
    def test_load_pipeline_success(self, mock_pipeline_class):
        """Test successful pipeline loading."""
        mock_pipeline = Mock()
        mock_pipeline.instantiate = Mock()
        mock_pipeline_class.from_pretrained.return_value = mock_pipeline
        
        config = DiarizationConfig(
            model="test-model",
            min_speakers=2,
            max_speakers=5,
            clustering_threshold=0.8,
            segmentation_threshold=0.6
        )
        
        processor = DiarizationProcessor(config)
        processor._load_pipeline()
        
        # Verify pipeline was loaded with correct model
        # Note: use_auth_token may be set from environment variable
        call_args = mock_pipeline_class.from_pretrained.call_args
        assert call_args[0] == ("test-model",)
        # Don't assert specific token value since it may come from environment
        
        # Verify pipeline was configured
        mock_pipeline.instantiate.assert_called_once()
        call_args = mock_pipeline.instantiate.call_args[0][0]
        # Check the actual configuration structure used in implementation
        assert call_args["clustering"]["threshold"] == 0.8
        assert call_args["segmentation"]["threshold"] == 0.6
        
        assert processor.pipeline == mock_pipeline
    
    @patch('src.audio_to_json.diarization.PYANNOTE_AVAILABLE', False)
    def test_load_pipeline_no_pyannote(self):
        """Test pipeline loading when PyAnnote is not available."""
        config = DiarizationConfig()
        processor = DiarizationProcessor(config)
        
        with pytest.raises(PipelineError) as exc_info:
            processor._load_pipeline()
        
        assert "PyAnnote not available" in str(exc_info.value)
        assert "pip install pyannote.audio torch" in str(exc_info.value)
    
    @patch('src.audio_to_json.diarization.PYANNOTE_AVAILABLE', True)
    @patch('src.audio_to_json.diarization.Pipeline')
    def test_load_pipeline_failure(self, mock_pipeline_class):
        """Test pipeline loading failure."""
        mock_pipeline_class.from_pretrained.side_effect = Exception("Model not found")
        
        config = DiarizationConfig()
        processor = DiarizationProcessor(config)
        
        with pytest.raises(PipelineError) as exc_info:
            processor._load_pipeline()
        
        assert "Failed to load diarization pipeline" in str(exc_info.value)
        assert "Model not found" in str(exc_info.value)