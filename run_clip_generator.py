#!/usr/bin/env python3
"""
Simple runner script for the Colombian Accent Clip Generator
"""

from accent_clip_generator import AccentClipGenerator, Config
import os
import sys

def run_test():
    """Run in test mode (first 5 minutes, 15 clips max)"""
    print("🧪 Running in TEST MODE")
    print("=" * 50)
    
    config = Config()
    config.TEST_MODE = True
    
    generator = AccentClipGenerator(config)
    
    # Find audio file
    audio_files = [f for f in os.listdir(config.VIDEO_SOURCES_DIR) 
                   if f.endswith(('.mp3', '.wav', '.m4a', '.flac'))]
    
    if not audio_files:
        print("❌ No audio files found in video-sources directory")
        return False
    
    audio_file = audio_files[0]
    print(f"📁 Processing: {audio_file}")
    print(f"⏱️  Duration: First {config.TEST_DURATION} seconds only")
    print(f"🔢 Max clips: 15 sample clips")
    print()
    
    try:
        report = generator.process_audio(audio_file)
        
        print("\n✅ TEST COMPLETED SUCCESSFULLY!")
        print("=" * 50)
        print(f"📊 Generated: {report['statistics']['clips_generated']} clips")
        print(f"⏱️  Time: {report['processing_time_seconds']:.2f} seconds")
        print(f"📁 Location: {config.TEST_CLIPS_DIR}/")
        print()
        print("🔍 NEXT STEPS:")
        print("1. Check clips in test-clips/ directory")
        print("2. Verify audio quality and syllable accuracy") 
        print("3. If satisfied, run: python run_clip_generator.py --full")
        
        return True
        
    except Exception as e:
        print(f"❌ Error during processing: {e}")
        return False

def run_full():
    """Run full processing"""
    print("🚀 Running FULL PROCESSING")
    print("=" * 50)
    
    config = Config()
    config.TEST_MODE = False
    
    generator = AccentClipGenerator(config)
    
    # Find audio file
    audio_files = [f for f in os.listdir(config.VIDEO_SOURCES_DIR) 
                   if f.endswith(('.mp3', '.wav', '.m4a', '.flac'))]
    
    if not audio_files:
        print("❌ No audio files found in video-sources directory")
        return False
    
    audio_file = audio_files[0]
    print(f"📁 Processing: {audio_file}")
    print(f"⏱️  Duration: Full audio file")
    print("🔄 This may take several minutes...")
    print()
    
    # Confirmation
    response = input("Continue with full processing? (y/N): ")
    if response.lower() != 'y':
        print("❌ Cancelled by user")
        return False
    
    try:
        report = generator.process_audio(audio_file)
        
        print("\n✅ FULL PROCESSING COMPLETED!")
        print("=" * 50)
        print(f"📊 Generated: {report['statistics']['clips_generated']} clips")
        print(f"⏱️  Time: {report['processing_time_seconds']:.2f} seconds")
        print(f"📁 Location: {config.PRACTICE_CLIPS_DIR}/")
        print()
        print("🎯 READY FOR FLASHCARD INTEGRATION!")
        
        return True
        
    except Exception as e:
        print(f"❌ Error during processing: {e}")
        return False

def main():
    """Main entry point with command line options"""
    if len(sys.argv) > 1 and sys.argv[1] == '--full':
        success = run_full()
    else:
        success = run_test()
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()