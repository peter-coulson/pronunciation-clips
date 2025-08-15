#!/usr/bin/env python3
"""
Colombian Accent Training: Whisper-Based Clip Generation
Automated Spanish pronunciation training using OpenAI Whisper and audio segmentation.
"""

import os
import json
import re
import time
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass, asdict
import logging

import whisper
import librosa
import soundfile as sf
from pydub import AudioSegment
import pandas as pd
import numpy as np

# Configuration
@dataclass
class Config:
    """Configuration for the clip generator"""
    SYLLABLE_RANGE: Tuple[int, int] = (2, 6)
    MIN_CONFIDENCE: float = 0.8
    MIN_DURATION: float = 0.3
    MAX_DURATION: float = 3.0
    BUFFER_MS: int = 50
    TEST_MODE: bool = True
    TEST_DURATION: int = 300  # 5 minutes
    WHISPER_MODEL: str = "medium"
    SAMPLE_RATE: int = 16000
    AUDIO_FORMAT: str = "wav"
    
    # Paths
    VIDEO_SOURCES_DIR: str = "video-sources"
    PRACTICE_CLIPS_DIR: str = "practice-clips"
    TRANSCRIPTS_DIR: str = "transcripts"
    TEST_CLIPS_DIR: str = "test-clips"

@dataclass
class WordClip:
    """Metadata for a word clip"""
    word: str
    syllable_count: int
    confidence: float
    duration_ms: int
    start_time: float
    end_time: float
    context: str
    difficulty: str
    phonetic: str
    instance_number: int
    
    def to_filename(self) -> str:
        """Generate standardized filename"""
        return f"{self.word}_{self.instance_number:03d}_{self.syllable_count}s_{int(self.confidence*100):03d}c_{self.duration_ms}ms.{Config.AUDIO_FORMAT}"

class SpanishSyllableCounter:
    """Spanish syllable counting using phonetic rules"""
    
    VOWELS = set('aeiouáéíóúü')
    DIPHTHONGS = {'ai', 'au', 'ei', 'eu', 'ia', 'ie', 'io', 'iu', 'oa', 'oe', 'oi', 'ou', 'ua', 'ue', 'ui', 'uo'}
    TRIPHTHONGS = {'iai', 'iau', 'iei', 'iou', 'uai', 'uau', 'uei', 'uou'}
    
    @classmethod
    def count_syllables(cls, word: str) -> int:
        """Count syllables in Spanish word using phonetic rules"""
        word = word.lower().strip()
        if not word:
            return 0
            
        # Remove non-letter characters
        word = re.sub(r'[^a-záéíóúüñ]', '', word)
        if not word:
            return 0
        
        # Handle triphthongs first
        for triph in cls.TRIPHTHONGS:
            word = word.replace(triph, 'X')
        
        # Handle diphthongs
        for diph in cls.DIPHTHONGS:
            word = word.replace(diph, 'X')
        
        # Count vowel groups (including X placeholders)
        vowel_groups = 0
        prev_vowel = False
        
        for char in word:
            is_vowel = char in cls.VOWELS or char == 'X'
            if is_vowel and not prev_vowel:
                vowel_groups += 1
            prev_vowel = is_vowel
        
        return max(1, vowel_groups)

class AccentClipGenerator:
    """Main class for generating Colombian accent training clips"""
    
    def __init__(self, config: Config = None):
        self.config = config or Config()
        self.syllable_counter = SpanishSyllableCounter()
        self.setup_logging()
        self.stats = {
            'total_words': 0,
            'filtered_words': 0,
            'clips_generated': 0,
            'syllable_distribution': {},
            'confidence_distribution': {},
        }
    
    def setup_logging(self):
        """Setup logging configuration"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('clip_generation.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def load_audio(self, audio_path: str) -> Tuple[np.ndarray, int]:
        """Load audio file using librosa"""
        self.logger.info(f"Loading audio: {audio_path}")
        
        if not os.path.exists(audio_path):
            raise FileNotFoundError(f"Audio file not found: {audio_path}")
        
        audio, sr = librosa.load(audio_path, sr=self.config.SAMPLE_RATE)
        
        # If in test mode, limit to first N seconds
        if self.config.TEST_MODE:
            max_samples = self.config.TEST_DURATION * sr
            audio = audio[:max_samples]
            self.logger.info(f"Test mode: Processing first {self.config.TEST_DURATION} seconds")
        
        return audio, sr
    
    def transcribe_with_whisper(self, audio_path: str) -> Dict:
        """Transcribe audio using Whisper with word-level timestamps"""
        self.logger.info(f"Loading Whisper model: {self.config.WHISPER_MODEL}")
        model = whisper.load_model(self.config.WHISPER_MODEL)
        
        self.logger.info("Starting transcription...")
        result = model.transcribe(
            audio_path,
            language='es',
            word_timestamps=True,
            verbose=False
        )
        
        # Save full transcript
        transcript_path = os.path.join(self.config.TRANSCRIPTS_DIR, 
                                     f"{Path(audio_path).stem}_transcript.json")
        os.makedirs(self.config.TRANSCRIPTS_DIR, exist_ok=True)
        
        with open(transcript_path, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        
        self.logger.info(f"Transcript saved: {transcript_path}")
        return result
    
    def filter_words(self, segments: List[Dict]) -> List[Dict]:
        """Filter words based on quality criteria"""
        filtered_words = []
        
        for segment in segments:
            if 'words' not in segment:
                continue
                
            for word_data in segment['words']:
                word = word_data.get('word', '').strip()
                confidence = word_data.get('probability', 0)
                start = word_data.get('start', 0)
                end = word_data.get('end', 0)
                
                # Skip if missing required data
                if not word or start is None or end is None:
                    continue
                
                # Clean word (remove punctuation)
                clean_word = re.sub(r'[^\w\sáéíóúüñ]', '', word).strip().lower()
                if not clean_word:
                    continue
                
                duration = end - start
                syllables = self.syllable_counter.count_syllables(clean_word)
                
                # Apply filters
                if (confidence >= self.config.MIN_CONFIDENCE and
                    self.config.MIN_DURATION <= duration <= self.config.MAX_DURATION and
                    self.config.SYLLABLE_RANGE[0] <= syllables <= self.config.SYLLABLE_RANGE[1] and
                    len(clean_word) >= 3):  # Minimum word length
                    
                    word_data['clean_word'] = clean_word
                    word_data['syllables'] = syllables
                    word_data['duration'] = duration
                    filtered_words.append(word_data)
        
        self.logger.info(f"Filtered {len(filtered_words)} words from segments")
        return filtered_words
    
    def determine_difficulty(self, syllables: int) -> str:
        """Determine difficulty level based on syllable count"""
        if syllables <= 3:
            return "beginner"
        elif syllables <= 5:
            return "intermediate"
        else:
            return "advanced"
    
    def generate_phonetic(self, word: str) -> str:
        """Generate basic phonetic representation (simplified)"""
        # This is a simplified phonetic representation
        # For production, consider using a proper Spanish phonetic library
        phonetic = word.lower()
        
        # Basic Spanish phonetic rules
        phonetic = re.sub(r'ch', 'tʃ', phonetic)
        phonetic = re.sub(r'll', 'ʎ', phonetic)
        phonetic = re.sub(r'ñ', 'ɲ', phonetic)
        phonetic = re.sub(r'rr', 'r', phonetic)
        phonetic = re.sub(r'qu', 'k', phonetic)
        phonetic = re.sub(r'c([ei])', r'θ\1', phonetic)
        phonetic = re.sub(r'z', 'θ', phonetic)
        phonetic = re.sub(r'j', 'x', phonetic)
        phonetic = re.sub(r'g([ei])', r'x\1', phonetic)
        
        # Add syllable separators (simplified)
        vowels = 'aeiouáéíóúü'
        result = ''
        for i, char in enumerate(phonetic):
            result += char
            if (i < len(phonetic) - 1 and 
                char in vowels and 
                phonetic[i+1] not in vowels):
                result += '.'
        
        return result
    
    def extract_clip(self, audio: np.ndarray, sr: int, start: float, end: float, 
                    buffer_ms: int = None) -> np.ndarray:
        """Extract audio clip with optional buffer"""
        if buffer_ms is None:
            buffer_ms = self.config.BUFFER_MS
        
        buffer_samples = int((buffer_ms / 1000) * sr)
        start_sample = max(0, int(start * sr) - buffer_samples)
        end_sample = min(len(audio), int(end * sr) + buffer_samples)
        
        return audio[start_sample:end_sample]
    
    def organize_clips(self, word_clips: List[WordClip], audio: np.ndarray, sr: int):
        """Generate and organize clips into directory structure"""
        word_instances = {}
        
        for word_data in word_clips:
            word = word_data.clean_word
            
            # Track instances of same word
            if word not in word_instances:
                word_instances[word] = 0
            word_instances[word] += 1
            
            # Create WordClip object
            clip = WordClip(
                word=word,
                syllable_count=word_data.syllables,
                confidence=word_data.get('probability', 0),
                duration_ms=int(word_data.duration * 1000),
                start_time=word_data.start,
                end_time=word_data.end,
                context=word_data.get('context', ''),
                difficulty=self.determine_difficulty(word_data.syllables),
                phonetic=self.generate_phonetic(word),
                instance_number=word_instances[word]
            )
            
            # Extract audio clip
            clip_audio = self.extract_clip(audio, sr, word_data.start, word_data.end)
            
            # Save to multiple locations
            self.save_clip_multiple_locations(clip, clip_audio, sr)
            
            self.stats['clips_generated'] += 1
            
            # Update statistics
            syllables = clip.syllable_count
            if syllables not in self.stats['syllable_distribution']:
                self.stats['syllable_distribution'][syllables] = 0
            self.stats['syllable_distribution'][syllables] += 1
    
    def save_clip_multiple_locations(self, clip: WordClip, audio_data: np.ndarray, sr: int):
        """Save clip to multiple organized locations"""
        base_dir = self.config.TEST_CLIPS_DIR if self.config.TEST_MODE else self.config.PRACTICE_CLIPS_DIR
        
        # 1. By syllables
        syllable_dir = os.path.join(base_dir, "by-syllables", f"{clip.syllable_count}-syllables")
        os.makedirs(syllable_dir, exist_ok=True)
        syllable_path = os.path.join(syllable_dir, clip.to_filename())
        sf.write(syllable_path, audio_data, sr)
        
        # 2. By word
        word_dir = os.path.join(base_dir, "by-word", clip.word)
        os.makedirs(word_dir, exist_ok=True)
        word_path = os.path.join(word_dir, clip.to_filename())
        sf.write(word_path, audio_data, sr)
        
        # Save metadata
        metadata_path = os.path.join(word_dir, "metadata.json")
        metadata = []
        if os.path.exists(metadata_path):
            with open(metadata_path, 'r', encoding='utf-8') as f:
                metadata = json.load(f)
        
        metadata.append(asdict(clip))
        with open(metadata_path, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, ensure_ascii=False, indent=2)
        
        # 3. Flashcard ready
        flashcard_dir = os.path.join(base_dir, "flashcard-ready", clip.difficulty)
        os.makedirs(flashcard_dir, exist_ok=True)
        flashcard_path = os.path.join(flashcard_dir, clip.to_filename())
        sf.write(flashcard_path, audio_data, sr)
    
    def generate_validation_report(self, word_clips: List[WordClip]) -> Dict:
        """Generate validation report for test mode"""
        report = {
            'total_clips': len(word_clips),
            'syllable_distribution': self.stats['syllable_distribution'],
            'confidence_stats': {
                'min': min(clip.confidence for clip in word_clips) if word_clips else 0,
                'max': max(clip.confidence for clip in word_clips) if word_clips else 0,
                'avg': sum(clip.confidence for clip in word_clips) / len(word_clips) if word_clips else 0
            },
            'duration_stats': {
                'min_ms': min(clip.duration_ms for clip in word_clips) if word_clips else 0,
                'max_ms': max(clip.duration_ms for clip in word_clips) if word_clips else 0,
                'avg_ms': sum(clip.duration_ms for clip in word_clips) / len(word_clips) if word_clips else 0
            },
            'unique_words': len(set(clip.word for clip in word_clips)),
            'recommendations': []
        }
        
        # Add recommendations
        if report['confidence_stats']['avg'] < 0.85:
            report['recommendations'].append("Consider increasing MIN_CONFIDENCE threshold")
        
        if report['total_clips'] < 10:
            report['recommendations'].append("Consider lowering MIN_CONFIDENCE or expanding SYLLABLE_RANGE")
        
        return report
    
    def process_audio(self, audio_file: str) -> Dict:
        """Main processing pipeline"""
        start_time = time.time()
        
        self.logger.info(f"Starting {'TEST' if self.config.TEST_MODE else 'FULL'} processing of {audio_file}")
        
        # Phase 1: Load and transcribe
        audio_path = os.path.join(self.config.VIDEO_SOURCES_DIR, audio_file)
        audio, sr = self.load_audio(audio_path)
        
        transcript = self.transcribe_with_whisper(audio_path)
        
        # Phase 2: Filter words
        filtered_words = self.filter_words(transcript['segments'])
        self.stats['total_words'] = sum(len(seg.get('words', [])) for seg in transcript['segments'])
        self.stats['filtered_words'] = len(filtered_words)
        
        # Phase 3: Generate clips (limit for test mode)
        if self.config.TEST_MODE:
            filtered_words = filtered_words[:15]  # Limit to 15 clips for testing
        
        # Add context to words
        for word_data in filtered_words:
            # Find the segment this word belongs to
            for segment in transcript['segments']:
                if 'words' in segment:
                    for w in segment['words']:
                        if (w.get('start') == word_data.get('start') and 
                            w.get('end') == word_data.get('end')):
                            word_data['context'] = segment.get('text', '').strip()
                            break
        
        self.organize_clips(filtered_words, audio, sr)
        
        # Phase 4: Generate report
        word_clips = [WordClip(
            word=wd['clean_word'],
            syllable_count=wd['syllables'],
            confidence=wd.get('probability', 0),
            duration_ms=int(wd['duration'] * 1000),
            start_time=wd['start'],
            end_time=wd['end'],
            context=wd.get('context', ''),
            difficulty=self.determine_difficulty(wd['syllables']),
            phonetic=self.generate_phonetic(wd['clean_word']),
            instance_number=1
        ) for wd in filtered_words]
        
        validation_report = self.generate_validation_report(word_clips)
        
        # Save processing report
        processing_time = time.time() - start_time
        final_report = {
            'processing_time_seconds': processing_time,
            'config': asdict(self.config),
            'statistics': self.stats,
            'validation': validation_report,
            'audio_file': audio_file,
            'test_mode': self.config.TEST_MODE
        }
        
        report_path = os.path.join(
            self.config.TEST_CLIPS_DIR if self.config.TEST_MODE else self.config.PRACTICE_CLIPS_DIR,
            'processing_report.json'
        )
        
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(final_report, f, ensure_ascii=False, indent=2)
        
        self.logger.info(f"Processing complete in {processing_time:.2f} seconds")
        self.logger.info(f"Generated {self.stats['clips_generated']} clips")
        self.logger.info(f"Report saved: {report_path}")
        
        return final_report

def main():
    """Main entry point"""
    config = Config()
    generator = AccentClipGenerator(config)
    
    # Find audio file
    audio_files = [f for f in os.listdir(config.VIDEO_SOURCES_DIR) 
                   if f.endswith(('.mp3', '.wav', '.m4a', '.flac'))]
    
    if not audio_files:
        print("No audio files found in video-sources directory")
        return
    
    audio_file = audio_files[0]  # Use first audio file found
    print(f"Processing: {audio_file}")
    
    if config.TEST_MODE:
        print("🧪 RUNNING IN TEST MODE - Processing first 5 minutes only")
        print("Review the generated clips in test-clips/ before running full processing")
    
    try:
        report = generator.process_audio(audio_file)
        
        print(f"\n✅ Processing completed successfully!")
        print(f"📊 Generated {report['statistics']['clips_generated']} clips")
        print(f"⏱️  Processing time: {report['processing_time_seconds']:.2f} seconds")
        
        if config.TEST_MODE:
            print(f"\n📁 Test clips saved to: {config.TEST_CLIPS_DIR}/")
            print("🔍 Please manually validate the clips before running full processing")
            print("💡 To run full processing, set TEST_MODE = False in the config")
        
    except Exception as e:
        print(f"❌ Error during processing: {e}")
        generator.logger.error(f"Processing failed: {e}", exc_info=True)

if __name__ == "__main__":
    main()