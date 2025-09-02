"""
Main CLI interface for pronunciation clip generator.

Provides command-line interface for processing Spanish audio files into
pronunciation clips with configurable parameters and user-friendly output.
"""
import sys
import click
import logging
import json
from pathlib import Path
from typing import Optional, Dict, Any

from ..shared.config import load_config, Config
from ..shared.exceptions import (
    ConfigError, AudioError, TranscriptionError, 
    EntityError, DatabaseError, PipelineError
)
from ..shared.logging_config import init_logger
from ..audio_to_json.pipeline import process_audio_to_json
from ..shared.models import WordDatabase


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
@click.option('--language', '-l',
              help='Override language for transcription (e.g., "en", "es", "auto")')
@click.pass_context
def process(ctx, audio_file: Path, output: Optional[Path], 
           speaker_map: Optional[Path], resume_from: Optional[str], language: Optional[str]):
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
    
    # Override language if specified
    if language:
        if language.lower() == 'auto':
            config.whisper.language = None
        else:
            config.whisper.language = language.lower()
    
    try:
        if not quiet:
            click.echo(f"Processing: {audio_file}")
            if verbose:
                click.echo(f"  Model: {config.whisper.model}")
                click.echo(f"  Language: {config.whisper.language or 'auto-detect'}")
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
        
        # Check faster-whisper
        try:
            from faster_whisper import WhisperModel
            click.echo("  ✓ faster-whisper available")
        except ImportError:
            click.echo("  ✗ faster-whisper not available")
        
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


@cli.command()
@click.argument('database_file', type=click.Path(exists=True, path_type=Path))
@click.option('--speaker-id', type=int, required=True, 
              help='Speaker ID to assign labels for')
@click.option('--label', '-l', required=True,
              help='Label to assign (name, gender, region, etc.)')
@click.option('--value', '-v', required=True,
              help='Value for the label')
@click.option('--output', '-o', 
              type=click.Path(path_type=Path),
              help='Output database file (default: overwrite input)')
@click.pass_context
def label_speakers(ctx, database_file: Path, speaker_id: int, 
                  label: str, value: str, output: Optional[Path]):
    """
    Label speakers in a processed database with metadata.
    
    DATABASE_FILE: Path to JSON database file with speaker information
    
    Examples:
        pronunciation-clips label-speakers results.json --speaker-id 0 --label name --value "Maria"
        pronunciation-clips label-speakers results.json --speaker-id 1 --label gender --value "female"
        pronunciation-clips label-speakers results.json --speaker-id 0 --label region --value "Bogotá"
    """
    verbose = ctx.obj['verbose']
    quiet = ctx.obj['quiet']
    
    try:
        if not quiet:
            click.echo(f"Loading database: {database_file}")
        
        # Load the database
        with open(database_file, 'r', encoding='utf-8') as f:
            database_data = json.load(f)
        
        # Validate database structure
        if 'speaker_map' not in database_data:
            click.echo("Error: Database file does not contain speaker_map", err=True)
            sys.exit(1)
        
        speaker_map = database_data['speaker_map']
        
        # Check if speaker ID exists
        speaker_key = str(speaker_id)
        if speaker_key not in speaker_map:
            click.echo(f"Error: Speaker ID {speaker_id} not found in database", err=True)
            click.echo(f"Available speaker IDs: {', '.join(speaker_map.keys())}", err=True)
            sys.exit(1)
        
        # Update speaker information
        speaker_info = speaker_map[speaker_key]
        
        # Valid labels for speaker information
        valid_labels = ['name', 'gender', 'region', 'notes']
        if label not in valid_labels:
            click.echo(f"Warning: Label '{label}' is not a standard speaker attribute", err=True)
            if not quiet:
                click.echo(f"Standard labels: {', '.join(valid_labels)}")
        
        # Update the label
        old_value = speaker_info.get(label, "not set")
        speaker_info[label] = value
        
        if verbose:
            click.echo(f"Speaker {speaker_id}: {label} '{old_value}' → '{value}'")
        
        # Determine output file
        output_file = output if output else database_file
        
        # Save updated database
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(database_data, f, indent=2, ensure_ascii=False)
        
        if not quiet:
            click.echo(f"✓ Speaker {speaker_id} labeled successfully")
            click.echo(f"  {label}: {value}")
            click.echo(f"  Database updated: {output_file}")
        
    except json.JSONDecodeError as e:
        click.echo(f"Error: Invalid JSON in database file: {e}", err=True)
        sys.exit(1)
    except FileNotFoundError:
        click.echo(f"Error: Database file not found: {database_file}", err=True)
        sys.exit(1)
    except Exception as e:
        click.echo(f"Error updating speaker labels: {e}", err=True)
        if verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


@cli.command()
@click.argument('database_file', type=click.Path(exists=True, path_type=Path))
@click.option('--detailed', '-d', is_flag=True,
              help='Show detailed analysis including speaker segments')
@click.option('--output-format', type=click.Choice(['text', 'json']), default='text',
              help='Output format (default: text)')
@click.option('--save-report', '-s',
              type=click.Path(path_type=Path),
              help='Save analysis report to file')
@click.pass_context
def analyze_speakers(ctx, database_file: Path, detailed: bool, 
                    output_format: str, save_report: Optional[Path]):
    """
    Analyze speaker distribution and characteristics in a processed database.
    
    DATABASE_FILE: Path to JSON database file with speaker information
    
    Examples:
        pronunciation-clips analyze-speakers results.json
        pronunciation-clips analyze-speakers results.json --detailed
        pronunciation-clips analyze-speakers results.json --output-format json
        pronunciation-clips analyze-speakers results.json --save-report speaker_analysis.txt
    """
    verbose = ctx.obj['verbose']
    quiet = ctx.obj['quiet']
    
    try:
        if not quiet:
            click.echo(f"Analyzing speakers: {database_file}")
        
        # Load the database
        with open(database_file, 'r', encoding='utf-8') as f:
            database_data = json.load(f)
        
        # Validate database structure
        required_fields = ['speaker_map', 'entities', 'metadata']
        for field in required_fields:
            if field not in database_data:
                click.echo(f"Error: Database file missing required field: {field}", err=True)
                sys.exit(1)
        
        speaker_map = database_data['speaker_map']
        entities = database_data['entities']
        metadata = database_data['metadata']
        
        # Perform speaker analysis
        analysis = _analyze_speaker_distribution(speaker_map, entities, metadata, detailed)
        
        # Format output
        if output_format == 'json':
            output_content = json.dumps(analysis, indent=2, ensure_ascii=False)
        else:
            output_content = _format_speaker_analysis_text(analysis, detailed)
        
        # Display or save output
        if save_report:
            with open(save_report, 'w', encoding='utf-8') as f:
                f.write(output_content)
            if not quiet:
                click.echo(f"✓ Analysis saved to: {save_report}")
        else:
            click.echo(output_content)
        
    except json.JSONDecodeError as e:
        click.echo(f"Error: Invalid JSON in database file: {e}", err=True)
        sys.exit(1)
    except FileNotFoundError:
        click.echo(f"Error: Database file not found: {database_file}", err=True)
        sys.exit(1)
    except Exception as e:
        click.echo(f"Error analyzing speakers: {e}", err=True)
        if verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


def _analyze_speaker_distribution(speaker_map: Dict[str, Any], entities: list, 
                                 metadata: Dict[str, Any], detailed: bool) -> Dict[str, Any]:
    """Analyze speaker distribution and characteristics."""
    
    # Count entities per speaker
    speaker_counts = {}
    speaker_durations = {}
    total_entities = len(entities)
    
    for entity in entities:
        speaker_id = str(entity.get('speaker_id', 0))
        speaker_counts[speaker_id] = speaker_counts.get(speaker_id, 0) + 1
        
        # Calculate duration if timestamps available
        start_time = entity.get('start_time', 0)
        end_time = entity.get('end_time', 0)
        duration = end_time - start_time
        speaker_durations[speaker_id] = speaker_durations.get(speaker_id, 0) + duration
    
    # Build analysis
    analysis = {
        'summary': {
            'total_speakers': len(speaker_map),
            'total_entities': total_entities,
            'total_duration': metadata.get('audio_duration', 0),
            'diarization_enabled': metadata.get('diarization_enabled', False),
            'speakers_detected_by_ml': metadata.get('speakers_detected', 1)
        },
        'speakers': []
    }
    
    # Analyze each speaker
    for speaker_id, speaker_info in speaker_map.items():
        entity_count = speaker_counts.get(speaker_id, 0)
        speaking_duration = speaker_durations.get(speaker_id, 0)
        
        speaker_analysis = {
            'speaker_id': int(speaker_id),
            'name': speaker_info.get('name', f'Speaker {speaker_id}'),
            'gender': speaker_info.get('gender', 'Unknown'),
            'region': speaker_info.get('region', 'Unknown'),
            'entity_count': entity_count,
            'entity_percentage': (entity_count / total_entities * 100) if total_entities > 0 else 0,
            'speaking_duration': speaking_duration,
            'speaking_percentage': (speaking_duration / analysis['summary']['total_duration'] * 100) 
                                 if analysis['summary']['total_duration'] > 0 else 0
        }
        
        if detailed and entity_count > 0:
            # Find speaker segments
            speaker_entities = [e for e in entities if str(e.get('speaker_id', 0)) == speaker_id]
            segments = _find_speaker_segments(speaker_entities)
            speaker_analysis['segments'] = segments
            speaker_analysis['segment_count'] = len(segments)
            
            # Calculate average confidence
            confidences = [e.get('confidence', 0) for e in speaker_entities]
            speaker_analysis['avg_confidence'] = sum(confidences) / len(confidences) if confidences else 0
        
        analysis['speakers'].append(speaker_analysis)
    
    # Sort speakers by speaking time
    analysis['speakers'].sort(key=lambda x: x['speaking_duration'], reverse=True)
    
    return analysis


def _find_speaker_segments(speaker_entities: list) -> list:
    """Find continuous speaking segments for a speaker."""
    if not speaker_entities:
        return []
    
    # Sort by start time
    sorted_entities = sorted(speaker_entities, key=lambda x: x.get('start_time', 0))
    
    segments = []
    current_segment = {
        'start_time': sorted_entities[0].get('start_time', 0),
        'end_time': sorted_entities[0].get('end_time', 0),
        'entity_count': 1
    }
    
    # Group consecutive entities into segments (gap threshold: 2 seconds)
    for entity in sorted_entities[1:]:
        start_time = entity.get('start_time', 0)
        end_time = entity.get('end_time', 0)
        
        if start_time - current_segment['end_time'] <= 2.0:
            # Continue current segment
            current_segment['end_time'] = end_time
            current_segment['entity_count'] += 1
        else:
            # Start new segment
            segments.append(current_segment)
            current_segment = {
                'start_time': start_time,
                'end_time': end_time,
                'entity_count': 1
            }
    
    segments.append(current_segment)
    
    # Add segment durations
    for segment in segments:
        segment['duration'] = segment['end_time'] - segment['start_time']
    
    return segments


def _format_speaker_analysis_text(analysis: Dict[str, Any], detailed: bool) -> str:
    """Format speaker analysis as human-readable text."""
    
    lines = []
    summary = analysis['summary']
    
    # Header
    lines.append("Speaker Analysis Report")
    lines.append("=" * 50)
    lines.append("")
    
    # Summary
    lines.append("Summary:")
    lines.append(f"  Total Speakers: {summary['total_speakers']}")
    lines.append(f"  Total Entities: {summary['total_entities']}")
    lines.append(f"  Total Duration: {summary['total_duration']:.1f}s")
    lines.append(f"  Diarization: {'Enabled' if summary['diarization_enabled'] else 'Disabled'}")
    if summary['diarization_enabled']:
        lines.append(f"  ML Detected Speakers: {summary['speakers_detected_by_ml']}")
    lines.append("")
    
    # Speaker details
    lines.append("Speaker Distribution:")
    lines.append("")
    
    for speaker in analysis['speakers']:
        lines.append(f"Speaker {speaker['speaker_id']} ({speaker['name']}):")
        lines.append(f"  Gender: {speaker['gender']}")
        lines.append(f"  Region: {speaker['region']}")
        lines.append(f"  Entities: {speaker['entity_count']} ({speaker['entity_percentage']:.1f}%)")
        lines.append(f"  Speaking Time: {speaker['speaking_duration']:.1f}s ({speaker['speaking_percentage']:.1f}%)")
        
        if detailed and 'segments' in speaker:
            lines.append(f"  Segments: {speaker['segment_count']}")
            lines.append(f"  Avg Confidence: {speaker['avg_confidence']:.2f}")
            
            if speaker['segments']:
                lines.append("  Speaking Segments:")
                for i, segment in enumerate(speaker['segments'][:5]):  # Show first 5 segments
                    lines.append(f"    {i+1}. {segment['start_time']:.1f}s - {segment['end_time']:.1f}s "
                               f"({segment['duration']:.1f}s, {segment['entity_count']} entities)")
                
                if len(speaker['segments']) > 5:
                    lines.append(f"    ... and {len(speaker['segments']) - 5} more segments")
        
        lines.append("")
    
    return "\n".join(lines)


if __name__ == '__main__':
    cli()