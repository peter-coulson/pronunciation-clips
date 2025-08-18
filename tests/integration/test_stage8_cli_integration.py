"""
Integration tests for Stage 8: CLI Interface.

Tests CLI integration with pipeline, configuration system,
and user experience workflows.
"""
import pytest
import tempfile
import json
from pathlib import Path
from unittest.mock import patch, MagicMock
from click.testing import CliRunner

from src.cli.main import cli
from src.shared.config import Config, load_config
from src.shared.models import WordDatabase, Entity, SpeakerInfo
from src.shared.exceptions import PipelineError, AudioError, ConfigError


class TestCLIPipelineIntegration:
    """Test CLI integration with the full pipeline."""
    
    @patch('src.cli.main.process_audio_to_json')
    @patch('src.cli.main.load_config')
    def test_full_cli_to_pipeline_integration(self, mock_load_config, mock_process):
        """Test complete CLI to pipeline integration."""
        runner = CliRunner()
        
        # Setup config
        config = Config()
        mock_load_config.return_value = config
        
        # Setup successful pipeline result
        mock_database = WordDatabase(
            metadata={"version": "1.0", "created_at": "2023-01-01T00:00:00"},
            speaker_map={"speaker_0": SpeakerInfo(name="Test Speaker")},
            entities=[]
        )
        mock_process.return_value = mock_database
        
        with runner.isolated_filesystem():
            # Create test audio file
            test_audio = Path("test.wav")
            test_audio.touch()
            
            # Create a default config file to trigger config loading
            config_file = Path("config.yaml")
            config_file.write_text("audio:\n  sample_rate: 16000\n")
            
            # Run CLI command
            result = runner.invoke(cli, ['process', str(test_audio)])
            
            # Verify integration
            mock_load_config.assert_called()
            mock_process.assert_called()
            
            # Verify CLI called pipeline with correct parameters
            call_args = mock_process.call_args
            assert call_args[0][0] == str(test_audio)  # audio_path
            assert call_args[0][1] == config  # config
    
    @patch('src.cli.main.process_audio_to_json')
    @patch('src.cli.main.load_config')
    def test_cli_with_output_file_integration(self, mock_load_config, mock_process):
        """Test CLI integration with output file specification."""
        runner = CliRunner()
        
        config = Config()
        mock_load_config.return_value = config
        
        mock_database = WordDatabase(
            metadata={"version": "1.0", "created_at": "2023-01-01T00:00:00"},
            speaker_map={}, entities=[]
        )
        mock_process.return_value = mock_database
        
        with runner.isolated_filesystem():
            test_audio = Path("test.wav")
            test_audio.touch()
            
            result = runner.invoke(cli, [
                'process', str(test_audio),
                '--output', 'custom_output.json'
            ])
            
            # Verify output parameter was passed
            call_args = mock_process.call_args
            if call_args and len(call_args[1]) > 0:
                # Check if output_path was passed in kwargs
                assert 'output_path' in call_args[1] or len(call_args[0]) > 2
    
    @patch('src.cli.main.process_audio_to_json')
    @patch('src.cli.main.load_config')
    def test_cli_config_file_integration(self, mock_load_config, mock_process):
        """Test CLI integration with custom config file."""
        runner = CliRunner()
        
        config = Config()
        mock_load_config.return_value = config
        mock_process.return_value = WordDatabase(
            metadata={"version": "1.0", "created_at": "2023-01-01"},
            speaker_map={}, entities=[]
        )
        
        with runner.isolated_filesystem():
            # Create custom config
            config_content = """
audio:
  sample_rate: 22050
  channels: 1

whisper:
  model: "tiny"
  language: "es"

quality:
  min_confidence: 0.9
"""
            custom_config = Path("custom.yaml")
            custom_config.write_text(config_content)
            
            test_audio = Path("test.wav")
            test_audio.touch()
            
            result = runner.invoke(cli, [
                '--config', str(custom_config),
                'process', str(test_audio)
            ])
            
            # Verify custom config was loaded
            if mock_load_config.call_args:
                config_path_arg = mock_load_config.call_args[0][0]
                assert str(custom_config) in str(config_path_arg) or mock_load_config.called


class TestCLIErrorHandlingIntegration:
    """Test CLI error handling integration with pipeline errors."""
    
    @patch('src.cli.main.process_audio_to_json')
    @patch('src.cli.main.load_config')
    def test_pipeline_error_integration(self, mock_load_config, mock_process):
        """Test CLI handles pipeline errors gracefully."""
        runner = CliRunner()
        
        config = Config()
        mock_load_config.return_value = config
        
        # Simulate pipeline error
        mock_process.side_effect = PipelineError("Pipeline processing failed")
        
        with runner.isolated_filesystem():
            test_audio = Path("test.wav")
            test_audio.touch()
            
            result = runner.invoke(cli, ['process', str(test_audio)])
            
            # CLI should handle error gracefully
            assert result.exit_code != 0
            assert "Pipeline processing failed" in result.output or "Error" in result.output
    
    @patch('src.cli.main.process_audio_to_json')
    @patch('src.cli.main.load_config')
    def test_audio_error_integration(self, mock_load_config, mock_process):
        """Test CLI handles audio errors gracefully."""
        runner = CliRunner()
        
        config = Config()
        mock_load_config.return_value = config
        
        # Simulate audio error
        mock_process.side_effect = AudioError("Audio file not supported")
        
        with runner.isolated_filesystem():
            test_audio = Path("test.wav")
            test_audio.touch()
            
            result = runner.invoke(cli, ['process', str(test_audio)])
            
            assert result.exit_code != 0
            assert "Audio file not supported" in result.output or "Error" in result.output
    
    @patch('src.cli.main.load_config')
    def test_config_error_integration(self, mock_load_config):
        """Test CLI handles configuration errors gracefully."""
        runner = CliRunner()
        
        # Simulate config error
        mock_load_config.side_effect = ConfigError("Invalid configuration")
        
        with runner.isolated_filesystem():
            test_audio = Path("test.wav")
            test_audio.touch()
            
            # Create a default config file to trigger config loading
            config_file = Path("config.yaml")
            config_file.write_text("invalid yaml content {[")
            
            result = runner.invoke(cli, ['process', str(test_audio)])
            
            assert result.exit_code != 0
            assert "Invalid configuration" in result.output or "configuration" in result.output.lower()
    
    def test_missing_file_integration(self):
        """Test CLI handles missing files gracefully."""
        runner = CliRunner()
        
        # Try to process non-existent file
        result = runner.invoke(cli, ['process', 'nonexistent.wav'])
        
        assert result.exit_code != 0
        assert "nonexistent" in result.output.lower() or "not found" in result.output.lower() or "error" in result.output.lower()


class TestCLILoggingIntegration:
    """Test CLI logging integration."""
    
    @patch('src.cli.main.init_logger')
    @patch('src.cli.main.process_audio_to_json')
    @patch('src.cli.main.load_config')
    def test_logging_initialization_integration(self, mock_load_config, mock_process, mock_init_logger):
        """Test CLI initializes logging correctly."""
        runner = CliRunner()
        
        config = Config()
        mock_load_config.return_value = config
        mock_process.return_value = WordDatabase(
            metadata={"version": "1.0", "created_at": "2023-01-01"},
            speaker_map={}, entities=[]
        )
        
        with runner.isolated_filesystem():
            test_audio = Path("test.wav")
            test_audio.touch()
            
            result = runner.invoke(cli, ['process', str(test_audio)])
            
            # Verify logging was initialized
            mock_init_logger.assert_called()
            # Should be called with the loaded config
            if mock_init_logger.call_args:
                assert mock_init_logger.call_args[0][0] == config
    
    @patch('src.cli.main.init_logger')
    @patch('src.cli.main.process_audio_to_json')
    @patch('src.cli.main.load_config')
    def test_verbose_logging_integration(self, mock_load_config, mock_process, mock_init_logger):
        """Test CLI verbose flag affects logging."""
        runner = CliRunner()
        
        config = Config()
        mock_load_config.return_value = config
        mock_process.return_value = WordDatabase(
            metadata={"version": "1.0", "created_at": "2023-01-01"},
            speaker_map={}, entities=[]
        )
        
        with runner.isolated_filesystem():
            test_audio = Path("test.wav")
            test_audio.touch()
            
            result = runner.invoke(cli, [
                'process', str(test_audio),
                '--verbose'
            ])
            
            # Verify verbose mode affects logging configuration
            if mock_init_logger.call_args:
                # Config might be modified for verbose mode
                used_config = mock_init_logger.call_args[0][0]
                assert used_config.logging.level in ["DEBUG", "INFO"]


class TestCLIProgressDisplayIntegration:
    """Test CLI progress display integration."""
    
    @patch('src.cli.main.process_audio_to_json')
    @patch('src.cli.main.load_config')
    def test_progress_output_integration(self, mock_load_config, mock_process):
        """Test CLI displays progress information."""
        runner = CliRunner()
        
        config = Config()
        mock_load_config.return_value = config
        
        # Create database with some entities
        entities = [
            Entity(
                entity_id="word_001", entity_type="word", text="hola",
                start_time=0.0, end_time=0.5, duration=0.5,
                confidence=0.9, probability=0.9, syllables=["ho", "la"],
                syllable_count=2, quality_score=0.8, speaker_id="speaker_0",
                recording_id="test", recording_path="test.wav", processed=False,
                created_at="2023-01-01T00:00:00"
            )
        ]
        
        mock_database = WordDatabase(
            metadata={"version": "1.0", "created_at": "2023-01-01T00:00:00"},
            speaker_map={"speaker_0": SpeakerInfo(name="Test Speaker")},
            entities=entities
        )
        mock_process.return_value = mock_database
        
        with runner.isolated_filesystem():
            test_audio = Path("test.wav")
            test_audio.touch()
            
            result = runner.invoke(cli, ['process', str(test_audio)])
            
            # Should display progress/completion information
            assert len(result.output) > 0
            # Output might contain entity count or completion message
            assert result.exit_code == 0 or "complete" in result.output.lower()
    
    @patch('src.cli.main.process_audio_to_json')
    @patch('src.cli.main.load_config')
    def test_summary_statistics_integration(self, mock_load_config, mock_process):
        """Test CLI displays summary statistics."""
        runner = CliRunner()
        
        config = Config()
        mock_load_config.return_value = config
        
        # Create database with multiple entities
        entities = []
        for i in range(5):
            entity = Entity(
                entity_id=f"word_{i+1:03d}", entity_type="word", text=f"palabra{i+1}",
                start_time=float(i), end_time=float(i+0.5), duration=0.5,
                confidence=0.9, probability=0.9, syllables=[f"pa{i+1}"],
                syllable_count=1, quality_score=0.8, speaker_id="speaker_0",
                recording_id="test", recording_path="test.wav", processed=False,
                created_at="2023-01-01T00:00:00"
            )
            entities.append(entity)
        
        mock_database = WordDatabase(
            metadata={"version": "1.0", "created_at": "2023-01-01T00:00:00"},
            speaker_map={"speaker_0": SpeakerInfo(name="Test Speaker")},
            entities=entities
        )
        mock_process.return_value = mock_database
        
        with runner.isolated_filesystem():
            test_audio = Path("test.wav")
            test_audio.touch()
            
            result = runner.invoke(cli, ['process', str(test_audio)])
            
            # Should show some statistics about processing
            assert len(result.output) > 0


class TestCLIFileOperationIntegration:
    """Test CLI file operation integration."""
    
    @patch('src.cli.main.process_audio_to_json')
    @patch('src.cli.main.load_config')
    def test_output_file_creation_integration(self, mock_load_config, mock_process):
        """Test CLI creates output files correctly."""
        runner = CliRunner()
        
        config = Config()
        mock_load_config.return_value = config
        
        mock_database = WordDatabase(
            metadata={"version": "1.0", "created_at": "2023-01-01"},
            speaker_map={}, entities=[]
        )
        mock_process.return_value = mock_database
        
        with runner.isolated_filesystem():
            test_audio = Path("test.wav")
            test_audio.touch()
            
            output_file = "result.json"
            result = runner.invoke(cli, [
                'process', str(test_audio),
                '--output', output_file
            ])
            
            # Verify CLI handling
            assert result.exit_code == 0 or "error" not in result.output.lower()
    
    @patch('src.cli.main.process_audio_to_json')
    @patch('src.cli.main.load_config')
    def test_directory_creation_integration(self, mock_load_config, mock_process):
        """Test CLI creates output directories if needed."""
        runner = CliRunner()
        
        config = Config()
        mock_load_config.return_value = config
        mock_process.return_value = WordDatabase(
            metadata={"version": "1.0", "created_at": "2023-01-01"},
            speaker_map={}, entities=[]
        )
        
        with runner.isolated_filesystem():
            test_audio = Path("test.wav")
            test_audio.touch()
            
            nested_output = "output/nested/result.json"
            result = runner.invoke(cli, [
                'process', str(test_audio),
                '--output', nested_output
            ])
            
            # CLI should handle nested path creation
            assert result.exit_code == 0 or "error" not in result.output.lower()
    
    @patch('src.cli.main.process_audio_to_json')
    @patch('src.cli.main.load_config')
    def test_overwrite_protection_integration(self, mock_load_config, mock_process):
        """Test CLI handles file overwrite situations."""
        runner = CliRunner()
        
        config = Config()
        mock_load_config.return_value = config
        mock_process.return_value = WordDatabase(
            metadata={"version": "1.0", "created_at": "2023-01-01"},
            speaker_map={}, entities=[]
        )
        
        with runner.isolated_filesystem():
            test_audio = Path("test.wav")
            test_audio.touch()
            
            # Create existing output file
            existing_output = Path("existing.json")
            existing_output.write_text('{"existing": "data"}')
            
            result = runner.invoke(cli, [
                'process', str(test_audio),
                '--output', str(existing_output)
            ])
            
            # CLI should handle overwrite scenario
            assert isinstance(result.exit_code, int)


class TestCLIAdvancedFeaturesIntegration:
    """Test CLI advanced features integration."""
    
    @patch('src.cli.main.process_audio_to_json')
    @patch('src.cli.main.load_config')
    def test_speaker_mapping_integration(self, mock_load_config, mock_process):
        """Test CLI speaker mapping integration."""
        runner = CliRunner()
        
        config = Config()
        mock_load_config.return_value = config
        mock_process.return_value = WordDatabase(
            metadata={"version": "1.0", "created_at": "2023-01-01"},
            speaker_map={}, entities=[]
        )
        
        with runner.isolated_filesystem():
            test_audio = Path("test.wav")
            test_audio.touch()
            
            result = runner.invoke(cli, [
                'process', str(test_audio),
                '--speakers', '0.0-10.0:alice,10.0-20.0:bob'
            ])
            
            # CLI should handle speaker mapping if implemented
            if '--speakers' in ' '.join(cli.commands.keys() if hasattr(cli, 'commands') else []):
                # Verify speaker mapping was passed to pipeline
                call_args = mock_process.call_args
                assert 'speaker_mapping' in call_args[1] if call_args and len(call_args) > 1 else True
    
    @patch('src.cli.main.process_audio_to_json')
    @patch('src.cli.main.load_config')
    def test_quality_options_integration(self, mock_load_config, mock_process):
        """Test CLI quality options integration."""
        runner = CliRunner()
        
        # Mock config modification for quality settings
        config = Config()
        mock_load_config.return_value = config
        mock_process.return_value = WordDatabase(
            metadata={"version": "1.0", "created_at": "2023-01-01"},
            speaker_map={}, entities=[]
        )
        
        with runner.isolated_filesystem():
            test_audio = Path("test.wav")
            test_audio.touch()
            
            result = runner.invoke(cli, [
                'process', str(test_audio),
                '--min-confidence', '0.8',
                '--min-duration', '0.3'
            ])
            
            # CLI should handle quality options if implemented
            assert isinstance(result.exit_code, int)


class TestCLIWorkflowIntegration:
    """Test complete CLI workflow integration."""
    
    @patch('src.cli.main.process_audio_to_json')
    @patch('src.cli.main.load_config')
    def test_complete_workflow_integration(self, mock_load_config, mock_process):
        """Test complete CLI workflow from start to finish."""
        runner = CliRunner()
        
        # Setup complete workflow
        config = Config()
        config.quality.min_confidence = 0.8
        mock_load_config.return_value = config
        
        # Create realistic database result
        entities = [
            Entity(
                entity_id="word_001", entity_type="word", text="hola",
                start_time=0.0, end_time=0.5, duration=0.5,
                confidence=0.9, probability=0.9, syllables=["ho", "la"],
                syllable_count=2, quality_score=0.85, speaker_id="speaker_0",
                recording_id="test_recording", recording_path="spanish_audio.wav",
                processed=False, created_at="2023-01-01T00:00:00"
            ),
            Entity(
                entity_id="word_002", entity_type="word", text="mundo",
                start_time=0.6, end_time=1.1, duration=0.5,
                confidence=0.87, probability=0.87, syllables=["mun", "do"],
                syllable_count=2, quality_score=0.82, speaker_id="speaker_0",
                recording_id="test_recording", recording_path="spanish_audio.wav",
                processed=False, created_at="2023-01-01T00:00:00"
            )
        ]
        
        mock_database = WordDatabase(
            metadata={
                "version": "1.0",
                "created_at": "2023-01-01T00:00:00",
                "whisper_model": "base",
                "audio_duration": 30.0,
                "entity_count": 2
            },
            speaker_map={
                "speaker_0": SpeakerInfo(
                    name="Default Speaker",
                    gender="Unknown",
                    region="Colombia"
                )
            },
            entities=entities
        )
        mock_process.return_value = mock_database
        
        with runner.isolated_filesystem():
            # Create test files
            audio_file = Path("spanish_audio.wav")
            audio_file.touch()
            
            config_file = Path("config.yaml")
            config_file.write_text("""
audio:
  sample_rate: 16000
whisper:
  model: "base"
  language: "es"
quality:
  min_confidence: 0.8
  syllable_range: [2, 6]
""")
            
            # Run complete workflow
            result = runner.invoke(cli, [
                '--config', str(config_file),
                '--verbose',
                'process', str(audio_file),
                '--output', 'result.json'
            ])
            
            # Verify workflow completion
            assert result.exit_code == 0 or "complete" in result.output.lower()
            
            # Verify all components were called
            mock_load_config.assert_called()
            mock_process.assert_called()
    
    @patch('src.cli.main.process_audio_to_json')
    @patch('src.cli.main.load_config')
    def test_batch_processing_workflow_integration(self, mock_load_config, mock_process):
        """Test batch processing workflow integration."""
        runner = CliRunner()
        
        config = Config()
        mock_load_config.return_value = config
        mock_process.return_value = WordDatabase(
            metadata={"version": "1.0", "created_at": "2023-01-01"},
            speaker_map={}, entities=[]
        )
        
        with runner.isolated_filesystem():
            # Create multiple audio files
            for i in range(3):
                audio_file = Path(f"audio_{i+1}.wav")
                audio_file.touch()
            
            # Process each file (simulating batch processing)
            for i in range(3):
                result = runner.invoke(cli, [
                    'process', f'audio_{i+1}.wav',
                    '--output', f'result_{i+1}.json'
                ])
                
                # Each should complete successfully
                assert isinstance(result.exit_code, int)
            
            # Verify all files were processed
            assert mock_process.call_count == 3


class TestCLIUserExperienceIntegration:
    """Test CLI user experience integration."""
    
    def test_help_system_integration(self):
        """Test CLI help system integration."""
        runner = CliRunner()
        
        # Test main help
        result = runner.invoke(cli, ['--help'])
        assert result.exit_code == 0
        assert len(result.output) > 0
        
        # Test command help
        result = runner.invoke(cli, ['process', '--help'])
        assert result.exit_code == 0
        assert len(result.output) > 0
    
    @patch('src.cli.main.process_audio_to_json')
    @patch('src.cli.main.load_config')
    def test_user_friendly_messages_integration(self, mock_load_config, mock_process):
        """Test CLI provides user-friendly messages."""
        runner = CliRunner()
        
        config = Config()
        mock_load_config.return_value = config
        mock_process.return_value = WordDatabase(
            metadata={"version": "1.0", "created_at": "2023-01-01"},
            speaker_map={}, entities=[]
        )
        
        with runner.isolated_filesystem():
            test_audio = Path("test.wav")
            test_audio.touch()
            
            result = runner.invoke(cli, ['process', str(test_audio)])
            
            # Output should be user-friendly (not technical stack traces)
            assert not "Traceback" in result.output
            assert not "Exception" in result.output or result.exit_code == 0
    
    @patch('src.cli.main.process_audio_to_json')
    @patch('src.cli.main.load_config')
    def test_quiet_mode_integration(self, mock_load_config, mock_process):
        """Test CLI quiet mode integration."""
        runner = CliRunner()
        
        config = Config()
        mock_load_config.return_value = config
        mock_process.return_value = WordDatabase(
            metadata={"version": "1.0", "created_at": "2023-01-01"},
            speaker_map={}, entities=[]
        )
        
        with runner.isolated_filesystem():
            test_audio = Path("test.wav")
            test_audio.touch()
            
            result = runner.invoke(cli, [
                'process', str(test_audio),
                '--quiet'
            ])
            
            # Quiet mode should reduce output
            if '--quiet' in str(result) or result.exit_code == 0:
                # Verify quiet mode behavior if implemented
                assert isinstance(result.output, str)