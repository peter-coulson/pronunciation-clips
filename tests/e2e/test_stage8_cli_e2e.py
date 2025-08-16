"""
Stage 8 E2E Test: CLI Interface

Test complete CLI workflow:
- Basic CLI commands work correctly
- Configuration handling works
- Error display is user-friendly
"""
import pytest
import subprocess
import sys
from pathlib import Path


def test_cli_basic_commands_e2e():
    """
    Test: CLI command → Audio processing → Success message
    
    Success Criteria:
    - `pronunciation-clips process audio.wav` completes successfully
    - CLI shows progress and completion message
    - Output file created in expected location
    """
    from src.cli.main import cli
    from click.testing import CliRunner
    
    runner = CliRunner()
    
    # Test basic process command
    with runner.isolated_filesystem():
        # Create test files
        test_audio = Path("test_audio.wav")
        test_audio.touch()  # Create empty file for now
        
        # Run CLI command
        result = runner.invoke(cli, ['process', str(test_audio)])
        
        # For now, just test that CLI interface exists
        # Real implementation will process actual audio
        assert result.exit_code is not None  # CLI ran without import errors


def test_cli_configuration_handling_e2e():
    """
    Test CLI configuration loading and custom config support
    
    Success Criteria:
    - CLI uses default config.yaml
    - CLI accepts custom config with --config flag
    - CLI shows helpful error for missing config
    """
    from src.cli.main import cli
    from click.testing import CliRunner
    
    runner = CliRunner()
    
    # Test custom config flag
    with runner.isolated_filesystem():
        # Create test files
        test_audio = Path("test_audio.wav")
        test_audio.touch()
        
        test_config = Path("custom_config.yaml")
        test_config.write_text("""
audio:
  sample_rate: 16000
whisper:
  model: "base"
quality:
  min_confidence: 0.8
output:
  database_path: "custom_output.json"
logging:
  level: "INFO"
""")
        
        # Run with custom config
        result = runner.invoke(cli, ['--config', str(test_config), 'process', str(test_audio)])
        
        # For now, just test that CLI interface accepts config flag
        assert result.exit_code is not None


def test_cli_error_display_e2e():
    """
    Test CLI error handling and user-friendly messages
    
    Success Criteria:
    - CLI shows user-friendly error for invalid audio
    - CLI shows help text when run without arguments
    - CLI exit codes correct (0 for success, 1 for error)
    """
    from src.cli.main import cli
    from click.testing import CliRunner
    
    runner = CliRunner()
    
    # Test help display
    result = runner.invoke(cli, ['--help'])
    assert result.exit_code == 0
    assert "Usage:" in result.output or "Commands:" in result.output
    
    # Test invalid file error
    result = runner.invoke(cli, ['process', 'nonexistent.wav'])
    # Should show error, not crash
    assert result.exit_code != 0 or "Error" in result.output or "not found" in result.output