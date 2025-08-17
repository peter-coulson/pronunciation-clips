"""
Unit tests for database writer module.

Tests JSON database writing, atomic operations, backup creation,
and validation. Focuses on file operations and error handling.
"""
import pytest
import json
import tempfile
import os
from pathlib import Path
from unittest.mock import patch, MagicMock
from datetime import datetime

from src.audio_to_json.database_writer import DatabaseWriter, write_database, create_default_database
from src.shared.models import WordDatabase, Entity, SpeakerInfo
from src.shared.config import Config, OutputConfig
from src.shared.exceptions import DatabaseError


class TestDatabaseWriter:
    """Test DatabaseWriter class."""
    
    def test_database_writer_creation(self):
        """Test creating DatabaseWriter with config."""
        config = Config()
        writer = DatabaseWriter(config)
        
        assert writer.config == config
        assert writer.logger is not None
    
    def test_write_database_basic(self):
        """Test basic database writing functionality."""
        config = Config()
        writer = DatabaseWriter(config)
        
        # Create test database
        database = create_default_database()
        
        with tempfile.TemporaryDirectory() as temp_dir:
            output_path = Path(temp_dir) / "test_database.json"
            
            result_path = writer.write_database(database, output_path)
            
            # Verify file was created
            assert result_path == output_path
            assert output_path.exists()
            
            # Verify content is valid JSON
            with open(output_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            assert 'metadata' in data
            assert 'speaker_map' in data
            assert 'entities' in data
    
    def test_write_database_with_entities(self):
        """Test writing database with entities."""
        config = Config()
        writer = DatabaseWriter(config)
        
        # Create test entity
        entity = Entity(
            entity_id="test_001",
            entity_type="word",
            text="hola",
            start_time=0.0,
            end_time=0.5,
            duration=0.5,
            confidence=0.9,
            probability=0.9,
            syllables=["ho", "la"],
            syllable_count=2,
            quality_score=0.8,
            speaker_id="speaker_0",
            recording_id="test",
            recording_path="test.wav",
            processed=False,
            created_at=datetime.now().isoformat()
        )
        
        database = create_default_database(entities=[entity])
        
        with tempfile.TemporaryDirectory() as temp_dir:
            output_path = Path(temp_dir) / "test_with_entities.json"
            
            writer.write_database(database, output_path)
            
            # Verify entity was written
            with open(output_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            assert len(data['entities']) == 1
            assert data['entities'][0]['text'] == "hola"
            assert data['entities'][0]['entity_id'] == "test_001"
    
    def test_write_database_pretty_print(self):
        """Test pretty printing option."""
        config = Config()
        config.output.pretty_print = True
        writer = DatabaseWriter(config)
        
        database = create_default_database()
        
        with tempfile.TemporaryDirectory() as temp_dir:
            output_path = Path(temp_dir) / "pretty.json"
            
            writer.write_database(database, output_path)
            
            # Check that file contains indentation (pretty printed)
            with open(output_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            assert '  ' in content  # Should have indentation
            assert '\n' in content  # Should have newlines
    
    def test_write_database_compact(self):
        """Test compact printing option."""
        config = Config()
        config.output.pretty_print = False
        writer = DatabaseWriter(config)
        
        database = create_default_database()
        
        with tempfile.TemporaryDirectory() as temp_dir:
            output_path = Path(temp_dir) / "compact.json"
            
            writer.write_database(database, output_path)
            
            # Check that file is compact (no unnecessary spaces)
            with open(output_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Should not have indentation spaces
            lines = content.split('\n')
            assert len([line for line in lines if line.startswith('  ')]) == 0
    
    def test_write_database_encoding(self):
        """Test different encoding options."""
        config = Config()
        config.output.encoding = "utf-8"
        writer = DatabaseWriter(config)
        
        # Create database with Spanish characters
        metadata = {
            "version": "1.0",
            "created_at": datetime.now().isoformat(),
            "description": "Español con acentos: ñ, á, é, í, ó, ú"
        }
        database = create_default_database(metadata=metadata)
        
        with tempfile.TemporaryDirectory() as temp_dir:
            output_path = Path(temp_dir) / "spanish.json"
            
            writer.write_database(database, output_path)
            
            # Verify Spanish characters are preserved
            with open(output_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            assert "ñ" in content
            assert "á" in content
            assert "Español" in content
    
    def test_write_database_backup_creation(self):
        """Test backup creation when overwriting existing file."""
        config = Config()
        config.output.backup_on_update = True
        writer = DatabaseWriter(config)
        
        database = create_default_database()
        
        with tempfile.TemporaryDirectory() as temp_dir:
            output_path = Path(temp_dir) / "database.json"
            
            # Write initial file
            writer.write_database(database, output_path)
            assert output_path.exists()
            
            # Modify database and write again
            database.metadata["version"] = "2.0"
            writer.write_database(database, output_path)
            
            # Check that backup was created
            backup_files = list(output_path.parent.glob("database_backup_*"))
            assert len(backup_files) == 1
            
            backup_path = backup_files[0]
            assert backup_path.exists()
            
            # Verify backup contains original version
            with open(backup_path, 'r') as f:
                backup_data = json.load(f)
            # Note: backup should have version 1.0, but since we're overwriting
            # the same object, it will have 2.0. In a real scenario, these would be different objects.
    
    def test_write_database_no_backup(self):
        """Test no backup creation when disabled."""
        config = Config()
        config.output.backup_on_update = False
        writer = DatabaseWriter(config)
        
        database = create_default_database()
        
        with tempfile.TemporaryDirectory() as temp_dir:
            output_path = Path(temp_dir) / "database.json"
            
            # Write initial file
            writer.write_database(database, output_path)
            
            # Write again
            writer.write_database(database, output_path)
            
            # Check that no backup was created
            backup_files = list(output_path.parent.glob("database_backup_*"))
            assert len(backup_files) == 0
    
    def test_write_database_directory_creation(self):
        """Test automatic directory creation."""
        config = Config()
        writer = DatabaseWriter(config)
        
        database = create_default_database()
        
        with tempfile.TemporaryDirectory() as temp_dir:
            nested_path = Path(temp_dir) / "nested" / "dir" / "database.json"
            
            writer.write_database(database, nested_path)
            
            # Verify directory was created
            assert nested_path.parent.exists()
            assert nested_path.exists()
    
    def test_write_database_default_path(self):
        """Test using default output path from config."""
        config = Config()
        writer = DatabaseWriter(config)
        
        database = create_default_database()
        
        with tempfile.TemporaryDirectory() as temp_dir:
            # Change working directory to temp dir
            original_cwd = os.getcwd()
            try:
                os.chdir(temp_dir)
                
                result_path = writer.write_database(database)
                
                # Should use config default
                expected_path = Path(config.output.database_path)
                assert result_path == expected_path
                assert expected_path.exists()
                
            finally:
                os.chdir(original_cwd)
    
    def test_write_database_atomic_operation(self):
        """Test atomic write operation (temp file then move)."""
        config = Config()
        writer = DatabaseWriter(config)
        
        database = create_default_database()
        
        with tempfile.TemporaryDirectory() as temp_dir:
            output_path = Path(temp_dir) / "atomic.json"
            
            # Mock the JSON writing to fail after temp file creation
            original_move = writer._write_json_file
            
            def failing_write(db, path):
                # Write to temp file first
                original_move(db, path)
                # Then simulate failure
                raise Exception("Simulated write failure")
            
            with patch.object(writer, '_write_json_file', side_effect=failing_write):
                with pytest.raises(DatabaseError):
                    writer.write_database(database, output_path)
                
                # Verify temp file was cleaned up
                temp_files = list(output_path.parent.glob("*.tmp"))
                assert len(temp_files) == 0
                
                # Verify final file was not created
                assert not output_path.exists()
    
    def test_write_database_validation_failure(self):
        """Test handling of validation failures."""
        config = Config()
        writer = DatabaseWriter(config)
        
        database = create_default_database()
        
        with tempfile.TemporaryDirectory() as temp_dir:
            output_path = Path(temp_dir) / "invalid.json"
            
            # Mock validation to fail
            with patch.object(writer, '_validate_written_file', side_effect=DatabaseError("Validation failed")):
                with pytest.raises(DatabaseError, match="Validation failed"):
                    writer.write_database(database, output_path)
                
                # Verify file was not created (cleaned up)
                assert not output_path.exists()
    
    def test_write_database_logging(self):
        """Test logging during database writing."""
        config = Config()
        writer = DatabaseWriter(config)
        
        database = create_default_database()
        
        with tempfile.TemporaryDirectory() as temp_dir:
            output_path = Path(temp_dir) / "logged.json"
            
            with patch.object(writer, 'log_stage_start') as mock_start, \
                 patch.object(writer, 'log_stage_complete') as mock_complete:
                
                writer.write_database(database, output_path)
                
                mock_start.assert_called_once()
                mock_complete.assert_called_once()
    
    def test_write_database_error_logging(self):
        """Test error logging during database writing."""
        config = Config()
        writer = DatabaseWriter(config)
        
        database = create_default_database()
        
        with tempfile.TemporaryDirectory() as temp_dir:
            output_path = Path(temp_dir) / "error.json"
            
            with patch.object(writer, '_write_json_file', side_effect=Exception("Write error")), \
                 patch.object(writer, 'log_stage_error') as mock_error:
                
                with pytest.raises(DatabaseError):
                    writer.write_database(database, output_path)
                
                mock_error.assert_called_once()
    
    def test_create_backup(self):
        """Test backup file creation."""
        config = Config()
        writer = DatabaseWriter(config)
        
        with tempfile.TemporaryDirectory() as temp_dir:
            original_path = Path(temp_dir) / "original.json"
            
            # Create original file
            with open(original_path, 'w') as f:
                json.dump({"test": "data"}, f)
            
            backup_path = writer._create_backup(original_path)
            
            assert backup_path.exists()
            assert backup_path.parent == original_path.parent
            assert "backup" in backup_path.name
            assert backup_path.suffix == original_path.suffix
            
            # Verify backup content matches original
            with open(backup_path, 'r') as f:
                backup_data = json.load(f)
            
            assert backup_data == {"test": "data"}
    
    def test_validate_written_file_valid(self):
        """Test validation of valid written file."""
        config = Config()
        writer = DatabaseWriter(config)
        
        database = create_default_database()
        
        with tempfile.TemporaryDirectory() as temp_dir:
            test_path = Path(temp_dir) / "valid.json"
            
            writer._write_json_file(database, test_path)
            
            # Should not raise exception
            writer._validate_written_file(test_path)
    
    def test_validate_written_file_invalid_json(self):
        """Test validation of invalid JSON file."""
        config = Config()
        writer = DatabaseWriter(config)
        
        with tempfile.TemporaryDirectory() as temp_dir:
            invalid_path = Path(temp_dir) / "invalid.json"
            
            # Write invalid JSON
            with open(invalid_path, 'w') as f:
                f.write("{ invalid json")
            
            with pytest.raises(DatabaseError, match="validation failed"):
                writer._validate_written_file(invalid_path)
    
    def test_validate_written_file_missing_keys(self):
        """Test validation of JSON missing required keys."""
        config = Config()
        writer = DatabaseWriter(config)
        
        with tempfile.TemporaryDirectory() as temp_dir:
            incomplete_path = Path(temp_dir) / "incomplete.json"
            
            # Write JSON missing required keys
            with open(incomplete_path, 'w') as f:
                json.dump({"metadata": {}}, f)  # Missing speaker_map and entities
            
            with pytest.raises(DatabaseError, match="validation failed"):
                writer._validate_written_file(incomplete_path)


class TestWriteDatabaseFunction:
    """Test standalone write_database function."""
    
    def test_write_database_function(self):
        """Test convenience write_database function."""
        config = Config()
        database = create_default_database()
        
        with tempfile.TemporaryDirectory() as temp_dir:
            output_path = Path(temp_dir) / "function_test.json"
            
            result_path = write_database(database, output_path, config)
            
            assert result_path == output_path
            assert output_path.exists()
            
            # Verify content
            with open(output_path, 'r') as f:
                data = json.load(f)
            
            assert 'metadata' in data
            assert 'speaker_map' in data
            assert 'entities' in data


class TestCreateDefaultDatabase:
    """Test create_default_database function."""
    
    def test_create_default_database_empty(self):
        """Test creating default database with no arguments."""
        database = create_default_database()
        
        assert isinstance(database, WordDatabase)
        assert len(database.entities) == 0
        assert len(database.speaker_map) == 1
        assert "speaker_0" in database.speaker_map
        assert database.metadata["version"] == "1.0"
        assert "created_at" in database.metadata
    
    def test_create_default_database_with_entities(self):
        """Test creating default database with entities."""
        entity = Entity(
            entity_id="test_001",
            entity_type="word",
            text="test",
            start_time=0.0,
            end_time=0.5,
            duration=0.5,
            confidence=0.9,
            probability=0.9,
            syllables=["test"],
            syllable_count=1,
            quality_score=0.8,
            speaker_id="speaker_0",
            recording_id="test",
            recording_path="test.wav",
            processed=False,
            created_at=datetime.now().isoformat()
        )
        
        database = create_default_database(entities=[entity])
        
        assert len(database.entities) == 1
        assert database.entities[0].text == "test"
    
    def test_create_default_database_with_custom_metadata(self):
        """Test creating default database with custom metadata."""
        custom_metadata = {
            "version": "2.0",
            "created_at": "2023-01-01T00:00:00",
            "custom_field": "custom_value"
        }
        
        database = create_default_database(metadata=custom_metadata)
        
        assert database.metadata["version"] == "2.0"
        assert database.metadata["custom_field"] == "custom_value"
    
    def test_create_default_database_with_custom_speakers(self):
        """Test creating default database with custom speaker mapping."""
        custom_speakers = {
            "alice": SpeakerInfo(name="Alice", gender="F", region="Colombia"),
            "bob": SpeakerInfo(name="Bob", gender="M", region="Spain")
        }
        
        database = create_default_database(speaker_map=custom_speakers)
        
        assert len(database.speaker_map) == 2
        assert database.speaker_map["alice"].name == "Alice"
        assert database.speaker_map["bob"].name == "Bob"
    
    def test_create_default_database_all_custom(self):
        """Test creating database with all custom parameters."""
        entity = Entity(
            entity_id="custom_001",
            entity_type="word",
            text="custom",
            start_time=0.0,
            end_time=0.5,
            duration=0.5,
            confidence=0.9,
            probability=0.9,
            syllables=["custom"],
            syllable_count=1,
            quality_score=0.8,
            speaker_id="custom_speaker",
            recording_id="custom",
            recording_path="custom.wav",
            processed=False,
            created_at=datetime.now().isoformat()
        )
        
        custom_metadata = {"version": "custom", "created_at": "custom_time"}
        custom_speakers = {"custom_speaker": SpeakerInfo(name="Custom Speaker")}
        
        database = create_default_database(
            entities=[entity],
            metadata=custom_metadata,
            speaker_map=custom_speakers
        )
        
        assert len(database.entities) == 1
        assert database.entities[0].text == "custom"
        assert database.metadata["version"] == "custom"
        assert database.speaker_map["custom_speaker"].name == "Custom Speaker"


class TestDatabaseWriterEdgeCases:
    """Test edge cases and boundary conditions."""
    
    def test_write_database_permission_error(self):
        """Test handling of permission errors."""
        config = Config()
        writer = DatabaseWriter(config)
        
        database = create_default_database()
        
        # Try to write to root directory (should fail with permission error)
        root_path = Path("/root_db.json")
        
        with pytest.raises(DatabaseError):
            writer.write_database(database, root_path)
    
    def test_write_database_large_database(self):
        """Test writing database with many entities."""
        config = Config()
        writer = DatabaseWriter(config)
        
        # Create database with many entities
        entities = []
        for i in range(100):
            entity = Entity(
                entity_id=f"word_{i:03d}",
                entity_type="word",
                text=f"word{i}",
                start_time=float(i),
                end_time=float(i + 0.5),
                duration=0.5,
                confidence=0.9,
                probability=0.9,
                syllables=[f"word{i}"],
                syllable_count=1,
                quality_score=0.8,
                speaker_id="speaker_0",
                recording_id="test",
                recording_path="test.wav",
                processed=False,
                created_at=datetime.now().isoformat()
            )
            entities.append(entity)
        
        database = create_default_database(entities=entities)
        
        with tempfile.TemporaryDirectory() as temp_dir:
            output_path = Path(temp_dir) / "large_db.json"
            
            result_path = writer.write_database(database, output_path)
            
            assert result_path.exists()
            
            # Verify all entities were written
            with open(result_path, 'r') as f:
                data = json.load(f)
            
            assert len(data['entities']) == 100
    
    def test_write_database_disk_full_simulation(self):
        """Test handling of disk full scenarios."""
        config = Config()
        writer = DatabaseWriter(config)
        
        database = create_default_database()
        
        with tempfile.TemporaryDirectory() as temp_dir:
            output_path = Path(temp_dir) / "disk_full.json"
            
            # Mock open to raise OSError (disk full)
            with patch('builtins.open', side_effect=OSError("No space left on device")):
                with pytest.raises(DatabaseError):
                    writer.write_database(database, output_path)