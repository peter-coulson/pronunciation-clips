"""
Main CLI interface for pronunciation clip generator.

Provides command-line interface for processing Spanish audio files into
pronunciation clips with configurable parameters and user-friendly output.
"""
import sys
import click
import logging
from pathlib import Path
from typing import Optional

from ..shared.config import load_config, Config
from ..shared.exceptions import (
    ConfigError, AudioError, TranscriptionError, 
    EntityError, DatabaseError, PipelineError
)
from ..shared.logging_config import init_logger
from ..audio_to_json.pipeline import process_audio_to_json


@click.group()
@click.option('--config', '-c', 
              type=click.Path(exists=True, path_type=Path),
              help='Path to custom configuration file')
@click.option('--verbose', '-v', is_flag=True, help='Enable verbose output')
@click.option('--quiet', '-q', is_flag=True, help='Suppress non-error output')
@click.pass_context
def cli(ctx, config: Optional[Path], verbose: bool, quiet: bool):
    """
    Spanish Pronunciation Clip Generator
    
    Process Spanish audio files to extract word-level pronunciation clips
    with smart buffering optimized for Colombian Spanish continuous speech.
    """
    # Ensure context object exists
    ctx.ensure_object(dict)
    
    # Set up logging level
    if quiet:
        log_level = logging.ERROR
    elif verbose:
        log_level = logging.DEBUG
    else:
        log_level = logging.INFO
    
    # Store CLI options in context
    ctx.obj['verbose'] = verbose
    ctx.obj['quiet'] = quiet
    ctx.obj['log_level'] = log_level
    
    # Load configuration
    try:
        if config:
            ctx.obj['config'] = load_config(str(config))
            if not quiet:
                click.echo(f"Using config: {config}")
        else:
            # Try to load default config
            default_config = Path("config.yaml")
            if default_config.exists():
                ctx.obj['config'] = load_config(str(default_config))
                if verbose:
                    click.echo(f"Using default config: {default_config}")
            else:
                # Use default configuration
                ctx.obj['config'] = Config()
                if verbose:
                    click.echo("Using built-in default configuration")
                    
        # Set up logging with config
        init_logger(ctx.obj['config'])
        
    except ConfigError as e:
        click.echo(f"Configuration error: {e}", err=True)
        sys.exit(1)
    except Exception as e:
        click.echo(f"Error loading configuration: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.argument('audio_file', type=click.Path(exists=True, path_type=Path))
@click.option('--output', '-o', 
              type=click.Path(path_type=Path),
              help='Output JSON file path (default: auto-generated)')
@click.option('--speaker-map', '-s',
              type=click.Path(exists=True, path_type=Path),
              help='JSON file with speaker time mappings')
@click.option('--resume-from', 
              type=click.Choice(['transcription', 'entities', 'database']),
              help='Resume processing from specific stage')
@click.pass_context
def process(ctx, audio_file: Path, output: Optional[Path], 
           speaker_map: Optional[Path], resume_from: Optional[str]):
    """
    Process an audio file to extract pronunciation clips.
    
    AUDIO_FILE: Path to Spanish audio file (.wav, .mp3, .m4a, .flac)
    
    Examples:
        pronunciation-clips process audio.wav
        pronunciation-clips process audio.wav --output results.json
        pronunciation-clips process audio.wav --speaker-map speakers.json
    """
    config = ctx.obj['config']
    verbose = ctx.obj['verbose']
    quiet = ctx.obj['quiet']
    
    try:
        if not quiet:
            click.echo(f"Processing: {audio_file}")
            if verbose:
                click.echo(f"  Model: {config.whisper.model}")
                click.echo(f"  Min confidence: {config.quality.min_confidence}")
                click.echo(f"  Syllable range: {config.quality.syllable_range}")
        
        # Load speaker mapping if provided
        speaker_mapping = None
        if speaker_map:
            try:
                import json
                with open(speaker_map, 'r') as f:
                    speaker_mapping = json.load(f)
                if verbose:
                    click.echo(f"  Speaker mapping: {len(speaker_mapping)} entries")
            except Exception as e:
                click.echo(f"Warning: Could not load speaker mapping: {e}", err=True)
        
        # Generate output path if not provided
        if not output:
            output = audio_file.with_suffix('.json')
            if verbose:
                click.echo(f"  Output: {output}")
        
        # Process audio file
        with click.progressbar(length=100, label='Processing audio') as bar:
            # Note: In a real implementation, we would update the progress bar
            # during processing. For now, we'll simulate progress.
            bar.update(10)  # Audio loading
            
            database = process_audio_to_json(
                str(audio_file),
                config,
                str(output),
                speaker_mapping,
                resume_from
            )
            
            bar.update(90)  # Complete
        
        # Success message
        if not quiet:
            entity_count = len(database.entities)
            click.echo(f"✓ Processing complete!")
            click.echo(f"  Entities created: {entity_count}")
            click.echo(f"  Output saved: {output}")
            
            if verbose:
                speakers = len(database.speaker_map)
                avg_confidence = sum(e.confidence for e in database.entities) / entity_count if entity_count > 0 else 0
                click.echo(f"  Speakers detected: {speakers}")
                click.echo(f"  Average confidence: {avg_confidence:.2f}")
        
    except AudioError as e:
        click.echo(f"Audio processing error: {e}", err=True)
        if verbose:
            click.echo(f"  File: {audio_file}", err=True)
        sys.exit(1)
        
    except TranscriptionError as e:
        click.echo(f"Transcription error: {e}", err=True)
        if verbose:
            click.echo("  Check audio quality and language settings", err=True)
        sys.exit(1)
        
    except (EntityError, DatabaseError) as e:
        click.echo(f"Processing error: {e}", err=True)
        sys.exit(1)
        
    except PipelineError as e:
        click.echo(f"Pipeline error: {e}", err=True)
        if verbose:
            click.echo(f"  Context: {e.context}", err=True)
        sys.exit(1)
        
    except Exception as e:
        click.echo(f"Unexpected error: {e}", err=True)
        if verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


@cli.command()
@click.pass_context
def version(ctx):
    """Show version information."""
    click.echo("Spanish Pronunciation Clip Generator v1.0.0")
    click.echo("Colombian Spanish Optimized")


@cli.command()
@click.option('--check-dependencies', is_flag=True, 
              help='Check if all required dependencies are available')
@click.pass_context
def info(ctx, check_dependencies: bool):
    """Show system information and configuration."""
    config = ctx.obj['config']
    
    click.echo("Configuration:")
    click.echo(f"  Whisper model: {config.whisper.model}")
    click.echo(f"  Audio sample rate: {config.audio.sample_rate}")
    click.echo(f"  Min confidence: {config.quality.min_confidence}")
    click.echo(f"  Min word duration: {config.quality.min_word_duration}s")
    click.echo(f"  Max word duration: {config.quality.max_word_duration}s")
    click.echo(f"  Syllable range: {config.quality.syllable_range}")
    
    if check_dependencies:
        click.echo("\nDependency Check:")
        
        # Check Whisper
        try:
            import whisper
            click.echo("  ✓ OpenAI Whisper available")
        except ImportError:
            click.echo("  ✗ OpenAI Whisper not available")
        
        # Check audio libraries
        try:
            import librosa
            click.echo("  ✓ Librosa available")
        except ImportError:
            click.echo("  ✗ Librosa not available")
        
        # Check other dependencies
        try:
            import torch
            click.echo(f"  ✓ PyTorch available")
        except ImportError:
            click.echo("  ✗ PyTorch not available")


if __name__ == '__main__':
    cli()