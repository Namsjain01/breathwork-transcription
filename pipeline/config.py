"""
Configuration file for micro-phenomenological interview transcription pipeline.

This file contains all settings and paths used by the transcription system.
Modify these settings to customize the pipeline behavior.
"""

import os
from pathlib import Path

# ============================================================================
# DIRECTORY PATHS
# ============================================================================

# Base directory (project root)
BASE_DIR = Path(__file__).parent.parent.absolute()

# Input: Original data directory
INPUT_DIR = BASE_DIR / "vid annos"

# Temporary: Processed audio files (will be deleted after transcription)
PROCESSED_DIR = BASE_DIR / "processed"

# Output: Final transcriptions and reports
OUTPUT_DIR = BASE_DIR / "output"

# Models: Whisper model storage
MODELS_DIR = BASE_DIR / "models"

# ============================================================================
# WHISPER SETTINGS
# ============================================================================

# Model size: "tiny.en", "base.en", "small.en", "medium.en", "large"
# small.en = 244M parameters, 466 MB, high accuracy (RECOMMENDED)
WHISPER_MODEL = "small.en"

# Language (force English transcription)
LANGUAGE = "en"

# Temperature for sampling (0.0 = deterministic/reproducible)
TEMPERATURE = 0.0

# Task type (transcribe vs translate)
TASK = "transcribe"

# Verbose output from Whisper
VERBOSE = False

# ============================================================================
# AUDIO PREPROCESSING SETTINGS
# ============================================================================

# Target sample rate (Whisper optimized for 16kHz)
TARGET_SAMPLE_RATE = 16000

# Target channels (1 = mono, Whisper works best with mono)
TARGET_CHANNELS = 1

# Target bit depth (16-bit PCM standard for Whisper)
TARGET_BIT_DEPTH = 16

# Audio normalization (loudness normalization for consistent volume)
NORMALIZE_AUDIO = True

# FFmpeg executable (usually just "ffmpeg" if on PATH)
FFMPEG_EXECUTABLE = "ffmpeg"

# ============================================================================
# FILE MATCHING SETTINGS
# ============================================================================

# Audio file extensions to process
AUDIO_EXTENSIONS = [".wav", ".WAV"]

# JSON metadata file extension
JSON_EXTENSION = ".json"

# Files to ignore (only system files - NOT audio files)
# Note: Only ignore actual system files, not audio recordings
# Even if a recording is named "temp_audio.wav", it should be transcribed
IGNORE_FILES = [".DS_Store", "Thumbs.db", "desktop.ini"]

# ============================================================================
# OUTPUT SETTINGS
# ============================================================================

# Generate individual transcript files
GENERATE_INDIVIDUAL_TRANSCRIPTS = True

# Generate combined transcript (TXT format)
GENERATE_COMBINED_TXT = True

# Generate combined transcript (JSON format)
GENERATE_COMBINED_JSON = True

# Generate processing report
GENERATE_PROCESSING_REPORT = True

# Delete intermediate processed audio files after transcription
DELETE_INTERMEDIATE_FILES = True

# ============================================================================
# TRANSCRIPT FORMATTING
# ============================================================================

# Timestamp format for video timestamps
TIMESTAMP_FORMAT = "%H:%M:%S"  # e.g., "00:00:05.693"

# Include milliseconds in timestamp display
INCLUDE_MILLISECONDS = True

# Separator for combined transcript sections
SECTION_SEPARATOR = "─" * 80

# Header separator for combined transcript
HEADER_SEPARATOR = "=" * 80

# ============================================================================
# PROCESSING SETTINGS
# ============================================================================

# Number of parallel processes for audio preprocessing
# Set to None to use all available CPU cores
NUM_PARALLEL_PROCESSES = None

# Skip already transcribed files (for resuming interrupted processing)
SKIP_EXISTING = True

# Show progress bars
SHOW_PROGRESS = True

# ============================================================================
# LOGGING SETTINGS
# ============================================================================

# Log level: "DEBUG", "INFO", "WARNING", "ERROR"
LOG_LEVEL = "INFO"

# Log to file in addition to console
LOG_TO_FILE = True

# Log file location
LOG_FILE = OUTPUT_DIR / "transcription.log"

# ============================================================================
# SCIENTIFIC METADATA
# ============================================================================

# Methodology reference
METHODOLOGY_FILE = BASE_DIR / "METHODOLOGY.md"

# Version of this pipeline
PIPELINE_VERSION = "1.0.0"

# Processing description
PROCESSING_DESCRIPTION = """
Audio files were preprocessed using FFmpeg (loudness normalization,
conversion to 16kHz mono 16-bit PCM) and transcribed using OpenAI
Whisper small.en model (244M parameters) with temperature 0.0 for
reproducibility. All processing performed locally with no cloud services.
"""

# ============================================================================
# VALIDATION
# ============================================================================

def validate_config():
    """Validate configuration settings and create necessary directories."""

    # Check if input directory exists
    if not INPUT_DIR.exists():
        raise FileNotFoundError(f"Input directory not found: {INPUT_DIR}")

    # Create output directories if they don't exist
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    MODELS_DIR.mkdir(parents=True, exist_ok=True)

    # Validate Whisper model name
    valid_models = ["tiny.en", "tiny", "base.en", "base", "small.en",
                    "small", "medium.en", "medium", "large", "large-v2", "large-v3"]
    if WHISPER_MODEL not in valid_models:
        raise ValueError(f"Invalid Whisper model: {WHISPER_MODEL}. "
                        f"Valid options: {', '.join(valid_models)}")

    # Check if FFmpeg is available
    import subprocess
    try:
        subprocess.run([FFMPEG_EXECUTABLE, "-version"],
                      capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        raise EnvironmentError(f"FFmpeg not found. Please install FFmpeg and "
                             f"ensure it's on your PATH.")

    print("✓ Configuration validated successfully")
    return True

if __name__ == "__main__":
    # Test configuration when run directly
    validate_config()
    print(f"\nConfiguration Summary:")
    print(f"  Input directory: {INPUT_DIR}")
    print(f"  Output directory: {OUTPUT_DIR}")
    print(f"  Whisper model: {WHISPER_MODEL}")
    print(f"  Sample rate: {TARGET_SAMPLE_RATE} Hz")
    print(f"  Channels: {TARGET_CHANNELS} (mono)")
    print(f"  Bit depth: {TARGET_BIT_DEPTH}-bit")
