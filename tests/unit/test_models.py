"""
Unit tests for data models.

Tests Entity, AudioMetadata, SpeakerInfo, and WordDatabase models.
Focuses on validation, edge cases, and data integrity.
"""
import pytest
from datetime import datetime

from src.shared.models import Entity, AudioMetadata, SpeakerInfo, WordDatabase, SpeakerSegment, DiarizationResult
from src.shared.exceptions import PipelineError

pytestmark = [
    pytest.mark.unit,
    pytest.mark.quick
]

class TestEntity:
    """Test Entity model validation and methods."""
    
    def test_valid_entity_creation(self):
        """Test creating valid Entity objects."""
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
            phonetic="ˈoʊlə",
            quality_score=0.8,
            speaker_id=0,
            recording_id="test_recording",
            recording_path="/path/to/audio.wav",
            processed=False,
            clip_path=None,
            selection_reason=None,
            created_at=datetime.now().isoformat()
        )
        
        assert entity.entity_id == "word_001"
        assert entity.text == "hola"
        assert entity.duration == 0.5
    
    def test_time_validation(self):
        """Test start_time < end_time validation."""
        # Valid timing
        Entity(
            entity_id="word_001", entity_type="word", text="test",
            start_time=1.0, end_time=2.0, duration=1.0,
            confidence=0.9, probability=0.9, syllables=["test"],
            syllable_count=1, quality_score=0.8, speaker_id=0,
            recording_id="test", recording_path="test.wav", processed=False,
            created_at=datetime.now().isoformat()
        )
        
        # Invalid timing - start >= end
        with pytest.raises(ValueError, match="end_time must be greater than start_time"):
            Entity(
                entity_id="word_001", entity_type="word", text="test",
                start_time=2.0, end_time=1.0, duration=1.0,
                confidence=0.9, probability=0.9, syllables=["test"],
                syllable_count=1, quality_score=0.8, speaker_id=0,
                recording_id="test", recording_path="test.wav", processed=False,
                created_at=datetime.now().isoformat()
            )
        
        # Edge case - equal times
        with pytest.raises(ValueError, match="end_time must be greater than start_time"):
            Entity(
                entity_id="word_001", entity_type="word", text="test",
                start_time=1.0, end_time=1.0, duration=0.0,
                confidence=0.9, probability=0.9, syllables=["test"],
                syllable_count=1, quality_score=0.8, speaker_id=0,
                recording_id="test", recording_path="test.wav", processed=False,
                created_at=datetime.now().isoformat()
            )
    
    def test_confidence_validation(self):
        """Test confidence score range validation."""
        # Valid confidence values
        for conf in [0.0, 0.5, 1.0]:
            Entity(
                entity_id="word_001", entity_type="word", text="test",
                start_time=1.0, end_time=2.0, duration=1.0,
                confidence=conf, probability=conf, syllables=["test"],
                syllable_count=1, quality_score=0.8, speaker_id=0,
                recording_id="test", recording_path="test.wav", processed=False,
                created_at=datetime.now().isoformat()
            )
        
        # Invalid confidence values
        for conf in [-0.1, 1.1]:
            with pytest.raises(ValueError):
                Entity(
                    entity_id="word_001", entity_type="word", text="test",
                    start_time=1.0, end_time=2.0, duration=1.0,
                    confidence=conf, probability=0.9, syllables=["test"],
                    syllable_count=1, quality_score=0.8, speaker_id=0,
                    recording_id="test", recording_path="test.wav", processed=False,
                    created_at=datetime.now().isoformat()
                )
    
    def test_quality_score_validation(self):
        """Test quality score range validation."""
        # Valid quality scores
        for score in [0.0, 0.5, 1.0]:
            Entity(
                entity_id="word_001", entity_type="word", text="test",
                start_time=1.0, end_time=2.0, duration=1.0,
                confidence=0.9, probability=0.9, syllables=["test"],
                syllable_count=1, quality_score=score, speaker_id=0,
                recording_id="test", recording_path="test.wav", processed=False,
                created_at=datetime.now().isoformat()
            )
        
        # Invalid quality scores
        for score in [-0.1, 1.1]:
            with pytest.raises(ValueError):
                Entity(
                    entity_id="word_001", entity_type="word", text="test",
                    start_time=1.0, end_time=2.0, duration=1.0,
                    confidence=0.9, probability=0.9, syllables=["test"],
                    syllable_count=1, quality_score=score, speaker_id=0,
                    recording_id="test", recording_path="test.wav", processed=False,
                    created_at=datetime.now().isoformat()
                )
    
    def test_syllable_count_consistency(self):
        """Test syllable_count matches length of syllables list."""
        # Consistent syllable data
        Entity(
            entity_id="word_001", entity_type="word", text="hola",
            start_time=1.0, end_time=2.0, duration=1.0,
            confidence=0.9, probability=0.9, syllables=["ho", "la"],
            syllable_count=2, quality_score=0.8, speaker_id=0,
            recording_id="test", recording_path="test.wav", processed=False,
            created_at=datetime.now().isoformat()
        )
        
        # Inconsistent syllable count
        with pytest.raises(ValueError, match="syllable_count must match length of syllables"):
            Entity(
                entity_id="word_001", entity_type="word", text="hola",
                start_time=1.0, end_time=2.0, duration=1.0,
                confidence=0.9, probability=0.9, syllables=["ho", "la"],
                syllable_count=3, quality_score=0.8, speaker_id=0,
                recording_id="test", recording_path="test.wav", processed=False,
                created_at=datetime.now().isoformat()
            )
    
    def test_entity_type_validation(self):
        """Test entity_type validation."""
        # Valid entity types
        for entity_type in ["word", "phrase", "sentence"]:
            Entity(
                entity_id="test_001", entity_type=entity_type, text="test",
                start_time=1.0, end_time=2.0, duration=1.0,
                confidence=0.9, probability=0.9, syllables=["test"],
                syllable_count=1, quality_score=0.8, speaker_id=0,
                recording_id="test", recording_path="test.wav", processed=False,
                created_at=datetime.now().isoformat()
            )
        
        # Invalid entity type
        with pytest.raises(ValueError):
            Entity(
                entity_id="test_001", entity_type="invalid", text="test",
                start_time=1.0, end_time=2.0, duration=1.0,
                confidence=0.9, probability=0.9, syllables=["test"],
                syllable_count=1, quality_score=0.8, speaker_id=0,
                recording_id="test", recording_path="test.wav", processed=False,
                created_at=datetime.now().isoformat()
            )


class TestSpeakerInfo:
    """Test SpeakerInfo model validation."""
    
    def test_valid_speaker_info(self):
        """Test creating valid SpeakerInfo objects."""
        speaker = SpeakerInfo(
            name="María García",
            gender="F",
            region="Colombia"
        )
        
        assert speaker.name == "María García"
        assert speaker.gender == "F"
        assert speaker.region == "Colombia"
    
    def test_gender_validation(self):
        """Test gender field validation."""
        # Valid genders
        for gender in ["M", "F", "Unknown"]:
            SpeakerInfo(name="Test Speaker", gender=gender)
        
        # Invalid gender
        with pytest.raises(ValueError):
            SpeakerInfo(name="Test Speaker", gender="Male")  # Should be "M"
    
    def test_default_values(self):
        """Test default values for optional fields."""
        speaker = SpeakerInfo(name="Test Speaker")
        assert speaker.gender == "Unknown"
        assert speaker.region == "Unknown"


class TestAudioMetadata:
    """Test AudioMetadata model validation."""
    
    def test_valid_metadata(self):
        """Test creating valid AudioMetadata objects."""
        metadata = AudioMetadata(
            path="/path/to/audio.wav",
            duration=120.5,
            sample_rate=16000,
            channels=1,
            format="wav",
            size_bytes=1024000
        )
        
        assert metadata.duration == 120.5
        assert metadata.sample_rate == 16000
        assert metadata.channels == 1
    
    def test_sample_rate_validation(self):
        """Test sample rate validation."""
        # Valid sample rate
        AudioMetadata(
            path="test.wav", duration=10.0, sample_rate=16000,
            channels=1, format="wav", size_bytes=1000
        )
        
        # Invalid sample rate
        with pytest.raises(ValueError):
            AudioMetadata(
                path="test.wav", duration=10.0, sample_rate=0,
                channels=1, format="wav", size_bytes=1000
            )
    
    def test_duration_validation(self):
        """Test duration validation."""
        # Valid duration
        AudioMetadata(
            path="test.wav", duration=0.1, sample_rate=16000,
            channels=1, format="wav", size_bytes=1000
        )
        
        # Invalid duration
        with pytest.raises(ValueError):
            AudioMetadata(
                path="test.wav", duration=-1.0, sample_rate=16000,
                channels=1, format="wav", size_bytes=1000
            )


class TestWordDatabase:
    """Test WordDatabase model and methods."""
    
    def test_empty_database(self):
        """Test creating empty database."""
        db = WordDatabase(
            metadata={"version": "1.0", "created_at": "2025-01-01T00:00:00Z"},
            speaker_map={},
            entities=[]
        )
        assert len(db.entities) == 0
        assert db.metadata is not None
        assert len(db.speaker_map) == 0
    
    def test_add_entity(self):
        """Test adding entities to database."""
        db = WordDatabase(
            metadata={"version": "1.0", "created_at": "2025-01-01T00:00:00Z"},
            speaker_map={},
            entities=[]
        )
        
        entity = Entity(
            entity_id="word_001", entity_type="word", text="test",
            start_time=1.0, end_time=2.0, duration=1.0,
            confidence=0.9, probability=0.9, syllables=["test"],
            syllable_count=1, quality_score=0.8, speaker_id=0,
            recording_id="test", recording_path="test.wav", processed=False,
            created_at=datetime.now().isoformat()
        )
        
        db.entities.append(entity)
        assert len(db.entities) == 1
        assert db.entities[0].entity_id == "word_001"
    
    def test_get_entities_by_type(self):
        """Test filtering entities by type."""
        db = WordDatabase(
            metadata={"version": "1.0", "created_at": "2025-01-01T00:00:00Z"},
            speaker_map={},
            entities=[]
        )
        
        # Add different entity types
        word_entity = Entity(
            entity_id="word_001", entity_type="word", text="test",
            start_time=1.0, end_time=2.0, duration=1.0,
            confidence=0.9, probability=0.9, syllables=["test"],
            syllable_count=1, quality_score=0.8, speaker_id=0,
            recording_id="test", recording_path="test.wav", processed=False,
            created_at=datetime.now().isoformat()
        )
        
        phrase_entity = Entity(
            entity_id="phrase_001", entity_type="phrase", text="test phrase",
            start_time=1.0, end_time=3.0, duration=2.0,
            confidence=0.9, probability=0.9, syllables=["test", "phrase"],
            syllable_count=2, quality_score=0.8, speaker_id=0,
            recording_id="test", recording_path="test.wav", processed=False,
            created_at=datetime.now().isoformat()
        )
        
        db.entities.extend([word_entity, phrase_entity])
        
        # Filter by type
        words = db.get_entities_by_type("word")
        phrases = db.get_entities_by_type("phrase")
        
        assert len(words) == 1
        assert len(phrases) == 1
        assert words[0].entity_type == "word"
        assert phrases[0].entity_type == "phrase"
    
    def test_get_entities_by_speaker(self):
        """Test filtering entities by speaker."""
        db = WordDatabase(
            metadata={"version": "1.0", "created_at": "2025-01-01T00:00:00Z"},
            speaker_map={},
            entities=[]
        )
        
        # Add entities with different speakers
        entity1 = Entity(
            entity_id="word_001", entity_type="word", text="test1",
            start_time=1.0, end_time=2.0, duration=1.0,
            confidence=0.9, probability=0.9, syllables=["test1"],
            syllable_count=1, quality_score=0.8, speaker_id=0,
            recording_id="test", recording_path="test.wav", processed=False,
            created_at=datetime.now().isoformat()
        )
        
        entity2 = Entity(
            entity_id="word_002", entity_type="word", text="test2",
            start_time=2.0, end_time=3.0, duration=1.0,
            confidence=0.9, probability=0.9, syllables=["test2"],
            syllable_count=1, quality_score=0.8, speaker_id=1,
            recording_id="test", recording_path="test.wav", processed=False,
            created_at=datetime.now().isoformat()
        )
        
        db.entities.extend([entity1, entity2])
        
        # Filter by speaker
        speaker0_entities = db.get_entities_by_speaker(0)
        speaker1_entities = db.get_entities_by_speaker(1)
        
        assert len(speaker0_entities) == 1
        assert len(speaker1_entities) == 1
        assert speaker0_entities[0].speaker_id == 0
        assert speaker1_entities[0].speaker_id == 1
    
    def test_get_entities_by_confidence(self):
        """Test filtering entities by confidence threshold."""
        db = WordDatabase(
            metadata={"version": "1.0", "created_at": "2025-01-01T00:00:00Z"},
            speaker_map={},
            entities=[]
        )
        
        # Add entities with different confidence levels
        high_conf_entity = Entity(
            entity_id="word_001", entity_type="word", text="high",
            start_time=1.0, end_time=2.0, duration=1.0,
            confidence=0.9, probability=0.9, syllables=["high"],
            syllable_count=1, quality_score=0.8, speaker_id=0,
            recording_id="test", recording_path="test.wav", processed=False,
            created_at=datetime.now().isoformat()
        )
        
        low_conf_entity = Entity(
            entity_id="word_002", entity_type="word", text="low",
            start_time=2.0, end_time=3.0, duration=1.0,
            confidence=0.3, probability=0.3, syllables=["low"],
            syllable_count=1, quality_score=0.3, speaker_id=0,
            recording_id="test", recording_path="test.wav", processed=False,
            created_at=datetime.now().isoformat()
        )
        
        db.entities.extend([high_conf_entity, low_conf_entity])
        
        # Filter by confidence
        high_confidence = db.get_entities_by_confidence(0.5)
        assert len(high_confidence) == 1
        assert high_confidence[0].confidence >= 0.5
        
        all_entities = db.get_entities_by_confidence(0.0)
        assert len(all_entities) == 2


class TestSpeakerSegment:
    """Test SpeakerSegment model validation."""
    
    def test_valid_speaker_segment(self):
        """Test creating valid SpeakerSegment objects."""
        segment = SpeakerSegment(
            speaker_id=0,
            start_time=1.0,
            end_time=2.5,
            confidence=0.85
        )
        
        assert segment.speaker_id == 0
        assert segment.start_time == 1.0
        assert segment.end_time == 2.5
        assert segment.confidence == 0.85
    
    def test_time_validation(self):
        """Test start_time < end_time validation."""
        # Valid timing
        SpeakerSegment(
            speaker_id=0,
            start_time=1.0,
            end_time=2.0,
            confidence=0.8
        )
        
        # Invalid timing - start >= end
        with pytest.raises(ValueError, match="end_time must be greater than start_time"):
            SpeakerSegment(
                speaker_id=0,
                start_time=2.0,
                end_time=1.0,
                confidence=0.8
            )
        
        # Edge case - equal times
        with pytest.raises(ValueError, match="end_time must be greater than start_time"):
            SpeakerSegment(
                speaker_id=0,
                start_time=1.0,
                end_time=1.0,
                confidence=0.8
            )
    
    def test_confidence_validation(self):
        """Test confidence score range validation."""
        # Valid confidence values (greater than 0, less than or equal to 1)
        for conf in [0.1, 0.5, 1.0]:
            SpeakerSegment(
                speaker_id=0,
                start_time=1.0,
                end_time=2.0,
                confidence=conf
            )
        
        # Invalid confidence values
        for conf in [0.0, -0.1, 1.1]:
            with pytest.raises(ValueError):
                SpeakerSegment(
                    speaker_id=0,
                    start_time=1.0,
                    end_time=2.0,
                    confidence=conf
                )
    
    def test_speaker_id_validation(self):
        """Test speaker_id validation (must be >= 0)."""
        # Valid speaker IDs
        for speaker_id in [0, 1, 5, 10]:
            SpeakerSegment(
                speaker_id=speaker_id,
                start_time=1.0,
                end_time=2.0,
                confidence=0.8
            )
        
        # Invalid speaker IDs
        with pytest.raises(ValueError):
            SpeakerSegment(
                speaker_id=-1,
                start_time=1.0,
                end_time=2.0,
                confidence=0.8
            )


class TestDiarizationResult:
    """Test DiarizationResult model validation."""
    
    def test_valid_diarization_result(self):
        """Test creating valid DiarizationResult objects."""
        segments = [
            SpeakerSegment(speaker_id=0, start_time=0.0, end_time=5.0, confidence=0.9),
            SpeakerSegment(speaker_id=1, start_time=5.0, end_time=10.0, confidence=0.85)
        ]
        
        result = DiarizationResult(
            speakers=[0, 1],
            segments=segments,
            audio_duration=10.0,
            processing_time=2.5
        )
        
        assert result.speakers == [0, 1]
        assert len(result.segments) == 2
        assert result.audio_duration == 10.0
        assert result.processing_time == 2.5
    
    def test_no_overlapping_segments_validation(self):
        """Test that overlapping segments are rejected."""
        # Non-overlapping segments (valid)
        segments = [
            SpeakerSegment(speaker_id=0, start_time=0.0, end_time=5.0, confidence=0.9),
            SpeakerSegment(speaker_id=1, start_time=5.0, end_time=10.0, confidence=0.85)
        ]
        
        DiarizationResult(
            speakers=[0, 1],
            segments=segments,
            audio_duration=10.0,
            processing_time=2.5
        )
        
        # Overlapping segments (invalid)
        overlapping_segments = [
            SpeakerSegment(speaker_id=0, start_time=0.0, end_time=5.5, confidence=0.9),
            SpeakerSegment(speaker_id=1, start_time=5.0, end_time=10.0, confidence=0.85)
        ]
        
        with pytest.raises(ValueError, match="Segments must not have significant overlap"):
            DiarizationResult(
                speakers=[0, 1],
                segments=overlapping_segments,
                audio_duration=10.0,
                processing_time=2.5
            )
    
    def test_unordered_segments_sorting(self):
        """Test that segments are sorted by start_time during validation."""
        # Segments in wrong order
        segments = [
            SpeakerSegment(speaker_id=1, start_time=5.0, end_time=10.0, confidence=0.85),
            SpeakerSegment(speaker_id=0, start_time=0.0, end_time=5.0, confidence=0.9)
        ]
        
        # Should work - validator sorts by start_time
        result = DiarizationResult(
            speakers=[0, 1],
            segments=segments,
            audio_duration=10.0,
            processing_time=2.5
        )
        
        # Original segments order preserved (validation doesn't modify input)
        assert result.segments[0].start_time == 5.0  # Original order
        assert result.segments[1].start_time == 0.0
    
    def test_empty_segments(self):
        """Test handling of empty segments list."""
        result = DiarizationResult(
            speakers=[],
            segments=[],
            audio_duration=10.0,
            processing_time=2.5
        )
        
        assert result.speakers == []
        assert result.segments == []
    
    def test_single_speaker(self):
        """Test single speaker scenario."""
        segments = [
            SpeakerSegment(speaker_id=0, start_time=0.0, end_time=10.0, confidence=0.9)
        ]
        
        result = DiarizationResult(
            speakers=[0],
            segments=segments,
            audio_duration=10.0,
            processing_time=2.5
        )
        
        assert result.speakers == [0]
        assert len(result.segments) == 1
        assert result.segments[0].speaker_id == 0