# Colombian Accent Clip Generator - Setup Guide

## Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run Test Mode (Recommended First)
```bash
python run_clip_generator.py
```
This will:
- Process first 5 minutes of audio only
- Generate ~15 sample clips
- Create validation report
- Save to `test-clips/` directory

### 3. Validate Test Results
Check the generated clips in `test-clips/`:
- **Audio quality**: Clear start/end, no cut-off words
- **Syllable accuracy**: Verify syllable counts are correct
- **File organization**: Check directory structure

### 4. Run Full Processing
```bash
python run_clip_generator.py --full
```

## Output Structure

```
practice-clips/
├── by-syllables/
│   ├── 2-syllables/     # Beginner level
│   ├── 3-syllables/     # Beginner level  
│   ├── 4-syllables/     # Intermediate
│   └── 5-6-syllables/   # Advanced
├── by-word/
│   └── [word]/
│       ├── palabra_001_3s_089c_1240ms.wav
│       ├── palabra_002_3s_092c_1180ms.wav
│       └── metadata.json
└── flashcard-ready/
    ├── beginner/        # 2-3 syllables
    ├── intermediate/    # 4-5 syllables
    └── advanced/        # 6+ syllables
```

## Configuration

Edit the `Config` class in `accent_clip_generator.py`:

```python
@dataclass
class Config:
    SYLLABLE_RANGE: Tuple[int, int] = (2, 6)     # Min/max syllables
    MIN_CONFIDENCE: float = 0.8                  # Whisper confidence
    MIN_DURATION: float = 0.3                    # Min clip length (sec)
    MAX_DURATION: float = 3.0                    # Max clip length (sec)
    WHISPER_MODEL: str = "medium"                # or "large" for better accuracy
```

## File Naming Convention

`[word]_[instance]_[syllables]s_[confidence]c_[duration]ms.wav`

Example: `literatura_003_5s_089c_1240ms.wav`
- Word: "literatura"
- Instance: 3rd occurrence
- Syllables: 5
- Confidence: 89%
- Duration: 1240ms

## Troubleshooting

### Low Clip Count
- Lower `MIN_CONFIDENCE` (try 0.7)
- Expand `SYLLABLE_RANGE` (try 1-8)
- Check audio quality of source

### Poor Audio Quality
- Increase `MIN_CONFIDENCE` (try 0.9)
- Adjust `BUFFER_MS` for better word boundaries

### Memory Issues
- Use smaller Whisper model ("base" or "small")
- Process in test mode first

## Integration with Flashcards

The generated clips are ready for flashcard integration:
1. Use files from `flashcard-ready/` directories
2. Import `metadata.json` for word information
3. Organize by difficulty level (beginner/intermediate/advanced)

## Audio Requirements

- Format: MP3, WAV, M4A, or FLAC
- Quality: Clear speech, minimal background noise
- Language: Colombian Spanish (or any Spanish variant)
- Location: Place in `video-sources/` directory