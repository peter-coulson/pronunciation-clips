# Data Models & Processing

## Data Models (Pydantic-based)

### Core Entity Model
```python
class Entity(BaseModel):
    # Core identification
    entity_id: str              # "word_001", "sentence_001"
    entity_type: str            # "word", "sentence", "phrase"
    text: str                   # Actual text content
    
    # Temporal information
    start_time: float           # Start time in seconds (≥ 0.0)
    end_time: float            # End time in seconds (> start_time)
    duration: float            # Duration in seconds (matches end - start)
    
    # Whisper outputs
    confidence: float          # Confidence score (0.0-1.0)
    probability: float         # Probability score (0.0-1.0)
    
    # Analysis fields
    syllables: List[str]       # Syllable breakdown
    syllable_count: int        # Count (must match syllables length)
    phonetic: Optional[str]    # Phonetic transcription
    quality_score: float       # Overall quality score (0.0-1.0)
    
    # Speaker & context
    speaker_id: str            # Speaker identifier
    recording_id: str          # Recording identifier
    recording_path: str        # Path to original recording
    
    # Processing status
    processed: bool            # Whether clip extracted (default: False)
    clip_path: Optional[str]   # Path to extracted clip
    selection_reason: Optional[str]  # Reason for selection
    created_at: str            # ISO timestamp
```

### Database Container
```python
class WordDatabase(BaseModel):
    metadata: Dict[str, Any]           # Version, timestamps, config snapshot
    speaker_map: Dict[str, SpeakerInfo]  # Speaker ID → metadata mapping
    entities: List[Entity]             # All processed entities
    
    # Query methods
    def get_entities_by_type(entity_type: str) -> List[Entity]
    def get_entities_by_speaker(speaker_id: str) -> List[Entity]
    def get_entities_by_confidence(min_confidence: float) -> List[Entity]
```

### Speaker Information
```python
class SpeakerInfo(BaseModel):
    name: str                  # Speaker name
    gender: str               # "M", "F", "Unknown"
    region: str               # Region/dialect information
```

### Audio Metadata
```python
class AudioMetadata(BaseModel):
    path: str                 # File path
    duration: float           # Duration in seconds
    sample_rate: int          # Sample rate in Hz
    channels: int             # Number of channels (1-2)
    format: str              # File format
    size_bytes: int          # File size
```

## JSON Storage Schema

### Database Structure
```json
{
  "metadata": {
    "version": "1.0",
    "created_at": "2025-08-15T...",
    "whisper_model": "base",
    "audio_duration": 120.5,
    "entity_count": 245,
    "config_snapshot": {
      "min_confidence": 0.8,
      "syllable_range": [2, 6]
    }
  },
  "speaker_map": {
    "speaker_0": {"name": "Default Speaker", "gender": "Unknown", "region": "Unknown"},
    "speaker_1": {"name": "María", "gender": "F", "region": "Bogotá"}
  },
  "entities": [
    {
      "entity_id": "word_001",
      "entity_type": "word",
      "text": "hola",
      "start_time": 1.23,
      "end_time": 1.67,
      "duration": 0.44,
      "confidence": 0.95,
      "probability": 0.89,
      "syllables": ["ho", "la"],
      "syllable_count": 2,
      "speaker_id": "speaker_1",
      "recording_id": "rec_audio1_20250815_143022",
      "recording_path": "/path/to/audio1.wav",
      "processed": false,
      "clip_path": null,
      "created_at": "2025-08-15T14:30:22.123Z"
    }
  ]
}
```

## Colombian Spanish Specific Requirements

### Smart Buffering Implementation
**Critical Issue**: Fixed 50ms buffer causes word overlap in Colombian Spanish continuous speech

**Problem Example**:
- Word "buenas" ends at 0.540s
- Word "tardes" starts at 0.540s (0ms gap)
- Adding 50ms buffer → overlap by 50ms

**Solution**: Zero-Gap Detection
```python
def _apply_smart_buffering(self, database: WordDatabase) -> WordDatabase:
    for i in range(len(sorted_entities) - 1):
        current = sorted_entities[i]
        next_entity = sorted_entities[i + 1]
        
        # Check for zero gap (Colombian Spanish characteristic)
        gap = next_entity.start_time - current.end_time
        
        if abs(gap) < 0.001:  # Essentially zero gap
            # Do NOT add buffer - would cause overlap
            continue
```

### Validated Configuration Values
From Colombian Spanish testing (Juan Gabriel Vásquez audio):
```yaml
quality:
  min_confidence: 0.8        # 35% pass rate, avg confidence 0.978
  min_word_duration: 0.3     # Filters articles, keeps content words
  max_word_duration: 3.0     # Handles complex Spanish words
  syllable_range: [2, 6]     # 2-syl: 45%, 3-syl: 20%, 4+syl: 35%

whisper:
  model: "medium"            # Optimal speed/accuracy for Spanish
  language: "es"             # Required for proper Spanish tokenization
```

### Performance Characteristics
- **Transcription bottleneck**: 99.9% of processing time (231.6ms/word)
- **Clip extraction**: <1ms per clip (negligible)
- **Processing rate**: ~44min for 81min audio
- **Zero-gap frequency**: High percentage of word pairs in continuous Colombian Spanish

## Future Extensions

### Sentence/Phrase Support
```json
{
  "entity_id": "sentence_001",
  "entity_type": "sentence", 
  "text": "Hola, ¿cómo estás?",
  "word_ids": ["word_001", "word_002", "word_003"],
  "word_count": 3,
  "start_time": 1.23,
  "end_time": 3.45
}
```

### Migration Path to SQLite
- Flat JSON structure → Direct table mapping
- Pandas integration: `pd.read_json()` → `df.to_sql()`
- Query optimization through indexing