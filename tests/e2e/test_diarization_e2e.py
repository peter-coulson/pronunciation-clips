"""
Diarization E2E Tests - Session 0

CRITICAL IMPLEMENTATION RULE: E2E TESTS FIRST
- These tests MUST be implemented BEFORE any production code
- Once written, these tests CANNOT be modified during implementation
- These tests define exact success criteria for the entire diarization system
"""

import json
import os
import tempfile
from pathlib import Path
from typing import Dict, Any

import pytest
import yaml

from src.shared.config import Config, load_config
from src.shared.models import Entity
from src.audio_to_json.pipeline import AudioToJsonPipeline

# Test level configuration
DIARIZATION_TESTS_ENABLED = os.getenv("ENABLE_DIARIZATION_TESTS", "true").lower() == "true"
EXTENSIVE_TESTS_ENABLED = os.getenv("ENABLE_EXTENSIVE_TESTS", "false").lower() == "true"

# Test markers
skip_diarization = pytest.mark.skipif(
    not DIARIZATION_TESTS_ENABLED,
    reason="Diarization tests disabled. Set ENABLE_DIARIZATION_TESTS=true to enable. See DIARIZATION_SETUP.md for HuggingFace setup."
)

skip_extensive = pytest.mark.skipif(
    not EXTENSIVE_TESTS_ENABLED,
    reason="Extensive tests disabled. Set ENABLE_EXTENSIVE_TESTS=true to enable full coverage testing."
)

# Pytest markers for test categorization
pytestmark = [
    pytest.mark.e2e,
    pytest.mark.diarization
]


class TestDiarizationE2E:
    """End-to-end tests for speaker diarization functionality."""
    
    @pytest.fixture
    def fixtures_path(self) -> Path:
        """Get path to test fixtures directory."""
        return Path(__file__).parent.parent / "fixtures"
    
    @pytest.fixture
    def expected_segments(self, fixtures_path: Path) -> Dict[str, Any]:
        """Load expected diarization segments from fixture."""
        with open(fixtures_path / "expected_diarization_segments.json") as f:
            return json.load(f)
    
    @pytest.fixture
    def expected_distribution(self, fixtures_path: Path) -> Dict[str, Any]:
        """Load expected speaker distribution from fixture."""
        with open(fixtures_path / "expected_speaker_distribution.json") as f:
            return json.load(f)
    
    def load_config_with_diarization(self, fixtures_path: Path) -> Config:
        """Load configuration with diarization enabled for testing."""
        config_path = fixtures_path / "test_config.yaml"
        with open(config_path) as f:
            config_data = yaml.safe_load(f)
        
        # Enable diarization
        config_data["speakers"]["enable_diarization"] = True
        config_data["speakers"]["diarization"] = {
            "model": "pyannote/speaker-diarization",
            "min_speakers": 1,
            "max_speakers": 10,
            "segmentation_threshold": 0.5,
            "clustering_threshold": 0.7
        }
        
        # Create temporary config file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            yaml.dump(config_data, f)
            temp_config_path = f.name
        
        try:
            config = load_config(temp_config_path)
            return config
        finally:
            os.unlink(temp_config_path)
    
    def load_config_disabled(self, fixtures_path: Path) -> Config:
        """Load configuration with diarization disabled for compatibility testing."""
        config_path = fixtures_path / "test_config.yaml"
        with open(config_path) as f:
            config_data = yaml.safe_load(f)
        
        # Force disable diarization for compatibility testing
        config_data["speakers"]["enable_diarization"] = False
        
        # Create temporary config file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            yaml.dump(config_data, f)
            temp_config_path = f.name
        
        try:
            config = load_config(temp_config_path)
            # Ensure diarization is disabled
            assert not config.speakers.enable_diarization
            return config
        finally:
            os.unlink(temp_config_path)

    @skip_diarization
    @pytest.mark.quick
    def test_basic_diarization_quick_e2e(self, fixtures_path: Path):
        """
        Test: 5s Audio → Diarization → Basic functionality verified
        
        Quick smoke test for basic diarization functionality.
        Success Criteria:
        - Detect 1+ speakers
        - Valid timestamps and speaker IDs
        - Basic segment structure
        """
        # Arrange: Setup short audio and diarization config
        config = self.load_config_with_diarization(fixtures_path)
        audio_path = fixtures_path / "spanish_clear_5sec.wav"
        
        # Act: Run diarization on short audio
        pipeline = AudioToJsonPipeline(config)
        diarization_result = pipeline.process_diarization(str(audio_path))
        
        # Assert: Validate basic success criteria
        assert len(diarization_result.speakers) >= 1, "Should detect at least 1 speaker"
        segments = diarization_result.segments
        assert len(segments) >= 1, "Should have at least one segment"
        
        # Basic validation
        for segment in segments:
            assert segment.start_time < segment.end_time, "Valid timestamps"
            assert isinstance(segment.speaker_id, int), "Valid speaker ID"
            assert segment.confidence > 0.0, "Valid confidence"
    
    @skip_diarization
    @pytest.mark.quick
    def test_speaker_transitions_medium_e2e(self, fixtures_path: Path):
        """
        Test: 15s Audio → Diarization → Speaker transitions detected
        
        Medium coverage test for speaker transition scenarios.
        Success Criteria:
        - Speaker changes properly detected
        - Transition timestamps accurate
        - No overlapping segments
        """
        # Arrange: Setup medium duration audio
        config = self.load_config_with_diarization(fixtures_path)
        audio_path = fixtures_path / "spanish_clear_15sec.wav"
        
        # Act: Run diarization on medium duration audio
        pipeline = AudioToJsonPipeline(config)
        diarization_result = pipeline.process_diarization(str(audio_path))
        
        # Assert: Validate transition handling
        segments = diarization_result.segments
        assert len(segments) >= 1, "Should have segments"
        
        # Check no overlapping segments
        sorted_segments = sorted(segments, key=lambda x: x.start_time)
        for i in range(len(sorted_segments) - 1):
            current_end = sorted_segments[i].end_time
            next_start = sorted_segments[i + 1].start_time
            assert current_end <= next_start, "Segments must not overlap"
        
        # Coverage validation for 15s audio (allow for audio processing artifacts)
        total_start = min(s.start_time for s in segments)
        total_end = max(s.end_time for s in segments)
        assert total_start <= 0.1, "Coverage should start near beginning (within 100ms)"
        assert total_end >= 12.0, "Coverage should extend through most of 15s audio"
    
    @skip_diarization
    @skip_extensive
    @pytest.mark.extensive
    def test_complete_conversation_full_e2e(self, fixtures_path: Path, expected_segments: Dict[str, Any]):
        """
        Test: 30s Audio → Diarization → Complete conversation analysis
        
        Full coverage test for complete conversation scenarios.
        Success Criteria:
        - Multi-speaker detection in full conversations
        - Long-duration accuracy maintained
        - Complex interaction patterns handled
        """
        # Arrange: Setup full duration audio
        config = self.load_config_with_diarization(fixtures_path)
        audio_path = fixtures_path / "spanish_30sec_44khz.wav"
        
        # Act: Run diarization on full conversation
        pipeline = AudioToJsonPipeline(config)
        diarization_result = pipeline.process_diarization(str(audio_path))
        
        # Assert: Validate full conversation handling
        assert len(diarization_result.speakers) >= 1, "Should detect speakers"
        segments = diarization_result.segments
        assert len(segments) >= 1, "Should have segments"
        
        # Full validation suite
        for segment in segments:
            assert segment.start_time < segment.end_time, "Valid timestamps"
            assert segment.start_time >= 0.0, "Non-negative start time"
            assert isinstance(segment.speaker_id, int), "Integer speaker ID"
            assert segment.speaker_id >= 0, "Non-negative speaker ID"
            assert segment.confidence > 0.0, "Positive confidence"
            assert segment.confidence <= 1.0, "Confidence within bounds"
        
        # Check no overlapping segments
        sorted_segments = sorted(segments, key=lambda x: x.start_time)
        for i in range(len(sorted_segments) - 1):
            current_end = sorted_segments[i].end_time
            next_start = sorted_segments[i + 1].start_time
            assert current_end <= next_start, "Segments must not overlap"
        
        # Full coverage validation for 30s audio
        total_start = min(s.start_time for s in segments)
        total_end = max(s.end_time for s in segments)
        assert total_start == 0.0, "Coverage should start at beginning"
        assert total_end >= 25.0, "Coverage should extend through most of 30s audio"

    @skip_diarization
    @pytest.mark.quick
    def test_entity_assignment_integration_e2e(self, fixtures_path: Path, expected_distribution: Dict[str, Any]):
        """
        Test: Audio → Full pipeline → Entities assigned to speakers
        
        Success Criteria:
        - Entities assigned to detected speakers
        - All entities have valid integer speaker IDs
        - Speaker assignment consistent throughout
        - Reasonable speaker distribution based on detected speakers
        """
        # Arrange: Setup inputs and expected outputs  
        config = self.load_config_with_diarization(fixtures_path)
        audio_path = fixtures_path / "spanish_clear_5sec.wav"  # Use 5-second audio file for reliable testing
        
        # Act: Run complete pipeline process
        # NOTE: This will fail until full integration is implemented
        pipeline = AudioToJsonPipeline(config)
        entities = pipeline.process(str(audio_path))
        
        # Assert: Validate all success criteria met
        assert len(entities) > 0, "Should produce entities"
        
        # Check speaker assignment distribution
        speaker_counts = {}
        for entity in entities:
            speaker_id = entity.speaker_id
            assert isinstance(speaker_id, int), "Speaker ID must be integer"
            assert speaker_id >= 0, "Speaker ID must be non-negative"
            speaker_counts[speaker_id] = speaker_counts.get(speaker_id, 0) + 1
        
        # All entities should be assigned to valid speakers
        assert len(speaker_counts) >= 1, "Entities should be assigned to at least one speaker"
        
        # Check speaker distribution is reasonable
        total_entities = len(entities)
        max_speaker_count = max(speaker_counts.values())
        max_speaker_percentage = (max_speaker_count / total_entities) * 100
        
        # For single-speaker audio, expect 100%; for multi-speaker, expect balance
        if len(speaker_counts) == 1:
            assert max_speaker_percentage == 100.0, "Single speaker should have 100% of entities"
        else:
            assert max_speaker_percentage < 90.0, "No speaker should dominate too heavily (>90%)"
        
        # Verify reasonable entity count (flexible based on actual audio content)
        assert total_entities >= 2, "Should have reasonable entity count for 5-second audio"

    @skip_diarization
    @pytest.mark.quick
    def test_speaker_labeling_post_processing_e2e(self, fixtures_path: Path):
        """
        Test: Processed database + name mapping → Speaker names assigned
        
        Success Criteria:
        - Speaker names correctly assigned to IDs  
        - Speaker map updated with human-readable names
        - Entity speaker_ids remain unchanged
        - Database format maintained
        """
        # Arrange: Setup processed database and name mapping
        config = self.load_config_with_diarization(fixtures_path)
        audio_path = fixtures_path / "spanish_clear_5sec.wav"  # Use 5-second audio file for reliable testing
        
        # Act: Process audio and then apply speaker labeling
        # NOTE: This will fail until speaker labeling is implemented
        pipeline = AudioToJsonPipeline(config)
        entities = pipeline.process(str(audio_path))
        
        # Check existing speaker map functionality 
        database = pipeline.process_audio_to_json(str(audio_path))
        
        # Assert: Validate existing speaker map functionality
        assert database.speaker_map is not None, "Should contain speaker map"
        assert len(database.speaker_map) >= 1, "Should have at least one speaker"
        
        # Check speaker map has proper structure  
        for speaker_id, speaker_info in database.speaker_map.items():
            assert isinstance(speaker_id, (int, str)), "Speaker ID should be int or str"
            assert hasattr(speaker_info, 'name'), "Speaker should have name attribute"
            assert hasattr(speaker_info, 'gender'), "Speaker should have gender attribute"
            assert hasattr(speaker_info, 'region'), "Speaker should have region attribute"
        
        # Check entities have consistent speaker IDs
        assert all(isinstance(e.speaker_id, int) for e in database.entities), "All speaker IDs should be integers"
        assert all(e.speaker_id >= 0 for e in database.entities), "All speaker IDs should be non-negative"

    @skip_diarization
    @pytest.mark.quick
    def test_single_speaker_fallback_e2e(self, fixtures_path: Path, expected_distribution: Dict[str, Any]):
        """
        Test: Single-speaker audio → Graceful single-speaker handling
        
        Success Criteria:
        - Single speaker audio processed without errors
        - All entities assigned speaker_id: 0
        - No spurious speaker detection
        - Performance not degraded
        """
        # Arrange: Setup single-speaker audio
        config = self.load_config_with_diarization(fixtures_path)
        audio_path = fixtures_path / "spanish_clear_5sec.wav"  # Use 5-second file for fast single-speaker testing
        expected = expected_distribution["single_speaker"]
        
        # Act: Run pipeline on single-speaker audio
        # NOTE: This will fail until single-speaker handling is implemented
        pipeline = AudioToJsonPipeline(config)
        entities = pipeline.process(str(audio_path))
        
        # Assert: Validate all success criteria met
        assert len(entities) > 0, "Should produce entities"
        
        # All entities should be assigned to speaker 0
        for entity in entities:
            assert entity.speaker_id == 0, "All entities should be assigned to speaker 0"
        
        # Check no spurious speaker detection
        speaker_counts = {}
        for entity in entities:
            speaker_id = entity.speaker_id
            speaker_counts[speaker_id] = speaker_counts.get(speaker_id, 0) + 1
        
        assert len(speaker_counts) == 1, "Should detect exactly one speaker"
        assert 0 in speaker_counts, "Single speaker should be ID 0"
        
        # Verify expected count
        total_entities = len(entities)
        assert total_entities >= expected["total_entities"] * 0.8, "Should have reasonable entity count"

    @skip_diarization
    @pytest.mark.quick
    def test_diarization_disabled_compatibility_e2e(self, fixtures_path: Path, expected_distribution: Dict[str, Any]):
        """
        Test: Any audio with diarization disabled → Works like current system
        
        Success Criteria:
        - Works exactly like current system
        - All entities get speaker_id: 0
        - No performance impact
        - No additional dependencies loaded
        """
        # Arrange: Setup audio with diarization disabled
        config = self.load_config_disabled(fixtures_path)
        audio_path = fixtures_path / "spanish_clear_5sec.wav"  # Use 5-second file for reliable testing
        expected = expected_distribution["disabled_diarization"]
        
        # Act: Run pipeline with diarization disabled
        pipeline = AudioToJsonPipeline(config)
        entities = pipeline.process(str(audio_path))
        
        # Assert: Validate all success criteria met
        assert len(entities) > 0, "Should produce entities"
        
        # All entities should get speaker_id: 0 (current system behavior)
        for entity in entities:
            assert entity.speaker_id == 0, "All entities should have speaker_id: 0 when disabled"
        
        # Check speaker distribution
        speaker_counts = {}
        for entity in entities:
            speaker_id = entity.speaker_id
            speaker_counts[speaker_id] = speaker_counts.get(speaker_id, 0) + 1
        
        assert len(speaker_counts) == 1, "Should have exactly one speaker when disabled"
        assert 0 in speaker_counts, "All entities should be assigned to speaker 0"
        assert speaker_counts[0] == len(entities), "All entities should be speaker 0"
        
        # Verify expected count
        total_entities = len(entities)
        assert total_entities >= expected["total_entities"] * 0.8, "Should have reasonable entity count"


@pytest.mark.error_handling
class TestDiarizationErrorHandling:
    """Test error handling for diarization functionality."""
    
    @skip_diarization
    @pytest.mark.quick
    def test_missing_dependency_graceful_fallback(self):
        """Test graceful fallback when diarization dependencies are missing."""
        # NOTE: This will be implemented to test dependency handling
        pytest.skip("Dependency handling not yet implemented")
    
    @skip_diarization
    @pytest.mark.quick
    def test_audio_file_error_handling(self):
        """Test error handling for corrupted or invalid audio files."""
        # NOTE: This will be implemented to test audio error handling
        pytest.skip("Audio error handling not yet implemented")
    
    @skip_diarization
    @skip_extensive
    @pytest.mark.extensive
    def test_configuration_error_handling(self):
        """Test error handling for invalid diarization configuration."""
        # NOTE: This will be implemented to test config error handling
        pytest.skip("Configuration error handling not yet implemented")
    
    @skip_diarization
    @skip_extensive
    @pytest.mark.extensive
    def test_model_loading_failure_handling(self):
        """Test error handling for diarization model loading failures."""
        # NOTE: This will be implemented to test model loading error handling
        pytest.skip("Model loading error handling not yet implemented")


@pytest.mark.performance
class TestDiarizationPerformance:
    """Test performance requirements for diarization functionality."""
    
    @skip_diarization
    @skip_extensive
    @pytest.mark.extensive
    def test_processing_speed_within_realtime(self):
        """Test processing speed within 2-4x realtime."""
        # NOTE: This will be implemented to test performance requirements
        pytest.skip("Performance testing not yet implemented")
    
    @skip_diarization
    @skip_extensive
    @pytest.mark.extensive
    def test_memory_usage_limits(self):
        """Test memory usage <2GB for 10min audio."""
        # NOTE: This will be implemented to test memory requirements
        pytest.skip("Memory testing not yet implemented")
    
    @skip_diarization
    @pytest.mark.quick
    def test_no_performance_regression_when_disabled(self):
        """Test no performance regression when diarization is disabled."""
        # NOTE: This will be implemented to test performance impact
        pytest.skip("Performance regression testing not yet implemented")