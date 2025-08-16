"""
Database writing module for atomic JSON operations.

Handles writing WordDatabase objects to JSON files with atomic operations,
backup creation, and validation. Ensures data integrity and provides
rollback capabilities for safe database updates.
"""
import json
import shutil
from pathlib import Path
from typing import Optional
from datetime import datetime

from ..shared.models import WordDatabase, SpeakerInfo
from ..shared.config import Config
from ..shared.exceptions import DatabaseError
from ..shared.logging_config import LoggerMixin


class DatabaseWriter(LoggerMixin):
    """Handles atomic database writing operations."""
    
    def __init__(self, config: Config):
        super().__init__()
        self.config = config
        
    def write_database(self, database: WordDatabase, output_path: Optional[Path] = None) -> Path:
        """
        Write WordDatabase to JSON file with atomic operations.
        
        Args:
            database: WordDatabase object to write
            output_path: Optional custom output path
            
        Returns:
            Path to the written database file
            
        Raises:
            DatabaseError: If database writing fails
        """
        try:
            # Determine output path
            if output_path is None:
                output_path = Path(self.config.output.database_path)
            else:
                output_path = Path(output_path)
                
            self.log_stage_start("database_writing", 
                               output_path=str(output_path),
                               entity_count=len(database.entities))
            
            # Ensure output directory exists
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Create backup if file exists
            backup_path = None
            if output_path.exists() and self.config.output.backup_on_update:
                backup_path = self._create_backup(output_path)
                self.log_progress("Backup created", backup_path=str(backup_path))
            
            # Write to temporary file first (atomic operation)
            temp_path = output_path.with_suffix(output_path.suffix + '.tmp')
            
            try:
                self._write_json_file(database, temp_path)
                
                # Validate written file
                self._validate_written_file(temp_path)
                
                # Atomic move to final location
                shutil.move(str(temp_path), str(output_path))
                
                self.log_stage_complete("database_writing",
                                      output_path=str(output_path),
                                      file_size=output_path.stat().st_size,
                                      entities_written=len(database.entities))
                
                return output_path
                
            except Exception as e:
                # Clean up temporary file
                if temp_path.exists():
                    temp_path.unlink()
                    
                # Restore backup if needed
                if backup_path and backup_path.exists():
                    shutil.move(str(backup_path), str(output_path))
                    self.log_progress("Backup restored due to write failure")
                    
                raise
                
        except Exception as e:
            self.log_stage_error("database_writing", e, output_path=str(output_path))
            if isinstance(e, DatabaseError):
                raise
            raise DatabaseError(f"Failed to write database: {e}", {"output_path": str(output_path)})
    
    def _create_backup(self, file_path: Path) -> Path:
        """Create timestamped backup of existing file."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"{file_path.stem}_backup_{timestamp}{file_path.suffix}"
        backup_path = file_path.parent / backup_name
        
        shutil.copy2(str(file_path), str(backup_path))
        return backup_path
    
    def _write_json_file(self, database: WordDatabase, file_path: Path):
        """Write database to JSON file with proper formatting."""
        with open(file_path, 'w', encoding=self.config.output.encoding) as f:
            if self.config.output.pretty_print:
                json.dump(
                    database.model_dump(),
                    f,
                    indent=2,
                    ensure_ascii=False,
                    separators=(',', ': ')
                )
            else:
                json.dump(
                    database.model_dump(),
                    f,
                    ensure_ascii=False,
                    separators=(',', ':')
                )
    
    def _validate_written_file(self, file_path: Path):
        """Validate that written file is valid JSON and can be parsed."""
        try:
            with open(file_path, 'r', encoding=self.config.output.encoding) as f:
                data = json.load(f)
                
            # Verify structure
            if not isinstance(data, dict):
                raise ValueError("JSON data is not a dictionary")
                
            required_keys = ['metadata', 'speaker_map', 'entities']
            for key in required_keys:
                if key not in data:
                    raise ValueError(f"Missing required key: {key}")
            
            # Try to parse back to WordDatabase
            WordDatabase.model_validate(data)
            
        except Exception as e:
            raise DatabaseError(f"Written file validation failed: {e}")


def write_database(database: WordDatabase, output_path: Path, config: Config) -> Path:
    """
    Convenience function for writing database.
    
    Args:
        database: WordDatabase object to write
        output_path: Path for output file
        config: Configuration object
        
    Returns:
        Path to written file
        
    Raises:
        DatabaseError: If writing fails
    """
    writer = DatabaseWriter(config)
    return writer.write_database(database, output_path)


def create_default_database(entities=None, metadata=None, speaker_map=None) -> WordDatabase:
    """
    Create a default WordDatabase with minimal required data.
    
    Args:
        entities: List of Entity objects (defaults to empty list)
        metadata: Metadata dictionary (defaults to basic metadata)
        speaker_map: Speaker mapping (defaults to single default speaker)
        
    Returns:
        WordDatabase object
    """
    if entities is None:
        entities = []
        
    if metadata is None:
        metadata = {
            "version": "1.0",
            "created_at": datetime.now().isoformat(),
            "whisper_model": "base"
        }
        
    if speaker_map is None:
        speaker_map = {
            "speaker_0": SpeakerInfo(
                name="Default Speaker",
                gender="Unknown",
                region="Unknown"
            )
        }
        
    return WordDatabase(
        metadata=metadata,
        speaker_map=speaker_map,
        entities=entities
    )