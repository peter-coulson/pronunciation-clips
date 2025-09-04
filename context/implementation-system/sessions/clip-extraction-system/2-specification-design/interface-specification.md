# Level 3 Interface Specification

## Session Information
- **Session Name**: clip-extraction-system  
- **Feature Name**: Pronunciation Clip Extraction System
- **Specification Level**: Level 3 (Interface Level)
- **Interface Date**: 2025-09-03
- **Previous Level**: Architecture Level (component relationships defined)
- **Next Level**: Behavior Level (test cases and expected behaviors)

## Interface Overview

### Interface Design Purpose
Define clean, implementable boundaries for the architectural components identified in Level 2, establishing contracts that enable independent development and comprehensive testing.

### Interface Design Principles
- **Contract-First Design**: All interfaces define preconditions, postconditions, and error conditions
- **Type Safety**: Pydantic models ensure runtime validation and IDE support
- **Separation of Concerns**: Each interface has a single, well-defined responsibility
- **Composability**: Interfaces can be combined without tight coupling
- **Testability**: All interfaces support mocking and unit testing

## Component Interface Definitions

### 1. Foundation Layer Interfaces

#### Configuration Management Interface
```python
# config.py interface
class Config(BaseModel):
    audio: AudioConfig
    whisper: WhisperConfig  
    speakers: SpeakersConfig
    quality: QualityConfig
    system: SystemConfig

def load_config(config_path: str = "config.yaml") -> Config:
    """Load and validate configuration from YAML file with environment overrides.
    
    Args:
        config_path: Path to YAML configuration file
        
    Returns:
        Validated configuration object
        
    Raises:
        ConfigurationError: Invalid configuration or file not found
        ValidationError: Configuration fails Pydantic validation
    """

def get_env_override(key: str, default: Any = None) -> Any:
    """Get environment variable override for configuration key.
    
    Args:
        key: Configuration key (supports dot notation: "audio.buffer_duration")
        default: Default value if environment variable not set
        
    Returns:
        Environment variable value or default
    """
```

#### Data Models Interface
```python
# models.py interface
class Entity(BaseModel):
    entity_id: str
    entity_type: str  # "word", "phrase", "speaker_segment"
    text: str
    start_time: float
    end_time: float
    duration: float
    confidence: float
    probability: float
    speaker_id: int
    recording_id: str
    recording_path: str
    created_at: str
    
    @field_validator('end_time')
    @classmethod
    def validate_time_order(cls, v, info):
        """Validate end_time > start_time"""
        
    @field_validator('duration')  
    @classmethod
    def validate_duration_match(cls, v, info):
        """Validate duration matches time difference within 1ms tolerance"""

class WordDatabase(BaseModel):
    version: str
    created_at: str
    recording_id: str
    recording_path: str
    speaker_map: Dict[int, SpeakerInfo]
    entities: List[Entity]
    
    def get_entities_by_type(self, entity_type: str) -> List[Entity]:
        """Filter entities by type with validation"""
        
    def get_entities_by_speaker(self, speaker_id: int) -> List[Entity]:
        """Filter entities by speaker ID with validation"""
        
    def get_entities_by_confidence(self, min_confidence: float) -> List[Entity]:
        """Filter entities by minimum confidence threshold"""

class SpeakerInfo(BaseModel):
    speaker_id: int
    speaker_name: Optional[str] = None
    total_duration: float
    segment_count: int
    confidence_avg: float
```

#### Exception Handling Interface
```python
# exceptions.py interface  
class PipelineError(Exception):
    """Base exception for all pipeline operations"""
    def __init__(self, message: str, context: Dict[str, Any] = None):
        self.message = message
        self.context = context or {}
        super().__init__(message)

class ConfigurationError(PipelineError):
    """Configuration loading or validation errors"""
    
class AudioProcessingError(PipelineError):
    """Audio loading, validation, or processing errors"""
    
class TranscriptionError(PipelineError):
    """Whisper transcription processing errors"""
    
class DiarizationError(PipelineError):
    """Speaker diarization processing errors"""
    
class DatabaseError(PipelineError):
    """JSON database operations errors"""
    
class ClipExtractionError(PipelineError):
    """Audio clip extraction and file creation errors"""
```

### 2. Audio-to-JSON Pipeline Interfaces

#### Audio Processor Interface
```python
# audio_processor.py interface
class AudioMetadata(BaseModel):
    sample_rate: int
    channels: int
    duration: float
    format: str
    file_size: int
    
def load_audio(file_path: str, target_sample_rate: int = 16000) -> Tuple[np.ndarray, AudioMetadata]:
    """Load and preprocess audio file for pipeline processing.
    
    Args:
        file_path: Path to audio file (.wav, .mp3, .m4a, .flac)
        target_sample_rate: Resample to this rate (default 16kHz)
        
    Returns:
        Tuple of (audio_array, metadata)
        
    Raises:
        AudioProcessingError: File not found, format unsupported, or loading failed
    """

def validate_audio_format(file_path: str) -> bool:
    """Validate audio file format compatibility.
    
    Args:
        file_path: Path to audio file
        
    Returns:
        True if format supported by librosa/soundfile
        
    Raises:
        AudioProcessingError: File access or validation errors
    """

def extract_audio_metadata(file_path: str) -> AudioMetadata:
    """Extract metadata without loading full audio into memory.
    
    Args:
        file_path: Path to audio file
        
    Returns:
        Audio metadata object
        
    Raises:
        AudioProcessingError: Metadata extraction failed
    """
```

#### Transcription Engine Interface
```python
# transcription_engine.py interface
class TranscriptionResult(BaseModel):
    segments: List[Dict[str, Any]]  # Whisper segment results
    language: str
    processing_time: float
    model_name: str
    
def initialize_whisper_model(model_name: str = "base", device: str = "cpu") -> Any:
    """Initialize faster-whisper model with specified configuration.
    
    Args:
        model_name: Whisper model size (tiny, base, small, medium, large)
        device: Processing device (cpu, cuda, mps)
        
    Returns:
        Initialized WhisperModel instance
        
    Raises:
        TranscriptionError: Model loading or device configuration failed
    """

def transcribe_audio(audio_array: np.ndarray, model: Any, config: WhisperConfig) -> TranscriptionResult:
    """Transcribe audio using faster-whisper with word-level timestamps.
    
    Args:
        audio_array: Audio data array (16kHz mono/stereo)
        model: Initialized WhisperModel instance
        config: Whisper configuration parameters
        
    Returns:
        Transcription results with word-level timing
        
    Raises:
        TranscriptionError: Transcription processing failed
    """

def extract_words_from_segments(segments: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Extract word-level information from Whisper segments.
    
    Args:
        segments: Whisper transcription segments
        
    Returns:
        List of word dictionaries with timing and confidence
        
    Raises:
        TranscriptionError: Word extraction or validation failed
    """
```

#### Diarization Processor Interface  
```python
# diarization_processor.py interface
class DiarizationResult(BaseModel):
    speaker_segments: List[Dict[str, Any]]  # PyAnnote segment results
    speaker_count: int
    processing_time: float
    model_name: str
    
def initialize_diarization_pipeline(device: str = "cpu", use_auth_token: Optional[str] = None) -> Any:
    """Initialize PyAnnote speaker diarization pipeline.
    
    Args:
        device: Processing device (cpu, mps, cuda)  
        use_auth_token: HuggingFace authentication token
        
    Returns:
        Initialized diarization pipeline
        
    Raises:
        DiarizationError: Pipeline initialization failed
    """

def perform_diarization(audio_array: np.ndarray, pipeline: Any, config: SpeakersConfig) -> DiarizationResult:
    """Perform speaker diarization on audio with configurable parameters.
    
    Args:
        audio_array: Audio data array (16kHz mono/stereo)
        pipeline: Initialized PyAnnote pipeline
        config: Speaker diarization configuration
        
    Returns:
        Speaker segment results with timing and confidence
        
    Raises:
        DiarizationError: Diarization processing failed
    """

def align_speakers_with_words(words: List[Dict], speaker_segments: List[Dict]) -> List[Dict]:
    """Assign speaker IDs to word-level transcription results.
    
    Args:
        words: Word-level transcription with timestamps
        speaker_segments: Speaker diarization segments
        
    Returns:
        Words with assigned speaker_id fields
        
    Raises:
        DiarizationError: Speaker alignment failed
    """
```

#### Entity Creator Interface
```python
# entity_creator.py interface
def create_word_entities(words: List[Dict[str, Any]], recording_id: str, recording_path: str, config: QualityConfig) -> List[Entity]:
    """Convert transcription words to Entity objects with quality filtering.
    
    Args:
        words: Word-level transcription results (with optional speaker_id)
        recording_id: Unique identifier for recording  
        recording_path: Path to original audio file
        config: Quality filtering configuration
        
    Returns:
        List of validated Entity objects
        
    Raises:
        ValidationError: Entity validation failed
        ConfigurationError: Invalid quality filter configuration
    """

def apply_quality_filters(entities: List[Entity], config: QualityConfig) -> List[Entity]:
    """Filter entities based on quality thresholds.
    
    Args:
        entities: List of Entity objects to filter
        config: Quality filtering parameters
        
    Returns:
        Filtered list of entities meeting quality criteria
        
    Raises:
        ValidationError: Quality filter validation failed
    """

def apply_colombian_spanish_buffering(entities: List[Entity], buffer_duration: float = 0.1) -> List[Entity]:
    """Apply Colombian Spanish zero-gap buffering to prevent word overlap.
    
    Args:
        entities: List of Entity objects with timing
        buffer_duration: Buffer duration in seconds (default 0.1s)
        
    Returns:
        Entities with adjusted timing for Colombian Spanish characteristics
        
    Raises:
        ValidationError: Buffer application failed
    """
```

#### Database Writer Interface
```python
# database_writer.py interface
def write_word_database(entities: List[Entity], output_path: str, recording_info: Dict[str, Any], speaker_info: Dict[int, SpeakerInfo]) -> None:
    """Write entities to JSON database with atomic operations.
    
    Args:
        entities: List of validated Entity objects
        output_path: Path for JSON database file
        recording_info: Recording metadata (id, path, created_at)
        speaker_info: Speaker identification mapping
        
    Returns:
        None
        
    Raises:
        DatabaseError: File write operation failed
        ValidationError: Database schema validation failed
    """

def backup_existing_database(database_path: str) -> str:
    """Create backup of existing database before overwrite.
    
    Args:
        database_path: Path to existing database file
        
    Returns:
        Path to backup file
        
    Raises:
        DatabaseError: Backup operation failed
    """

def rollback_database_changes(database_path: str, backup_path: str) -> None:
    """Rollback database changes using backup file.
    
    Args:
        database_path: Path to current database file
        backup_path: Path to backup file for restoration
        
    Returns:
        None
        
    Raises:
        DatabaseError: Rollback operation failed
    """
```

### 3. JSON-to-Clips Pipeline Interfaces

#### Database Reader Interface
```python
# database_reader.py interface
def load_word_database(database_path: str) -> WordDatabase:
    """Load and validate JSON database for clip extraction.
    
    Args:
        database_path: Path to JSON database file
        
    Returns:
        Validated WordDatabase object
        
    Raises:
        DatabaseError: File loading or validation failed
    """

def validate_database_schema(database_data: Dict[str, Any]) -> bool:
    """Validate database schema compatibility.
    
    Args:
        database_data: Raw database dictionary from JSON
        
    Returns:
        True if schema is valid and compatible
        
    Raises:
        ValidationError: Schema validation failed
    """
```

#### Search Engine Interface
```python
# search_engine.py interface
class SearchCriteria(BaseModel):
    text_pattern: Optional[str] = None  # Regex or substring matching
    speaker_ids: Optional[List[int]] = None  # Filter by specific speakers
    min_confidence: Optional[float] = None  # Minimum confidence threshold
    max_confidence: Optional[float] = None  # Maximum confidence threshold  
    min_duration: Optional[float] = None  # Minimum clip duration
    max_duration: Optional[float] = None  # Maximum clip duration
    entity_types: Optional[List[str]] = None  # Filter by entity types
    
def search_entities(database: WordDatabase, criteria: SearchCriteria) -> List[Entity]:
    """Search database entities using flexible criteria.
    
    Args:
        database: Loaded WordDatabase object
        criteria: Search filtering parameters
        
    Returns:
        List of entities matching search criteria
        
    Raises:
        ValidationError: Search criteria validation failed
        DatabaseError: Search operation failed
    """

def rank_search_results(entities: List[Entity], ranking_criteria: str = "confidence") -> List[Entity]:
    """Rank search results using specified criteria.
    
    Args:
        entities: List of entities to rank
        ranking_criteria: Ranking method ("confidence", "duration", "alphabetical")
        
    Returns:
        Ranked list of entities
        
    Raises:
        ValueError: Invalid ranking criteria
    """
```

#### Clip Extractor Interface
```python
# clip_extractor.py interface
class ClipMetadata(BaseModel):
    entity_id: str
    original_recording: str
    clip_path: str
    start_time: float
    end_time: float
    duration: float
    speaker_id: int
    text: str
    confidence: float
    created_at: str
    
def extract_audio_clip(entity: Entity, original_audio_path: str, output_dir: str, buffer_duration: float = 0.1) -> ClipMetadata:
    """Extract audio clip for entity with Colombian Spanish buffering.
    
    Args:
        entity: Entity object with timing information
        original_audio_path: Path to source audio file
        output_dir: Directory for clip output
        buffer_duration: Buffer around clip boundaries (default 0.1s)
        
    Returns:
        Metadata for created clip file
        
    Raises:
        ClipExtractionError: Audio extraction or file creation failed
        AudioProcessingError: Source audio loading failed
    """

def batch_extract_clips(entities: List[Entity], original_audio_path: str, output_dir: str, config: Dict[str, Any]) -> List[ClipMetadata]:
    """Extract multiple clips efficiently with shared audio loading.
    
    Args:
        entities: List of entities for clip extraction
        original_audio_path: Path to source audio file  
        output_dir: Directory for clip output
        config: Extraction configuration parameters
        
    Returns:
        List of metadata for all created clips
        
    Raises:
        ClipExtractionError: Batch extraction failed
        AudioProcessingError: Source audio processing failed
    """

def generate_clip_filename(entity: Entity, config: Dict[str, Any]) -> str:
    """Generate path-safe filename for audio clip.
    
    Args:
        entity: Entity object for filename generation
        config: Naming convention configuration
        
    Returns:
        Safe filename for audio clip
        
    Raises:
        ValueError: Filename generation failed
    """
```

### 4. CLI Interface Definitions

#### Command Router Interface
```python
# main.py interface (Click-based CLI)
@click.group()
@click.option('--config', default='config.yaml', help='Configuration file path')
@click.option('--verbose', is_flag=True, help='Enable verbose logging')
@click.pass_context
def cli(ctx, config, verbose):
    """Pronunciation Clip Extraction System CLI"""

@cli.command()
@click.argument('audio_path', type=click.Path(exists=True))
@click.option('--output', '-o', default='database.json', help='Output database path')
@click.option('--resume', is_flag=True, help='Resume from existing checkpoint')
def process_audio(audio_path, output, resume):
    """Process audio file to create word database"""

@cli.command()
@click.argument('database_path', type=click.Path(exists=True))
@click.option('--search', '-s', help='Text search pattern')
@click.option('--speaker', type=int, help='Filter by speaker ID')
@click.option('--min-confidence', type=float, help='Minimum confidence threshold')
@click.option('--output-dir', '-o', default='clips/', help='Output directory for clips')
def extract_clips(database_path, search, speaker, min_confidence, output_dir):
    """Extract clips from word database"""

@cli.command()
@click.argument('database_path', type=click.Path(exists=True))
def analyze_speakers(database_path):
    """Analyze speaker information in database"""

@cli.command()
@click.argument('database_path', type=click.Path(exists=True))
@click.option('--speaker-id', type=int, required=True)
@click.option('--speaker-name', required=True)
def label_speaker(database_path, speaker_id, speaker_name):
    """Add speaker name label to database"""
```

## Context Integration Notes

### Constraint Knowledge Application
- **Entity Model Contracts**: All required fields defined with Pydantic validation (entity_id, entity_type, text, start_time, end_time, duration, confidence, probability, speaker_id, recording_id, recording_path, created_at)
- **Speaker Identification**: Integer-based speaker_id (0, 1, 2) with SpeakerInfo mapping as confirmed in implementation
- **Temporal Constraints**: end_time > start_time validation, duration matching time difference within 1ms tolerance
- **Quality Filtering**: Configurable confidence thresholds, duration ranges, syllable count validation support

### Integration Knowledge Application  
- **Database Interface Contracts**: WordDatabase with query methods (get_entities_by_type, get_entities_by_speaker, get_entities_by_confidence)
- **Audio Processing Integration**: AudioMetadata extraction, format validation, resampling operations through librosa
- **CLI Interface Contracts**: Click command structure with arguments, options, progress feedback, error handling
- **External Dependency Contracts**: faster-whisper, PyAnnote, and librosa integration with proper error handling

### Pattern Knowledge Application
- **Entity Creation Patterns**: Word-to-entity conversion with quality filters and speaker assignment logic
- **Database Querying Patterns**: Method-based filtering by type, speaker, confidence with typed list returns  
- **CLI Command Patterns**: Context passing, configuration loading, verbose/quiet modes, structured error reporting
- **Configuration Loading Patterns**: File existence checks, YAML parsing, environment overlay, Pydantic validation

### Convention Knowledge Application
- **Field Naming**: snake_case for all model fields, consistent timestamp formats (ISO 8601)
- **ID Generation**: Structured entity_id format ("word_001"), sequential integer speaker IDs (0, 1, 2)
- **File Organization**: Predictable output paths, backup file naming, temporary file cleanup protocols  
- **Error Message Formatting**: Clear user-facing messages with optional verbose context through exception hierarchy

## Interface Validation

### Contract Completeness Assessment
- ✅ All architectural components have defined interfaces
- ✅ Input/output contracts specified with types and validation
- ✅ Error conditions and exception handling defined  
- ✅ Preconditions and postconditions documented
- ✅ Integration points between components specified

### Type Safety Validation
- ✅ Pydantic models provide runtime validation for all data structures
- ✅ Method signatures include type hints for parameters and returns
- ✅ Configuration models ensure type safety for system parameters
- ✅ Exception hierarchy provides typed error handling

### Implementability Assessment
- ✅ Interfaces are directly implementable from method signatures
- ✅ Dependencies clearly specified with integration contracts
- ✅ Configuration requirements defined with validation rules
- ✅ Testing interfaces support mocking and unit testing
- ✅ CLI interfaces provide complete user interaction coverage

### Interface Consistency Analysis
- ✅ Naming conventions consistent across all interfaces
- ✅ Error handling patterns uniform throughout system
- ✅ Configuration access patterns standardized
- ✅ Data model usage consistent across components
- ✅ Return type patterns follow established conventions

## Implementation Handoff Requirements

### Ready for Behavior Level Transition
- ✅ Component boundaries clearly defined with implementable contracts
- ✅ Data schemas fully specified with validation rules
- ✅ Error handling interfaces complete with exception hierarchy
- ✅ CLI command interfaces defined with Click integration
- ✅ External dependency integration contracts established

### Behavior Specification Requirements
The Behavior Level specification will need to define:
1. Test cases for each interface method with expected inputs/outputs
2. Error condition testing with specific exception scenarios  
3. Integration testing between components through interfaces
4. End-to-end workflow testing through CLI commands
5. Performance characteristics and resource usage expectations

### Interface Success Criteria Met
- ✅ Interfaces are directly implementable from Level 2 architecture
- ✅ Clean boundaries established with appropriate coupling
- ✅ Context knowledge properly integrated in interface design
- ✅ Type safety and validation ensured throughout
- ✅ Foundation established for comprehensive behavior specification