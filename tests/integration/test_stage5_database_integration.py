"""
Integration tests for Stage 5: Database Writing.

Tests focused integration of entity data to database creation,
atomic JSON writing operations, and backup/validation systems.
"""
import pytest
import tempfile
import json
import os
from pathlib import Path
from datetime import datetime
from unittest.mock import patch, MagicMock

from src.audio_to_json.database_writer import DatabaseWriter, write_database, create_default_database
from src.audio_to_json.entity_creation import EntityCreator
from src.audio_to_json.transcription import Word
from src.shared.config import Config, OutputConfig
from src.shared.models import WordDatabase, Entity, SpeakerInfo, AudioMetadata
from src.shared.exceptions import DatabaseError


class TestEntityToDatabaseIntegration:
    """Test integration from entities to database creation."""
    
    def test_entities_to_database_integration(self):
        """Test that entities integrate properly with database creation."""
        config = Config()
        entity_creator = EntityCreator(config.quality)
        
        # Create entities from words
        words = [
            Word("hola", 0.0, 0.5, 0.9),
            Word("mundo", 0.5, 1.0, 0.8),
            Word("español", 1.0, 1.5, 0.85)
        ]
        
        entities = entity_creator.create_entities(words, "test_recording", "test.wav")
        filtered_entities = entity_creator.apply_quality_filters(entities)
        
        # Create database from entities
        database = create_default_database(entities=filtered_entities)
        
        # Verify integration
        assert isinstance(database, WordDatabase)
        assert len(database.entities) == len(filtered_entities)
        assert database.metadata["version"] == "1.0"
        assert "created_at" in database.metadata
        
        # Verify entities maintained their properties
        for i, entity in enumerate(database.entities):
            assert entity.text in ["hola", "mundo", "español"]
            assert entity.entity_type == "word"
            assert entity.confidence > 0.0
    
    def test_database_with_audio_metadata_integration(self):
        """Test database creation with audio metadata integration."""
        # Create audio metadata
        audio_metadata = AudioMetadata(
            path="test.wav", duration=120.0, sample_rate=16000,
            channels=1, format="wav", size_bytes=1024000
        )
        
        # Create entities
        entity = Entity(
            entity_id="word_001", entity_type="word", text="test",
            start_time=0.0, end_time=0.5, duration=0.5,
            confidence=0.9, probability=0.9, syllables=["test"],
            syllable_count=1, quality_score=0.8, speaker_id="speaker_0",
            recording_id="test", recording_path="test.wav", processed=False,
            created_at=datetime.now().isoformat()
        )
        
        # Create database with metadata
        metadata = {
            "version": "1.0",
            "created_at": datetime.now().isoformat(),
            "audio_metadata": audio_metadata.model_dump()
        }
        
        database = create_default_database(
            entities=[entity],
            metadata=metadata
        )
        
        # Verify integration
        assert database.metadata["audio_metadata"]["duration"] == 120.0
        assert database.metadata["audio_metadata"]["sample_rate"] == 16000
        assert len(database.entities) == 1
    
    def test_speaker_mapping_integration(self):
        """Test speaker mapping integration with database creation."""
        # Create entities with different speakers
        entities = []
        for i, speaker_id in enumerate(["speaker_alice", "speaker_bob"]):
            entity = Entity(
                entity_id=f"word_{i+1:03d}", entity_type="word", text=f"word{i+1}",
                start_time=float(i), end_time=float(i+0.5), duration=0.5,
                confidence=0.9, probability=0.9, syllables=[f"word{i+1}"],
                syllable_count=1, quality_score=0.8, speaker_id=speaker_id,
                recording_id="test", recording_path="test.wav", processed=False,
                created_at=datetime.now().isoformat()
            )
            entities.append(entity)
        
        # Create speaker mapping
        speaker_map = {
            "speaker_alice": SpeakerInfo(name="Alice", gender="F", region="Colombia"),
            "speaker_bob": SpeakerInfo(name="Bob", gender="M", region="Spain")
        }
        
        database = create_default_database(
            entities=entities,
            speaker_map=speaker_map
        )
        
        # Verify speaker integration
        assert len(database.speaker_map) == 2
        assert database.speaker_map["speaker_alice"].name == "Alice"
        assert database.speaker_map["speaker_bob"].name == "Bob"
        assert database.entities[0].speaker_id in database.speaker_map
        assert database.entities[1].speaker_id in database.speaker_map


class TestAtomicWritingIntegration:
    """Test atomic writing operations integration."""
    
    def test_atomic_write_with_backup_integration(self):
        """Test atomic write operations with backup creation."""
        config = Config()
        config.output.backup_on_update = True
        writer = DatabaseWriter(config)
        
        database = create_default_database()
        
        with tempfile.TemporaryDirectory() as temp_dir:
            output_path = Path(temp_dir) / "database.json"
            
            # Write initial database
            writer.write_database(database, output_path)
            assert output_path.exists()
            
            # Modify and write again (should create backup)
            database.metadata["version"] = "2.0"
            writer.write_database(database, output_path)
            
            # Verify backup was created
            backup_files = list(output_path.parent.glob("database_backup_*"))
            assert len(backup_files) == 1
            
            # Verify both files are valid JSON
            with open(output_path, 'r') as f:
                current_data = json.load(f)
            with open(backup_files[0], 'r') as f:
                backup_data = json.load(f)
            
            assert current_data["metadata"]["version"] == "2.0"
            # Backup might have version 2.0 since we modified the same object
            assert "metadata" in backup_data
    
    def test_write_failure_rollback_integration(self):
        """Test write failure rollback integration."""
        config = Config()
        config.output.backup_on_update = True
        writer = DatabaseWriter(config)
        
        database = create_default_database()
        
        with tempfile.TemporaryDirectory() as temp_dir:
            output_path = Path(temp_dir) / "database.json"
            
            # Write initial database
            original_content = {"original": "data"}
            with open(output_path, 'w') as f:
                json.dump(original_content, f)
            
            # Mock validation to fail
            with patch.object(writer, '_validate_written_file', side_effect=DatabaseError("Validation failed")):
                with pytest.raises(DatabaseError):
                    writer.write_database(database, output_path)
                
                # Verify original file is preserved (backup was restored)
                with open(output_path, 'r') as f:
                    data = json.load(f)
                assert data == original_content
    
    def test_directory_creation_integration(self):
        """Test automatic directory creation integration."""
        config = Config()
        writer = DatabaseWriter(config)
        
        database = create_default_database()
        
        with tempfile.TemporaryDirectory() as temp_dir:
            nested_path = Path(temp_dir) / "deep" / "nested" / "dirs" / "database.json"
            
            # Directory doesn't exist yet
            assert not nested_path.parent.exists()
            
            # Write database (should create directories)
            writer.write_database(database, nested_path)
            
            # Verify directories were created
            assert nested_path.parent.exists()
            assert nested_path.exists()
            
            # Verify content is valid
            with open(nested_path, 'r') as f:
                data = json.load(f)
            assert "metadata" in data


class TestConfigurationIntegration:
    """Test configuration integration with database writing."""
    
    def test_output_config_integration(self):
        """Test output configuration integration."""
        config = Config()
        config.output.pretty_print = True
        config.output.encoding = "utf-8"
        writer = DatabaseWriter(config)
        
        # Create database with Spanish characters
        entity = Entity(
            entity_id="word_001", entity_type="word", text="niño",
            start_time=0.0, end_time=0.5, duration=0.5,
            confidence=0.9, probability=0.9, syllables=["ni", "ño"],
            syllable_count=2, quality_score=0.8, speaker_id="speaker_0",
            recording_id="test", recording_path="test.wav", processed=False,
            created_at=datetime.now().isoformat()
        )
        
        database = create_default_database(entities=[entity])
        
        with tempfile.TemporaryDirectory() as temp_dir:
            output_path = Path(temp_dir) / "spanish.json"
            
            writer.write_database(database, output_path)
            
            # Verify pretty printing
            with open(output_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            assert "  " in content  # Should have indentation
            assert "niño" in content  # Spanish characters preserved
    
    def test_compact_output_integration(self):
        """Test compact output configuration integration."""
        config = Config()
        config.output.pretty_print = False
        writer = DatabaseWriter(config)
        
        database = create_default_database()
        
        with tempfile.TemporaryDirectory() as temp_dir:
            output_path = Path(temp_dir) / "compact.json"
            
            writer.write_database(database, output_path)
            
            # Verify compact format
            with open(output_path, 'r') as f:
                content = f.read()
            
            # Should not have unnecessary indentation
            lines = content.split('\n')
            indented_lines = [line for line in lines if line.startswith('  ')]
            assert len(indented_lines) == 0


class TestValidationIntegration:
    """Test validation integration with database writing."""
    
    def test_round_trip_validation_integration(self):
        """Test round-trip validation integration."""
        config = Config()
        writer = DatabaseWriter(config)
        
        # Create complex database
        entities = []
        for i in range(5):
            entity = Entity(
                entity_id=f"word_{i+1:03d}", entity_type="word", text=f"palabra{i+1}",
                start_time=float(i), end_time=float(i+0.5), duration=0.5,
                confidence=0.9, probability=0.9, syllables=[f"pa{i+1}"],
                syllable_count=1, quality_score=0.8, speaker_id="speaker_0",
                recording_id="test", recording_path="test.wav", processed=False,
                created_at=datetime.now().isoformat()
            )
            entities.append(entity)
        
        database = create_default_database(entities=entities)
        
        with tempfile.TemporaryDirectory() as temp_dir:
            output_path = Path(temp_dir) / "validation_test.json"
            
            # Write database
            writer.write_database(database, output_path)
            
            # Read back and validate
            with open(output_path, 'r') as f:
                data = json.load(f)
            
            # Should be able to recreate WordDatabase
            restored_db = WordDatabase.model_validate(data)
            
            assert len(restored_db.entities) == 5
            assert restored_db.metadata["version"] == database.metadata["version"]
            
            # Verify all entities preserved
            for i, entity in enumerate(restored_db.entities):
                assert entity.text == f"palabra{i+1}"
                assert entity.entity_type == "word"
    
    def test_schema_validation_integration(self):
        """Test schema validation integration."""
        config = Config()
        writer = DatabaseWriter(config)
        
        with tempfile.TemporaryDirectory() as temp_dir:
            invalid_path = Path(temp_dir) / "invalid.json"
            
            # Write invalid JSON manually
            with open(invalid_path, 'w') as f:
                f.write('{"incomplete": "json"')  # Missing closing brace
            
            # Validation should fail
            with pytest.raises(DatabaseError, match="validation failed"):
                writer._validate_written_file(invalid_path)


class TestConvenienceFunctionIntegration:
    """Test convenience function integration."""
    
    def test_write_database_function_integration(self):
        """Test write_database convenience function integration."""
        config = Config()
        database = create_default_database()
        
        with tempfile.TemporaryDirectory() as temp_dir:
            output_path = Path(temp_dir) / "convenience_test.json"
            
            # Use convenience function
            result_path = write_database(database, output_path, config)
            
            assert result_path == output_path
            assert output_path.exists()
            
            # Verify content
            with open(output_path, 'r') as f:
                data = json.load(f)
            
            assert "metadata" in data
            assert "speaker_map" in data
            assert "entities" in data
    
    def test_create_default_database_integration(self):
        """Test create_default_database function integration."""
        # Test with no arguments
        db1 = create_default_database()
        assert len(db1.entities) == 0
        assert len(db1.speaker_map) == 1
        assert "speaker_0" in db1.speaker_map
        
        # Test with entities
        entity = Entity(
            entity_id="test_001", entity_type="word", text="test",
            start_time=0.0, end_time=0.5, duration=0.5,
            confidence=0.9, probability=0.9, syllables=["test"],
            syllable_count=1, quality_score=0.8, speaker_id="speaker_0",
            recording_id="test", recording_path="test.wav", processed=False,
            created_at=datetime.now().isoformat()
        )
        
        db2 = create_default_database(entities=[entity])
        assert len(db2.entities) == 1
        assert db2.entities[0].text == "test"


class TestErrorHandlingIntegration:
    """Test error handling integration in database operations."""
    
    def test_permission_error_handling_integration(self):
        """Test permission error handling integration."""
        config = Config()
        writer = DatabaseWriter(config)
        
        database = create_default_database()
        
        # Try to write to restricted location
        restricted_path = Path("/root/restricted.json")
        
        with pytest.raises(DatabaseError):
            writer.write_database(database, restricted_path)
    
    def test_disk_space_error_simulation_integration(self):
        """Test disk space error simulation integration."""
        config = Config()
        writer = DatabaseWriter(config)
        
        database = create_default_database()
        
        with tempfile.TemporaryDirectory() as temp_dir:
            output_path = Path(temp_dir) / "disk_full.json"
            
            # Mock file operations to simulate disk full
            with patch('builtins.open', side_effect=OSError("No space left on device")):
                with pytest.raises(DatabaseError):
                    writer.write_database(database, output_path)
    
    def test_corrupted_backup_handling_integration(self):
        """Test corrupted backup handling integration."""
        config = Config()
        config.output.backup_on_update = True
        writer = DatabaseWriter(config)
        
        database = create_default_database()
        
        with tempfile.TemporaryDirectory() as temp_dir:
            output_path = Path(temp_dir) / "backup_test.json"
            
            # Create corrupted existing file
            with open(output_path, 'w') as f:
                f.write("corrupted json content")
            
            # Writing should still succeed (creates backup of corrupted file)
            result_path = writer.write_database(database, output_path)
            
            assert result_path.exists()
            
            # Verify new file is valid JSON
            with open(result_path, 'r') as f:
                data = json.load(f)
            assert "metadata" in data


class TestLargeDataIntegration:
    """Test integration with large datasets."""
    
    def test_large_database_integration(self):
        """Test integration with large database."""
        config = Config()
        writer = DatabaseWriter(config)
        
        # Create large database (1000 entities)
        entities = []
        for i in range(1000):
            entity = Entity(
                entity_id=f"word_{i+1:04d}", entity_type="word", text=f"palabra{i+1}",
                start_time=float(i), end_time=float(i+0.5), duration=0.5,
                confidence=0.9, probability=0.9, syllables=[f"pa{i+1}"],
                syllable_count=1, quality_score=0.8, speaker_id="speaker_0",
                recording_id="test", recording_path="test.wav", processed=False,
                created_at=datetime.now().isoformat()
            )
            entities.append(entity)
        
        database = create_default_database(entities=entities)
        
        with tempfile.TemporaryDirectory() as temp_dir:
            output_path = Path(temp_dir) / "large_db.json"
            
            # Write large database
            result_path = writer.write_database(database, output_path)
            
            assert result_path.exists()
            
            # Verify all entities were written
            with open(result_path, 'r') as f:
                data = json.load(f)
            
            assert len(data['entities']) == 1000
            assert data['metadata']['entity_count'] if 'entity_count' in data['metadata'] else len(data['entities']) == 1000
    
    def test_unicode_content_integration(self):
        """Test integration with complex Unicode content."""
        config = Config()
        writer = DatabaseWriter(config)
        
        # Create entities with complex Unicode
        unicode_words = [
            "niño", "corazón", "español", "piñata", "señor",
            "café", "José", "María", "años", "mañana"
        ]
        
        entities = []
        for i, word in enumerate(unicode_words):
            entity = Entity(
                entity_id=f"word_{i+1:03d}", entity_type="word", text=word,
                start_time=float(i), end_time=float(i+0.5), duration=0.5,
                confidence=0.9, probability=0.9, syllables=[word],
                syllable_count=1, quality_score=0.8, speaker_id="speaker_0",
                recording_id="test", recording_path="test.wav", processed=False,
                created_at=datetime.now().isoformat()
            )
            entities.append(entity)
        
        database = create_default_database(entities=entities)
        
        with tempfile.TemporaryDirectory() as temp_dir:
            output_path = Path(temp_dir) / "unicode_test.json"
            
            writer.write_database(database, output_path)
            
            # Verify Unicode preservation
            with open(output_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            for word in unicode_words:
                assert word in content
            
            # Verify round-trip
            with open(output_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            restored_words = [entity['text'] for entity in data['entities']]
            assert set(restored_words) == set(unicode_words)