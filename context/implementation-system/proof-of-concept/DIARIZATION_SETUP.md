# Diarization Setup Guide

## Overview

The pronunciation clips system includes speaker diarization functionality with PyAnnote-based speaker separation, MPS hardware acceleration, and pipeline caching. The system automatically detects and separates multiple speakers in audio files with hardware optimization for M1 Macs.

## Default Behavior

**By default, diarization tests are SKIPPED** to keep core development fast and simple. The system will:
- ✅ Process audio with single-speaker assignment (`speaker_id=0`)
- ✅ Pass all core E2E tests (stages 1-8)
- ✅ Provide full CLI functionality
- ⚠️ Skip diarization-specific E2E tests

## Enabling Full Diarization Testing

### Prerequisites

1. **HuggingFace Account**: Create account at https://huggingface.co/
2. **Model Access**: Accept terms at https://hf.co/pyannote/speaker-diarization
3. **Access Token**: Generate at https://hf.co/settings/tokens

### Step-by-Step Setup

#### 1. Create HuggingFace Access Token
```bash
# Visit https://hf.co/settings/tokens
# Click "New token" → "Read" access → Copy token
```

#### 2. Accept Model Terms
```bash
# Visit https://hf.co/pyannote/speaker-diarization
# Click "Accept" to agree to model terms
# Required for gated model access
```

#### 3. Set Environment Variables
```bash
# Export your HuggingFace token
export HF_TOKEN="your_token_here"

# Enable diarization tests
export ENABLE_DIARIZATION_TESTS="true"
```

#### 4. Install Dependencies (if not already installed)
```bash
# Dependencies should already be in requirements.txt
pip install "pyannote.audio>=3.0.0" "faster-whisper>=1.2.0"
```

#### 5. Run Full Test Suite
```bash
# Run all tests including diarization
ENABLE_DIARIZATION_TESTS=true HF_TOKEN=your_token ./pytest_venv.sh tests/e2e/

# Run only diarization tests
ENABLE_DIARIZATION_TESTS=true HF_TOKEN=your_token ./pytest_venv.sh tests/e2e/test_diarization_e2e.py
```

## Testing Modes

### Core Development (Default - Recommended)
```bash
# Fast testing without ML dependencies
./pytest_venv.sh tests/e2e/test_stage*.py

# Result: 13/13 core E2E tests passing
# Diarization: Single speaker fallback (speaker_id=0)
```

### Full Feature Development (Optional)
```bash
# Complete system validation including ML
ENABLE_DIARIZATION_TESTS=true HF_TOKEN=xxx ./pytest_venv.sh tests/e2e/

# Result: All E2E tests including multi-speaker detection
# Diarization: Real speaker separation (speaker_id=0,1,2...)
```

## Production Deployment Options

### Option 1: Simple Deployment (No Diarization)
```yaml
# Minimal dependencies, single speaker mode
dependencies:
  - faster-whisper
  - librosa  
  - basic audio processing
features:
  - Audio transcription ✅
  - Entity creation ✅
  - Single speaker assignment ✅
  - CLI interface ✅
```

### Option 2: Full Featured Deployment (With Diarization)
```yaml
# Complete ML stack, multi-speaker detection  
dependencies:
  - faster-whisper
  - librosa
  - pyannote.audio
  - torch ecosystem
environment:
  - HF_TOKEN: required
features:
  - Audio transcription ✅
  - Entity creation ✅
  - Multi-speaker detection ✅
  - Speaker labeling ✅
  - CLI interface ✅
```

## Troubleshooting

### Common Issues

**"Could not download pipeline" Error**
```bash
# Cause: Missing or invalid HF_TOKEN
# Solution: Verify token and model access
export HF_TOKEN="your_valid_token"
```

**"Model is gated" Error**
```bash
# Cause: Haven't accepted model terms
# Solution: Visit https://hf.co/pyannote/speaker-diarization and accept
```

**Tests Still Failing**
```bash
# Check environment variables are set
echo $ENABLE_DIARIZATION_TESTS  # Should be "true" 
echo $HF_TOKEN                   # Should be your token

# Verify pyannote installation
python -c "import pyannote.audio; print('✅ pyannote.audio available')"
```

### Test Configuration

The system automatically detects the testing mode:

```python
# In test files
@pytest.mark.skipif(
    not os.getenv("ENABLE_DIARIZATION_TESTS"), 
    reason="Diarization tests disabled by default. Set ENABLE_DIARIZATION_TESTS=true to enable."
)
def test_diarization_functionality():
    # Full diarization testing
```

## Performance Impact

| Mode | Dependencies | Install Time | Test Time | Disk Space |
|------|-------------|--------------|-----------|------------|
| Core | Basic | ~30s | ~15s | ~500MB |
| Full | ML Stack | ~5min | ~30s | ~2GB |

## Security Notes

- **Never commit HF_TOKEN** to version control
- Store tokens in environment variables or secure credential stores
- Use `.env` files with `.gitignore` for local development
- Rotate tokens periodically for security

## Development Workflow

```bash
# 1. Core development (daily workflow)
git checkout feature-branch
./pytest_venv.sh tests/e2e/test_stage*.py  # Fast core tests

# 2. Full validation (before PR)
export HF_TOKEN="your_token"
export ENABLE_DIARIZATION_TESTS="true"
./pytest_venv.sh tests/e2e/  # Complete validation

# 3. Clean environment
unset HF_TOKEN ENABLE_DIARIZATION_TESTS
```

This approach ensures fast development cycles while maintaining the ability to validate the complete system when needed.

## Quick Start Examples

### Default Development (Recommended)
```bash
# Fast core development - no diarization dependencies needed
./pytest_venv.sh tests/e2e/test_stage*.py
# Result: 13/13 core tests passing, diarization tests skipped

# Check what tests are skipped
./pytest_venv.sh tests/e2e/test_diarization_e2e.py -v
# Result: 12/12 diarization tests skipped with clear reason
```

### Full Diarization Testing (When Needed)
```bash
# 1. Set up HuggingFace authentication first
export HF_TOKEN="your_token_here"

# 2. Enable diarization tests
export ENABLE_DIARIZATION_TESTS="true"

# 3. Run full test suite
./pytest_venv.sh tests/e2e/
# Result: All tests including real multi-speaker detection

# 4. Run only diarization tests
./pytest_venv.sh tests/e2e/test_diarization_e2e.py
# Result: Real ML-based speaker separation testing
```

### Verification Commands
```bash
# Verify environment setup
echo "Diarization enabled: $ENABLE_DIARIZATION_TESTS"
echo "HF Token set: ${HF_TOKEN:+YES}"

# Test specific functionality
ENABLE_DIARIZATION_TESTS=true ./pytest_venv.sh tests/e2e/test_diarization_e2e.py::TestDiarizationE2E::test_basic_diarization_detection_e2e -v
```