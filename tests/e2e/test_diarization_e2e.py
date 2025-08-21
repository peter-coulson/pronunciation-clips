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

# Skip diarization tests by default - requires HuggingFace authentication
DIARIZATION_TESTS_ENABLED = os.getenv("ENABLE_DIARIZATION_TESTS", "false").lower() == "true"
skip_diarization = pytest.mark.skipif(
    not DIARIZATION_TESTS_ENABLED,
    reason="Diarization tests disabled by default. Set ENABLE_DIARIZATION_TESTS=true to enable. See DIARIZATION_SETUP.md for details."
)


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
        config = load_config(str(config_path))
        # Ensure diarization is explicitly disabled
        assert not config.speakers.enable_diarization
        return config

    @skip_diarization
    def test_basic_diarization_detection_e2e(self, fixtures_path: Path, expected_segments: Dict[str, Any]):
        """
        Test: Multi-speaker audio → Diarization → Speaker segments detected
        
        Success Criteria:
        - Detect 2+ speakers in conversation
        - Speaker segments have valid timestamps (start < end)
        - Speaker IDs are integers (0, 1, 2...)
        - Segments cover full audio duration
        - No overlapping segments
        - Confidence scores > 0.0
        """
        # Arrange: Setup multi-speaker audio and diarization config
        config = self.load_config_with_diarization(fixtures_path)
        audio_path = fixtures_path / "spanish_complete_test.wav"
        expected = expected_segments["multi_speaker_conversation"]
        
        # Act: Run diarization on multi-speaker audio
        # NOTE: This will fail until diarization is implemented
        pipeline = AudioToJsonPipeline(config)
        diarization_result = pipeline.process_diarization(str(audio_path))
        
        # Assert: Validate all success criteria met
        assert len(diarization_result.speakers) >= 2, "Should detect 2+ speakers"
        assert len(diarization_result.speakers) == expected["expected_speakers"]
        
        # Validate segment structure
        segments = diarization_result.segments
        assert len(segments) >= 2, "Should have multiple segments"
        
        for segment in segments:
            # Valid timestamps
            assert segment.start_time < segment.end_time, "Start time must be before end time"
            assert segment.start_time >= 0.0, "Start time must be non-negative"
            
            # Valid speaker IDs (integers)
            assert isinstance(segment.speaker_id, int), "Speaker ID must be integer"
            assert segment.speaker_id >= 0, "Speaker ID must be non-negative"
            
            # Valid confidence scores
            assert segment.confidence > 0.0, "Confidence must be positive"
            assert segment.confidence <= 1.0, "Confidence must not exceed 1.0"
        
        # Check no overlapping segments
        sorted_segments = sorted(segments, key=lambda x: x.start_time)
        for i in range(len(sorted_segments) - 1):
            current_end = sorted_segments[i].end_time
            next_start = sorted_segments[i + 1].start_time
            assert current_end <= next_start, "Segments must not overlap"
        
        # Segments should cover full audio duration
        total_start = min(s.start_time for s in segments)
        total_end = max(s.end_time for s in segments)
        assert total_start == 0.0, "Coverage should start at beginning"
        assert total_end > 30.0, "Coverage should extend through audio"

    @skip_diarization
    def test_entity_assignment_integration_e2e(self, fixtures_path: Path, expected_distribution: Dict[str, Any]):
        """
        Test: Multi-speaker audio → Full pipeline → Entities assigned to speakers
        
        Success Criteria:
        - Entities assigned to detected speakers (not all speaker_id: 0)
        - Speaker distribution matches conversation pattern
        - All entities have valid integer speaker IDs
        - Speaker changes align with segment boundaries
        - Max speaker percentage < 80% (no single speaker dominance)
        """
        # Arrange: Setup inputs and expected outputs
        config = self.load_config_with_diarization(fixtures_path)
        audio_path = fixtures_path / "spanish_complete_test.wav"
        expected = expected_distribution["multi_speaker_conversation"]
        
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
        
        # Entities should be assigned to multiple speakers (not all speaker_id: 0)
        assert len(speaker_counts) > 1, "Entities should be assigned to multiple speakers"
        
        # Check speaker distribution balance
        total_entities = len(entities)
        max_speaker_count = max(speaker_counts.values())
        max_speaker_percentage = (max_speaker_count / total_entities) * 100
        
        assert max_speaker_percentage < 80.0, "No single speaker should dominate (>80%)"
        
        # Verify expected distribution pattern
        assert total_entities >= expected["total_entities"] * 0.8, "Should have reasonable entity count"
        assert len(speaker_counts) == len(expected["speaker_distribution"]), "Speaker count should match expected"

    @skip_diarization
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
        audio_path = fixtures_path / "spanish_complete_test.wav"
        
        # Act: Process audio and then apply speaker labeling
        # NOTE: This will fail until speaker labeling is implemented
        pipeline = AudioToJsonPipeline(config)
        entities = pipeline.process(str(audio_path))
        
        # Simulate speaker name assignment
        speaker_names = {0: "Speaker A", 1: "Speaker B"}
        labeled_result = pipeline.assign_speaker_names(entities, speaker_names)
        
        # Assert: Validate all success criteria met
        assert "entities" in labeled_result, "Should contain entities"
        assert "speaker_map" in labeled_result, "Should contain speaker map"
        
        # Check speaker map updated with names
        speaker_map = labeled_result["speaker_map"]
        for speaker_id, name in speaker_names.items():
            assert speaker_id in speaker_map, f"Speaker {speaker_id} should be in map"
            assert speaker_map[speaker_id]["name"] == name, f"Speaker {speaker_id} name should be '{name}'"
        
        # Check entity speaker_ids remain unchanged
        original_speaker_ids = [e.speaker_id for e in entities]
        labeled_entities = labeled_result["entities"]
        labeled_speaker_ids = [e.speaker_id for e in labeled_entities]
        assert original_speaker_ids == labeled_speaker_ids, "Entity speaker IDs should remain unchanged"

    @skip_diarization
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
        audio_path = fixtures_path / "spanish_30sec_16khz.wav"
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
        audio_path = fixtures_path / "spanish_30sec_44khz.wav"
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


class TestDiarizationErrorHandling:
    """Test error handling for diarization functionality."""
    
    @skip_diarization
    def test_missing_dependency_graceful_fallback(self):
        """Test graceful fallback when diarization dependencies are missing."""
        # NOTE: This will be implemented to test dependency handling
        pytest.skip("Dependency handling not yet implemented")
    
    @skip_diarization
    def test_audio_file_error_handling(self):
        """Test error handling for corrupted or invalid audio files."""
        # NOTE: This will be implemented to test audio error handling
        pytest.skip("Audio error handling not yet implemented")
    
    @skip_diarization
    def test_configuration_error_handling(self):
        """Test error handling for invalid diarization configuration."""
        # NOTE: This will be implemented to test config error handling
        pytest.skip("Configuration error handling not yet implemented")
    
    @skip_diarization
    def test_model_loading_failure_handling(self):
        """Test error handling for diarization model loading failures."""
        # NOTE: This will be implemented to test model loading error handling
        pytest.skip("Model loading error handling not yet implemented")


class TestDiarizationPerformance:
    """Test performance requirements for diarization functionality."""
    
    @skip_diarization
    def test_processing_speed_within_realtime(self):
        """Test processing speed within 2-4x realtime."""
        # NOTE: This will be implemented to test performance requirements
        pytest.skip("Performance testing not yet implemented")
    
    @skip_diarization
    def test_memory_usage_limits(self):
        """Test memory usage <2GB for 10min audio."""
        # NOTE: This will be implemented to test memory requirements
        pytest.skip("Memory testing not yet implemented")
    
    @skip_diarization
    def test_no_performance_regression_when_disabled(self):
        """Test no performance regression when diarization is disabled."""
        # NOTE: This will be implemented to test performance impact
        pytest.skip("Performance regression testing not yet implemented")