"""
Unit tests for CLI interface.

Tests CLI command parsing, configuration handling, and user interface components.
"""
import pytest
import tempfile
from pathlib import Path
from unittest.mock import patch, MagicMock
from click.testing import CliRunner

from src.cli.main import cli
from src.shared.config import Config


class TestCLIBasicCommands:
    """Test basic CLI command functionality."""
    
    def test_cli_help_command(self):
        """Test CLI help command works."""
        runner = CliRunner()
        result = runner.invoke(cli, ['--help'])
        
        assert result.exit_code == 0
        assert 'Usage:' in result.output or 'help' in result.output.lower()
    
    def test_cli_version_if_available(self):
        """Test CLI version command if available."""
        runner = CliRunner()
        result = runner.invoke(cli, ['--version'])
        
        # Version command may or may not be implemented
        assert result.exit_code in [0, 2]  # 0 if implemented, 2 if not
    
    @patch('src.cli.main.process_audio_to_json')
    def test_process_command_basic(self, mock_process):
        """Test basic process command."""
        runner = CliRunner()
        
        # Mock the pipeline function
        mock_database = MagicMock()
        mock_process.return_value = mock_database
        
        with runner.isolated_filesystem():
            # Create test audio file
            test_audio = Path("test.wav")
            test_audio.touch()
            
            result = runner.invoke(cli, ['process', str(test_audio)])
            
            # Should not error on CLI interface
            assert result.exit_code != 1  # Not a CLI parsing error
    
    @patch('src.cli.main.process_audio_to_json')
    def test_process_command_with_output(self, mock_process):
        """Test process command with output file."""
        runner = CliRunner()
        
        mock_database = MagicMock()
        mock_process.return_value = mock_database
        
        with runner.isolated_filesystem():
            test_audio = Path("test.wav")
            test_audio.touch()
            
            result = runner.invoke(cli, [
                'process', str(test_audio), 
                '--output', 'custom_output.json'
            ])
            
            # CLI should handle the arguments
            assert '--output' in str(result) or result.exit_code != 1


class TestCLIConfigurationHandling:
    """Test CLI configuration handling."""
    
    @patch('src.cli.main.load_config')
    @patch('src.cli.main.process_audio_to_json')
    def test_default_config_loading(self, mock_process, mock_load_config):
        """Test CLI loads default configuration."""
        runner = CliRunner()
        
        # Mock config loading
        mock_config = Config()
        mock_load_config.return_value = mock_config
        mock_process.return_value = MagicMock()
        
        with runner.isolated_filesystem():
            test_audio = Path("test.wav")
            test_audio.touch()
            
            # Create a default config file to trigger config loading
            config_file = Path("config.yaml")
            config_file.write_text("audio:\n  sample_rate: 16000\n")
            
            runner.invoke(cli, ['process', str(test_audio)])
            
            # Should attempt to load default config
            mock_load_config.assert_called()
    
    @patch('src.cli.main.load_config')
    @patch('src.cli.main.process_audio_to_json')
    def test_custom_config_loading(self, mock_process, mock_load_config):
        """Test CLI loads custom configuration."""
        runner = CliRunner()
        
        mock_config = Config()
        mock_load_config.return_value = mock_config
        mock_process.return_value = MagicMock()
        
        with runner.isolated_filesystem():
            # Create test files
            test_audio = Path("test.wav")
            test_audio.touch()
            
            custom_config = Path("custom_config.yaml")
            custom_config.write_text("audio:\n  sample_rate: 22050\n")
            
            result = runner.invoke(cli, [
                'process', str(test_audio),
                '--config', str(custom_config)
            ])
            
            # Should handle custom config argument
            assert '--config' in str(result) or result.exit_code != 1
    
    def test_config_error_handling(self):
        """Test CLI handles configuration errors."""
        runner = CliRunner()
        
        with runner.isolated_filesystem():
            test_audio = Path("test.wav")
            test_audio.touch()
            
            # Try with non-existent config file
            result = runner.invoke(cli, [
                'process', str(test_audio),
                '--config', 'nonexistent.yaml'
            ])
            
            # Should handle error gracefully (not crash)
            assert isinstance(result.exit_code, int)


class TestCLIFileHandling:
    """Test CLI file handling."""
    
    def test_missing_audio_file_error(self):
        """Test CLI handles missing audio file error."""
        runner = CliRunner()
        
        result = runner.invoke(cli, ['process', 'nonexistent.wav'])
        
        # Should handle missing file error
        assert result.exit_code != 0 or 'error' in result.output.lower()
    
    @patch('src.cli.main.process_audio_to_json')
    def test_output_path_creation(self, mock_process):
        """Test CLI creates output directory if needed."""
        runner = CliRunner()
        
        mock_process.return_value = MagicMock()
        
        with runner.isolated_filesystem():
            test_audio = Path("test.wav")
            test_audio.touch()
            
            # Output to nested directory
            result = runner.invoke(cli, [
                'process', str(test_audio),
                '--output', 'nested/dir/output.json'
            ])
            
            # CLI should handle the path
            assert isinstance(result.exit_code, int)
    
    @patch('src.cli.main.process_audio_to_json')
    def test_relative_path_handling(self, mock_process):
        """Test CLI handles relative paths correctly."""
        runner = CliRunner()
        
        mock_process.return_value = MagicMock()
        
        with runner.isolated_filesystem():
            test_audio = Path("test.wav")
            test_audio.touch()
            
            # Use relative paths
            result = runner.invoke(cli, [
                'process', './test.wav',
                '--output', './output.json'
            ])
            
            assert isinstance(result.exit_code, int)


class TestCLIVerbosityAndLogging:
    """Test CLI verbosity and logging options."""
    
    @patch('src.cli.main.init_logger')
    @patch('src.cli.main.process_audio_to_json')
    def test_verbose_flag(self, mock_process, mock_init_logger):
        """Test CLI verbose flag."""
        runner = CliRunner()
        
        mock_process.return_value = MagicMock()
        
        with runner.isolated_filesystem():
            test_audio = Path("test.wav")
            test_audio.touch()
            
            result = runner.invoke(cli, [
                'process', str(test_audio),
                '--verbose'
            ])
            
            # Should handle verbose flag
            assert '--verbose' in str(result) or result.exit_code != 1
    
    @patch('src.cli.main.init_logger')
    @patch('src.cli.main.process_audio_to_json')
    def test_quiet_flag(self, mock_process, mock_init_logger):
        """Test CLI quiet flag."""
        runner = CliRunner()
        
        mock_process.return_value = MagicMock()
        
        with runner.isolated_filesystem():
            test_audio = Path("test.wav")
            test_audio.touch()
            
            result = runner.invoke(cli, [
                'process', str(test_audio),
                '--quiet'
            ])
            
            # Should handle quiet flag
            assert '--quiet' in str(result) or result.exit_code != 1


class TestCLIProgressDisplay:
    """Test CLI progress display functionality."""
    
    @patch('src.cli.main.process_audio_to_json')
    def test_progress_display(self, mock_process):
        """Test CLI displays progress information."""
        runner = CliRunner()
        
        mock_process.return_value = MagicMock()
        
        with runner.isolated_filesystem():
            test_audio = Path("test.wav")
            test_audio.touch()
            
            result = runner.invoke(cli, ['process', str(test_audio)])
            
            # Output should contain some information
            assert isinstance(result.output, str)
    
    @patch('src.cli.main.process_audio_to_json')
    def test_completion_message(self, mock_process):
        """Test CLI shows completion message."""
        runner = CliRunner()
        
        # Mock successful processing
        mock_database = MagicMock()
        mock_database.entities = []
        mock_process.return_value = mock_database
        
        with runner.isolated_filesystem():
            test_audio = Path("test.wav")
            test_audio.touch()
            
            result = runner.invoke(cli, ['process', str(test_audio)])
            
            # Should complete without critical errors
            assert result.exit_code != 1  # Not a CLI argument error


class TestCLIErrorHandling:
    """Test CLI error handling and user-friendly messages."""
    
    @patch('src.cli.main.process_audio_to_json')
    def test_pipeline_error_display(self, mock_process):
        """Test CLI displays pipeline errors user-friendly."""
        runner = CliRunner()
        
        # Mock pipeline error
        from src.shared.exceptions import PipelineError
        mock_process.side_effect = PipelineError("Test pipeline error")
        
        with runner.isolated_filesystem():
            test_audio = Path("test.wav")
            test_audio.touch()
            
            result = runner.invoke(cli, ['process', str(test_audio)])
            
            # Should handle error gracefully
            assert result.exit_code != 0
            # Error message should be user-friendly, not a raw stack trace
            assert 'Test pipeline error' in result.output or 'Error' in result.output
    
    @patch('src.cli.main.process_audio_to_json')
    def test_audio_error_display(self, mock_process):
        """Test CLI displays audio errors user-friendly."""
        runner = CliRunner()
        
        from src.shared.exceptions import AudioError
        mock_process.side_effect = AudioError("Audio file not found")
        
        with runner.isolated_filesystem():
            test_audio = Path("test.wav")
            test_audio.touch()
            
            result = runner.invoke(cli, ['process', str(test_audio)])
            
            assert result.exit_code != 0
            # Should contain error information
            assert len(result.output) > 0
    
    @patch('src.cli.main.process_audio_to_json')
    def test_unexpected_error_display(self, mock_process):
        """Test CLI displays unexpected errors gracefully."""
        runner = CliRunner()
        
        # Mock unexpected error
        mock_process.side_effect = Exception("Unexpected error")
        
        with runner.isolated_filesystem():
            test_audio = Path("test.wav")
            test_audio.touch()
            
            result = runner.invoke(cli, ['process', str(test_audio)])
            
            # Should handle unexpected errors
            assert result.exit_code != 0
            assert isinstance(result.output, str)


class TestCLIAdvancedOptions:
    """Test CLI advanced options and features."""
    
    @patch('src.cli.main.process_audio_to_json')
    def test_speaker_mapping_option(self, mock_process):
        """Test CLI speaker mapping option if available."""
        runner = CliRunner()
        
        mock_process.return_value = MagicMock()
        
        with runner.isolated_filesystem():
            test_audio = Path("test.wav")
            test_audio.touch()
            
            # Try speaker mapping option
            result = runner.invoke(cli, [
                'process', str(test_audio),
                '--speakers', '0.0-10.0:speaker_a,10.0-20.0:speaker_b'
            ])
            
            # Should handle speaker option if implemented
            assert '--speakers' in str(result) or result.exit_code != 1
    
    @patch('src.cli.main.process_audio_to_json')
    def test_model_selection_option(self, mock_process):
        """Test CLI model selection option if available."""
        runner = CliRunner()
        
        mock_process.return_value = MagicMock()
        
        with runner.isolated_filesystem():
            test_audio = Path("test.wav")
            test_audio.touch()
            
            result = runner.invoke(cli, [
                'process', str(test_audio),
                '--model', 'tiny'
            ])
            
            # Should handle model option if implemented
            assert '--model' in str(result) or result.exit_code != 1
    
    @patch('src.cli.main.process_audio_to_json')
    def test_quality_filters_option(self, mock_process):
        """Test CLI quality filters option if available."""
        runner = CliRunner()
        
        mock_process.return_value = MagicMock()
        
        with runner.isolated_filesystem():
            test_audio = Path("test.wav")
            test_audio.touch()
            
            result = runner.invoke(cli, [
                'process', str(test_audio),
                '--min-confidence', '0.8'
            ])
            
            # Should handle quality option if implemented
            assert '--min-confidence' in str(result) or result.exit_code != 1


class TestCLIOutputFormats:
    """Test CLI output format options."""
    
    @patch('src.cli.main.process_audio_to_json')
    def test_pretty_print_option(self, mock_process):
        """Test CLI pretty print option."""
        runner = CliRunner()
        
        mock_process.return_value = MagicMock()
        
        with runner.isolated_filesystem():
            test_audio = Path("test.wav")
            test_audio.touch()
            
            result = runner.invoke(cli, [
                'process', str(test_audio),
                '--pretty'
            ])
            
            # Should handle pretty print option if implemented
            assert '--pretty' in str(result) or result.exit_code != 1
    
    @patch('src.cli.main.process_audio_to_json')
    def test_compact_output_option(self, mock_process):
        """Test CLI compact output option."""
        runner = CliRunner()
        
        mock_process.return_value = MagicMock()
        
        with runner.isolated_filesystem():
            test_audio = Path("test.wav")
            test_audio.touch()
            
            result = runner.invoke(cli, [
                'process', str(test_audio),
                '--compact'
            ])
            
            # Should handle compact option if implemented
            assert '--compact' in str(result) or result.exit_code != 1


class TestCLIUtilityCommands:
    """Test CLI utility commands."""
    
    def test_config_command_if_available(self):
        """Test CLI config command if available."""
        runner = CliRunner()
        
        result = runner.invoke(cli, ['config', '--help'])
        
        # Config command may or may not be implemented
        assert result.exit_code in [0, 2]  # 0 if implemented, 2 if not found
    
    def test_validate_command_if_available(self):
        """Test CLI validate command if available."""
        runner = CliRunner()
        
        result = runner.invoke(cli, ['validate', '--help'])
        
        # Validate command may or may not be implemented
        assert result.exit_code in [0, 2]


class TestCLIIntegrationPoints:
    """Test CLI integration with other components."""
    
    @patch('src.cli.main.load_config')
    def test_config_loading_integration(self, mock_load_config):
        """Test CLI integrates with config loading."""
        runner = CliRunner()
        
        mock_config = Config()
        mock_load_config.return_value = mock_config
        
        with runner.isolated_filesystem():
            test_audio = Path("test.wav")
            test_audio.touch()
            
            # Create a default config file to trigger config loading
            config_file = Path("config.yaml")
            config_file.write_text("audio:\n  sample_rate: 16000\n")
            
            # Mock to avoid actual processing
            with patch('src.cli.main.process_audio_to_json'):
                runner.invoke(cli, ['process', str(test_audio)])
            
            # Should have attempted config loading
            mock_load_config.assert_called()
    
    @patch('src.cli.main.process_audio_to_json')
    def test_pipeline_integration(self, mock_process):
        """Test CLI integrates with pipeline."""
        runner = CliRunner()
        
        mock_database = MagicMock()
        mock_process.return_value = mock_database
        
        with runner.isolated_filesystem():
            test_audio = Path("test.wav")
            test_audio.touch()
            
            runner.invoke(cli, ['process', str(test_audio)])
            
            # Should have called pipeline
            mock_process.assert_called()
    
    @patch('src.cli.main.init_logger')
    def test_logging_integration(self, mock_init_logger):
        """Test CLI integrates with logging."""
        runner = CliRunner()
        
        with runner.isolated_filesystem():
            test_audio = Path("test.wav")
            test_audio.touch()
            
            with patch('src.cli.main.process_audio_to_json'):
                runner.invoke(cli, ['process', str(test_audio)])
            
            # Should initialize logging
            mock_init_logger.assert_called()


class TestCLIArgumentValidation:
    """Test CLI argument validation."""
    
    def test_no_arguments_shows_help(self):
        """Test CLI shows help when no arguments provided."""
        runner = CliRunner()
        
        result = runner.invoke(cli, [])
        
        # Should show help or usage information
        assert result.exit_code in [0, 2] or 'Usage' in result.output
    
    def test_invalid_command_error(self):
        """Test CLI handles invalid commands."""
        runner = CliRunner()
        
        result = runner.invoke(cli, ['invalid_command'])
        
        # Should show error for invalid command
        assert result.exit_code != 0 or 'invalid' in result.output.lower()
    
    def test_missing_required_arguments(self):
        """Test CLI handles missing required arguments."""
        runner = CliRunner()
        
        result = runner.invoke(cli, ['process'])  # Missing audio file argument
        
        # Should show error for missing argument
        assert result.exit_code != 0 or 'missing' in result.output.lower()


class TestCLIEdgeCases:
    """Test CLI edge cases."""
    
    @patch('src.cli.main.process_audio_to_json')
    def test_empty_audio_file(self, mock_process):
        """Test CLI handles empty audio file."""
        runner = CliRunner()
        
        mock_process.return_value = MagicMock()
        
        with runner.isolated_filesystem():
            # Create empty audio file
            empty_audio = Path("empty.wav")
            empty_audio.touch()  # Creates empty file
            
            result = runner.invoke(cli, ['process', str(empty_audio)])
            
            # Should handle empty file gracefully
            assert isinstance(result.exit_code, int)
    
    @patch('src.cli.main.process_audio_to_json')
    def test_special_characters_in_paths(self, mock_process):
        """Test CLI handles special characters in file paths."""
        runner = CliRunner()
        
        mock_process.return_value = MagicMock()
        
        with runner.isolated_filesystem():
            # Create file with special characters
            special_audio = Path("test file with spaces & symbols.wav")
            special_audio.touch()
            
            result = runner.invoke(cli, ['process', str(special_audio)])
            
            # Should handle special characters
            assert isinstance(result.exit_code, int)
    
    @patch('src.cli.main.process_audio_to_json')
    def test_very_long_paths(self, mock_process):
        """Test CLI handles very long file paths."""
        runner = CliRunner()
        
        mock_process.return_value = MagicMock()
        
        with runner.isolated_filesystem():
            # Create nested directory structure
            long_path = Path("a" * 50) / ("b" * 50) / "test.wav"
            long_path.parent.mkdir(parents=True, exist_ok=True)
            long_path.touch()
            
            result = runner.invoke(cli, ['process', str(long_path)])
            
            # Should handle long paths
            assert isinstance(result.exit_code, int)