# Implementation Details

## Data Storage Architecture

### Storage Format
- **Initial**: JSON-based word occurrences database
- **Migration path**: Designed for easy conversion to SQLite in future
- **Structure**: Flat array of word occurrences for optimal querying
- **Future extensibility**: Designed to support sentences/phrases without breaking changes

### JSON Schema

```json
{
  "metadata": {
    "version": "1.0",
    "created_at": "2025-08-15T...",
    "whisper_model": "base"
  },
  "speaker_map": {
    "0": {"name": "María", "gender": "F", "region": "Bogotá"},
    "1": {"name": "Carlos", "gender": "M", "region": "Medellín"}, 
    "2": {"name": "Speaker_3", "gender": "Unknown", "region": "Unknown"}
  },
  "entities": [
    {
      "entity_id": "word_001",
      "entity_type": "word",
      "text": "hola",
      "start_time": 1.23,
      "end_time": 1.67,
      "duration": 0.44,
      
      // Whisper outputs
      "confidence": 0.95,
      "probability": 0.89,
      
      // Analysis fields
      "syllables": ["ho", "la"],
      "syllable_count": 2,
      "phonetic": "ˈoʊlə",
      "quality_score": 0.87,
      
      // Speaker & context
      "speaker_id": "0",
      "recording_id": "rec_audio1_wav",
      "recording_path": "audio1.wav",
      
      // Processing status
      "processed": false,
      "clip_path": null,
      "selection_reason": null,
      "created_at": "2025-08-15T..."
    }
  ]
}
```

## Dependencies

From `requirements.txt`:
- `openai-whisper>=20231117` - Speech recognition and word timestamps
- `librosa>=0.10.0` - Audio processing
- `pydub>=0.25.0` - Audio manipulation
- `soundfile>=0.12.0` - Audio I/O
- `pandas>=2.0.0` - Data analysis and JSON/SQL migration
- `numpy>=1.21.0` - Numerical operations
- `torch>=2.0.0` - Deep learning framework
- `torchaudio>=2.0.0` - Audio processing for PyTorch

## Modular Architecture

### Module Separation
- **Module 1**: Audio → JSON Pipeline (Initial focus)
  - Scope: Audio files → Complete JSON database with all entities
  - Output: Populated JSON, no audio clips extracted yet
- **Module 2**: JSON → Clips Pipeline (Future implementation)
  - Scope: JSON database → Audio clips + updated JSON processing status

### Shared Components (Root Level)
- **Configuration management**: Centralized config, no static data in modules
- **Logging framework**: Structured logging across both modules  
- **Core data models**: Entity, Speaker, Metadata schemas
- **Common validation**: Entity structure, timestamps, file paths, JSON schema

### Module-Specific Validation
- **Module 1**: Audio formats, sample rates, Whisper confidence thresholds, speaker diarization
- **Module 2**: Selection criteria, duration limits, clip naming conflicts

## Data Structure Design Decisions

### Entity Structure
- **Generic entities**: `word_occurrences` renamed to `entities` for extensibility
- **Multiple entries per word**: Each spoken instance gets its own record
- **Flat array structure**: Optimized for pandas operations and SQL migration
- **Unique entity IDs**: Enable precise tracking and updates
- **Entity types**: Currently `"word"` only, designed for future `"sentence"` and `"phrase"`

### Speaker Management
- **Speaker mapping**: Separate map linking IDs to names/metadata
- **Flexible identification**: Support both named speakers and unknown speakers
- **Filter capability**: Easy querying by speaker name or characteristics

### Processing Pipeline Compatibility
- **Pipeline stages**: Designed for transcription → selection → clip extraction
- **State tracking**: `processed` flag enables resumable operations
- **Atomic updates**: Structure supports concurrent clipping script updates

## Clip Storage

### Directory Structure
- **Flat structure**: Single `clips/` directory for all audio clips
- **Naming convention**: `{text}_{entity_type}_{entity_num}_{speaker}_{start}-{end}.wav`
- **Example**: `hola_word_001_maria_1.23-1.67.wav`

### Benefits
- Simple filesystem operations and atomic writes
- Human-readable filenames for easy browsing
- No directory management overhead
- Compatible with JSON database organization

## Future Extensions (Not Implemented Initially)

### Sentence/Phrase Support
**Note**: The JSON structure now supports this extensibility, but sentence/phrase functionality will not be implemented in the initial MVP.

Future sentence/phrase entities would extend the current structure:

```json
{
  "entity_id": "sentence_001", 
  "entity_type": "sentence",
  "text": "Hola, ¿cómo estás?",
  "start_time": 1.23,
  "end_time": 3.45,
  "word_ids": ["word_001", "word_002", "word_003"],
  "word_count": 3,
  "speaker_id": "0",
  "recording_id": "rec_audio1_wav",
  "processed": false,
  "clip_path": null
}
```

Additional fields for sentences/phrases:
- `word_ids`: References to constituent word entities
- `word_count`: Number of words (easily computed, can be added later)

## Migration Path

### JSON to SQLite
- **Easy conversion**: `pd.read_json()` → `df.to_sql()`
- **Normalized structure**: Current design maps directly to relational tables
- **Query optimization**: Flat structure enables efficient indexing and joins