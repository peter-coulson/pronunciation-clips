"""
Create standardized test audio files for E2E testing

This script creates synthetic audio files with known characteristics.
These should be replaced with real Spanish audio for actual testing.
"""
import numpy as np
import soundfile as sf
import librosa
from pathlib import Path


def create_test_audio_fixtures():
    """Generate test audio files with known characteristics"""
    
    fixtures_dir = Path("tests/fixtures")
    fixtures_dir.mkdir(exist_ok=True)
    
    # Generate 30-second test audio (sine wave with varying frequency)
    sample_rate_16k = 16000
    sample_rate_44k = 44100
    duration = 30.0
    
    # Create a more complex signal (multiple frequencies to simulate speech-like patterns)
    t_16k = np.linspace(0, duration, int(sample_rate_16k * duration), False)
    t_44k = np.linspace(0, duration, int(sample_rate_44k * duration), False)
    
    # Create speech-like signal with multiple frequency components
    def create_speech_like_signal(t, base_freq=200):
        """Create a more realistic speech-like signal"""
        # Fundamental frequency (simulates voice pitch)
        fundamental = np.sin(2 * np.pi * base_freq * t)
        # Add harmonics (simulates speech formants)
        harmonic2 = 0.5 * np.sin(2 * np.pi * base_freq * 2 * t)
        harmonic3 = 0.3 * np.sin(2 * np.pi * base_freq * 3 * t)
        # Add some noise for realism
        noise = 0.1 * np.random.normal(0, 1, len(t))
        # Combine and normalize
        signal = fundamental + harmonic2 + harmonic3 + noise
        return 0.1 * signal / np.max(np.abs(signal))
    
    # Generate 16kHz version
    audio_16khz = create_speech_like_signal(t_16k, base_freq=150)
    sf.write(fixtures_dir / "spanish_30sec_16khz.wav", audio_16khz, sample_rate_16k)
    
    # Generate 44.1kHz version
    audio_44khz = create_speech_like_signal(t_44k, base_freq=150)
    sf.write(fixtures_dir / "spanish_30sec_44khz.wav", audio_44khz, sample_rate_44k)
    
    # Create clear version (same as 16khz)
    sf.write(fixtures_dir / "spanish_clear_30sec.wav", audio_16khz, sample_rate_16k)
    
    # Create noisy version (add more noise)
    noisy_audio = audio_16khz + 0.05 * np.random.normal(0, 1, len(audio_16khz))
    sf.write(fixtures_dir / "spanish_noisy_30sec.wav", noisy_audio, sample_rate_16k)
    
    # Create quiet version (reduce amplitude)
    quiet_audio = 0.3 * audio_16khz
    sf.write(fixtures_dir / "spanish_quiet_30sec.wav", quiet_audio, sample_rate_16k)
    
    # Create longer test file (2-3 minutes for full pipeline testing)
    duration_long = 120.0  # 2 minutes
    t_long = np.linspace(0, duration_long, int(sample_rate_16k * duration_long), False)
    audio_long = create_speech_like_signal(t_long, base_freq=180)
    sf.write(fixtures_dir / "spanish_complete_test.wav", audio_long, sample_rate_16k)
    
    print("✅ Test audio fixtures created:")
    print(f"  - {fixtures_dir / 'spanish_30sec_16khz.wav'} (16kHz, 30s)")
    print(f"  - {fixtures_dir / 'spanish_30sec_44khz.wav'} (44.1kHz, 30s)")
    print(f"  - {fixtures_dir / 'spanish_clear_30sec.wav'} (clear, 30s)")
    print(f"  - {fixtures_dir / 'spanish_noisy_30sec.wav'} (noisy, 30s)")
    print(f"  - {fixtures_dir / 'spanish_quiet_30sec.wav'} (quiet, 30s)")
    print(f"  - {fixtures_dir / 'spanish_complete_test.wav'} (long, 2min)")
    print()
    print("⚠️  IMPORTANT: Replace these synthetic files with real Spanish audio samples")
    print("   for proper testing of the transcription pipeline!")


if __name__ == "__main__":
    create_test_audio_fixtures()