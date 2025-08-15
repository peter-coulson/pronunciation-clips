# E2E Test Skeleton Setup Plan

## Overview
Create skeleton end-to-end tests for all 8 stages BEFORE any implementation begins. These tests define exact success criteria and force proper interface design.

## Pre-Implementation Strategy

### **1. Create Test Directory Structure**
```
tests/
├── e2e/
│   ├── __init__.py
│   ├── test_stage1_foundation_e2e.py
│   ├── test_stage2_audio_e2e.py
│   ├── test_stage3_transcription_e2e.py
│   ├── test_stage4_entities_e2e.py
│   ├── test_stage5_database_e2e.py
│   ├── test_stage6_pipeline_e2e.py
│   ├── test_stage7_speakers_e2e.py
│   └── test_stage8_cli_e2e.py
├── fixtures/
│   ├── test_config.yaml
│   ├── spanish_30sec_16khz.wav
│   ├── spanish_30sec_44khz.wav
│   ├── spanish_clear_30sec.wav
│   ├── spanish_noisy_30sec.wav
│   ├── spanish_quiet_30sec.wav
│   ├── spanish_complete_test.wav
│   └── expected_outputs/
│       ├── stage1_expected.json
│       ├── stage3_expected_transcription.json
│       └── stage6_expected_database.json
└── conftest.py  # Shared pytest fixtures
```

### **2. Skeleton Test Implementation**

#### **Stage 1: Foundation E2E Test**
```python
# tests/e2e/test_stage1_foundation_e2e.py
import pytest
from pathlib import Path

def test_foundation_e2e():
    """
    Test: Load config → Create models → Initialize logging → Serialize to JSON
    
    Success Criteria:
    - Config loads from YAML without errors
    - Entity creation with validation works
    - Structured logging initializes with session ID
    - JSON serialization/deserialization works
    - No exceptions thrown in full workflow
    """
    # Will fail initially - that's expected
    from src.shared.config import load_config
    from src.shared.models import Entity, WordDatabase
    from src.shared.logging_config import init_logger
    
    # Load config
    config = load_config("tests/fixtures/test_config.yaml")
    assert config is not None
    
    # Create entities
    entity = Entity(
        entity_id="word_001",
        entity_type="word", 
        text="hola",
        start_time=1.23,
        end_time=1.67,
        # ... all required fields
    )
    
    # Initialize logging
    logger = init_logger(config)
    logger.info("Test message", stage="foundation", word_count=1)
    
    # Create database
    database = WordDatabase(
        metadata={"version": "1.0"},
        speaker_map={"0": {"name": "Test Speaker"}},
        entities=[entity]
    )
    
    # Serialize and validate
    json_output = database.json()
    assert "entities" in json_output
    assert "speaker_map" in json_output
    
    # Round-trip test
    database_restored = WordDatabase.parse_raw(json_output)
    assert len(database_restored.entities) == 1
```

#### **Stage 2: Audio Processing E2E Test**
```python
# tests/e2e/test_stage2_audio_e2e.py
def test_audio_processing_e2e():
    """
    Test: Load audio file → Extract metadata → Validate format → Resample if needed
    
    Success Criteria:
    - Load 16kHz WAV file successfully
    - Extract correct duration, sample rate, channels
    - Resample 44.1kHz to 16kHz correctly
    - Reject invalid audio files with clear errors
    - Audio metadata matches expected values
    """
    from src.audio_to_json.audio_processor import process_audio
    from src.shared.config import load_config
    
    config = load_config("tests/fixtures/test_config.yaml")
    
    # Test 1: Valid 16kHz audio
    audio_data = process_audio("tests/fixtures/spanish_30sec_16khz.wav", config)
    assert audio_data.sample_rate == 16000
    assert abs(audio_data.duration - 30.0) < 0.1
    
    # Test 2: Resample 44.1kHz audio  
    audio_data = process_audio("tests/fixtures/spanish_30sec_44khz.wav", config)
    assert audio_data.sample_rate == 16000
    
    # Test 3: Invalid file should raise AudioError
    with pytest.raises(AudioError):
        process_audio("nonexistent.wav", config)
```

#### **Stage 3: Transcription E2E Test**
```python
# tests/e2e/test_stage3_transcription_e2e.py
def test_transcription_e2e():
    """
    Test: Audio data → Whisper transcription → Word timestamps
    
    Success Criteria:
    - Whisper transcribes Spanish audio successfully
    - Word timestamps are valid (start < end)
    - Confidence scores between 0.0 and 1.0
    - Word count reasonable for 30-second audio
    - Spanish language detection works
    """
    from src.audio_to_json.transcription import transcribe_audio
    from src.audio_to_json.audio_processor import process_audio
    from src.shared.config import load_config
    
    config = load_config("tests/fixtures/test_config.yaml")
    
    # Load and transcribe
    audio_data = process_audio("tests/fixtures/spanish_clear_30sec.wav", config) 
    words = transcribe_audio(audio_data, config.whisper)
    
    # Validate results
    assert len(words) > 0
    assert len(words) < 1000  # Reasonable for 30 seconds
    
    for word in words:
        assert word.start_time < word.end_time
        assert 0.0 <= word.confidence <= 1.0
        assert len(word.text.strip()) > 0
    
    # Check Spanish language processing
    spanish_words = [w.text for w in words]
    assert any(word in ["hola", "buenos", "días", "cómo"] for word in spanish_words)
```

#### **Stage 6: Full Pipeline E2E Test**
```python
# tests/e2e/test_stage6_pipeline_e2e.py
def test_full_pipeline_e2e():
    """
    Test: Audio file → Complete JSON database (full pipeline)
    
    Success Criteria:
    - Process real Spanish audio end-to-end
    - Output JSON contains expected word count (±20%)
    - All entities have valid timestamps and confidence scores
    - Processing completes within reasonable time
    - Smart buffering prevents word overlap
    """
    from src.audio_to_json.pipeline import process_audio_to_json
    from src.shared.config import load_config
    import json
    import time
    
    config = load_config("tests/fixtures/test_config.yaml")
    
    start_time = time.time()
    
    # Process complete audio file
    database = process_audio_to_json(
        "tests/fixtures/spanish_complete_test.wav", 
        config
    )
    
    processing_time = time.time() - start_time
    
    # Validate output structure
    assert database.metadata is not None
    assert database.speaker_map is not None
    assert len(database.entities) > 0
    
    # Validate entities
    for entity in database.entities:
        assert entity.entity_type == "word"
        assert entity.start_time < entity.end_time
        assert 0.0 <= entity.confidence <= 1.0
        assert entity.duration > 0
    
    # Performance check
    assert processing_time < 300  # Should complete within 5 minutes for test audio
    
    # Smart buffering validation (no overlap)
    sorted_entities = sorted(database.entities, key=lambda e: e.start_time)
    for i in range(len(sorted_entities) - 1):
        current = sorted_entities[i]
        next_entity = sorted_entities[i + 1] 
        # Current entity should not extend into next entity's start
        assert current.end_time <= next_entity.start_time + 0.001  # 1ms tolerance
```

### **3. Test Fixtures Creation**

#### **Audio Fixtures**
```python
# setup_audio_fixtures.py
"""
Create standardized test audio files for E2E testing
"""
import librosa
import soundfile as sf
import numpy as np

def create_test_audio_fixtures():
    """Generate test audio files with known characteristics"""
    
    # Generate 30-second sine wave test audio
    sample_rate = 16000
    duration = 30.0
    frequency = 440  # A4 note
    
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    audio_16khz = np.sin(2 * np.pi * frequency * t) * 0.1
    
    # Save 16kHz version
    sf.write("tests/fixtures/spanish_30sec_16khz.wav", audio_16khz, 16000)
    
    # Create 44.1kHz version
    audio_44khz = librosa.resample(audio_16khz, orig_sr=16000, target_sr=44100)
    sf.write("tests/fixtures/spanish_30sec_44khz.wav", audio_44khz, 44100)
    
    # Note: Real Spanish audio files should replace these synthetic ones
    print("✅ Test audio fixtures created")
    print("⚠️  Replace with real Spanish audio for actual testing")
```

#### **Configuration Fixture**
```yaml
# tests/fixtures/test_config.yaml
audio:
  sample_rate: 16000
  channels: 1
  buffer_seconds: 0.025  # Smart buffering

whisper:
  model: "base"  # Faster for testing
  language: "es"
  word_timestamps: true
  temperature: 0.0

speakers:
  enable_diarization: false
  default_speaker:
    name: "Test Speaker"
    id: "speaker_0"

output:
  database_path: "tests/output/test_database.json"
  encoding: "utf-8"
  pretty_print: true
  backup_on_update: false  # Disable for testing

quality:
  min_confidence: 0.8
  min_word_duration: 0.3
  max_word_duration: 3.0
  syllable_range: [2, 6]

logging:
  level: "DEBUG"
  format: "structured"
  file: "tests/output/test.log"
  console: false  # Quiet during testing
```

### **4. Setup Script Implementation**

```python
# setup_e2e_tests.py
"""
Creates skeleton E2E tests and fixtures for all pipeline stages
"""
import os
from pathlib import Path

def create_directory_structure():
    """Create complete test directory structure"""
    dirs = [
        "tests/e2e",
        "tests/fixtures",
        "tests/fixtures/expected_outputs", 
        "tests/output",
        "demos"
    ]
    
    for dir_path in dirs:
        Path(dir_path).mkdir(parents=True, exist_ok=True)
        
    # Create __init__.py files
    for test_dir in ["tests", "tests/e2e"]:
        init_file = Path(test_dir) / "__init__.py"
        init_file.write_text("# Test package\n")

def create_skeleton_tests():
    """Create all 8 stage E2E test files"""
    # Implementation would create all test files shown above
    print("✅ Created skeleton E2E tests for all 8 stages")

def create_test_fixtures():
    """Create test configuration and audio fixtures"""
    # Create test_config.yaml
    # Create synthetic audio files (to be replaced with real Spanish audio)
    print("✅ Created test fixtures")

def create_makefile():
    """Create Makefile for easy test execution"""
    makefile_content = """
# E2E Test Commands
test-e2e-all:
	pytest tests/e2e/ -v

test-e2e-stage1:
	pytest tests/e2e/test_stage1_foundation_e2e.py -v

test-e2e-stage2:
	pytest tests/e2e/test_stage2_audio_e2e.py -v

# ... commands for all stages

verify-e2e-setup:
	pytest tests/e2e/ --collect-only

clean-test-output:
	rm -rf tests/output/*
"""
    Path("Makefile").write_text(makefile_content)
    print("✅ Created Makefile with test commands")

def main():
    """Set up complete E2E testing framework"""
    print("🚀 Setting up E2E test skeletons...")
    
    create_directory_structure()
    create_skeleton_tests()
    create_test_fixtures()
    create_makefile()
    
    print("\n✅ E2E TEST SETUP COMPLETE!")
    print("\nNext steps:")
    print("1. Replace synthetic audio with real Spanish test files")
    print("2. Run: pytest tests/e2e/ --collect-only")
    print("3. Verify all tests are discoverable (will fail, that's expected)")
    print("4. Begin Stage 1 implementation")

if __name__ == "__main__":
    main()
```

## Implementation Order

### **Phase 1: Setup (Before Any Coding)**
1. **Run setup script**: `python setup_e2e_tests.py`
2. **Verify test discovery**: `pytest tests/e2e/ --collect-only`
3. **Add real Spanish audio**: Replace synthetic fixtures with actual audio
4. **Validate setup**: `make verify-e2e-setup`

### **Phase 2: Stage-by-Stage Development**
1. **Implement Stage 1**: Foundation modules
2. **Run E2E test**: `make test-e2e-stage1` (should pass when stage complete)
3. **Proceed to Stage 2**: Only after Stage 1 E2E passes
4. **Repeat**: Each stage must pass its E2E test before proceeding

## Success Criteria

### **Setup Success**
- All 8 E2E test files created
- Test fixtures in place (config + audio)
- All tests discoverable by pytest
- Clear failure messages indicating missing implementation

### **Development Success**
- Each stage E2E test passes before moving to next stage
- Real Spanish audio processed successfully
- Complete pipeline E2E test validates end-to-end workflow
- All interfaces forced to be well-defined through test requirements

This skeleton approach ensures we have clear targets and proper interfaces before any implementation begins.