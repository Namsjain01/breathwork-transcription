# How to Use the Breathwork Transcription Pipeline

This guide walks you through setting up and using the transcription pipeline step-by-step.

---

## Table of Contents

1. [Quick Start](#quick-start)
2. [Installation](#installation)
3. [Preparing Your Files](#preparing-your-files)
4. [Running the Pipeline](#running-the-pipeline)
5. [Understanding the Output](#understanding-the-output)
6. [Configuration Options](#configuration-options)
7. [Troubleshooting](#troubleshooting)
8. [Common Scenarios](#common-scenarios)

---

## Quick Start

**For the impatient** - minimal steps to get started:

```bash
# 1. Install dependencies
pip install openai-whisper
brew install ffmpeg  # macOS (or use apt/download for other OS)

# 2. Verify setup
python3 pipeline/config.py

# 3. Run pipeline
python3 pipeline/run_pipeline.py
```

Done! Your transcripts are in the `output/` folder.

---

## Installation

### Step 1: Check Python Version

You need Python 3.8 or higher:

```bash
python3 --version
```

Expected output: `Python 3.8.x` or higher

If you don't have Python, download it from [python.org](https://www.python.org/downloads/).

### Step 2: Install Whisper

```bash
pip install openai-whisper
```

This installs:
- openai-whisper (transcription engine)
- torch (machine learning framework)
- numpy (numerical computing)
- Other dependencies

**Note**: This may take a few minutes and requires ~2GB disk space.

### Step 3: Install FFmpeg

FFmpeg is used for audio processing.

**macOS** (using Homebrew):
```bash
brew install ffmpeg
```

Don't have Homebrew? Install it first:
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

**Ubuntu/Debian Linux**:
```bash
sudo apt update
sudo apt install ffmpeg
```

**Windows**:
1. Download from [ffmpeg.org/download.html](https://ffmpeg.org/download.html)
2. Extract to `C:\ffmpeg`
3. Add `C:\ffmpeg\bin` to your system PATH
4. Restart your terminal

### Step 4: Verify Installation

Run the configuration validator:

```bash
cd "/Users/namsjain01/Desktop/Breathwork transcribe"
python3 pipeline/config.py
```

**Expected output**:
```
✓ Configuration validated successfully

Configuration Summary:
  Input directory: /path/to/vid annos
  Output directory: /path/to/output
  Whisper model: small.en
  Sample rate: 16000 Hz
  Channels: 1 (mono)
  Bit depth: 16-bit
```

If you see this, you're ready to go! 🎉

---

## Preparing Your Files

### Directory Structure

Place your recordings in the `vid annos/` folder:

```
vid annos/
└── participant-name/              # Participant or session folder
    └── video_recording_[date]/    # Recording session
        ├── video_recording_[date].mkv    # Video file (optional)
        ├── note_001.wav                  # Audio recording 1
        ├── note_001.json                 # Timestamp for recording 1
        ├── note_002.wav                  # Audio recording 2
        ├── note_002.json                 # Timestamp for recording 2
        └── ...
```

### Audio Files (.wav)

- **Format**: Any WAV format works (16-bit, 32-bit, float, etc.)
- **Channels**: Mono or stereo (converted to mono automatically)
- **Sample Rate**: Any rate (converted to 16kHz automatically)
- **Naming**: Any name ending in `.wav`

### Timestamp Files (.json)

Create a `.json` file for each audio with the same name:

**Example**: If you have `note_001.wav`, create `note_001.json`:

```json
{
  "video_timestamp_sec": 5.693
}
```

The `video_timestamp_sec` is the time in seconds when this annotation was made in the video.

**How to get the timestamp**:
1. Play your video and pause where the annotation was made
2. Note the time (e.g., 00:00:05.693)
3. Convert to seconds: 5.693
4. Put it in the JSON file

### Files Without Timestamps (Orphaned)

If you have audio files without `.json` files, that's okay! They will still be transcribed and marked as "orphaned recordings" in the output.

**Example**: `temp_audio.wav` without `temp_audio.json` will be transcribed and labeled as having no video timestamp.

---

## Running the Pipeline

### Basic Usage

Process all sessions in `vid annos/`:

```bash
python3 pipeline/run_pipeline.py
```

**What happens**:
1. Scans `vid annos/` for session folders
2. Finds all audio files
3. Matches them with JSON timestamps
4. Preprocesses audio
5. Transcribes with Whisper
6. Generates output files

**Expected output**:
```
✓ Configuration validated successfully

Scanning for sessions...
✓ Found 2 session(s)

================================================================================
Processing session: video_recording_2025-11-10T11_52_19
================================================================================

Step 1: Finding audio files and matching with timestamps...
  ✓ Found 7 files with timestamps
  ⚠ Found 1 orphaned files (no JSON timestamp)

Step 2: Preprocessing audio files...
✓ Successfully preprocessed 8/8 files

Step 3: Transcribing audio with Whisper...
Loading Whisper model 'small.en'...
✓ Model loaded successfully

Transcribing 8 audio files...
  [1/8] note_001.wav... ✓ (125 chars, 23 words)
  [2/8] note_002.wav... ✓ (89 chars, 18 words)
  ...
  [8/8] temp_audio.wav... ✓ (447 chars, 89 words)

✓ Successfully transcribed 8/8 files

...

✓ Session processed successfully in 33.3 seconds
```

### Process Specific Session

If you only want to process one session:

```bash
python3 pipeline/run_pipeline.py --session video_recording_2025-11-10T11_52_19
```

Replace `video_recording_2025-11-10T11_52_19` with your session folder name.

### Keep Intermediate Files

By default, the preprocessed audio files are deleted after transcription. To keep them:

```bash
python3 pipeline/run_pipeline.py --no-cleanup
```

The preprocessed files will be saved in `processed/[session_name]/normalized_audio/`.

This is useful for:
- Debugging audio issues
- Checking preprocessing results
- Reusing preprocessed audio

---

## Understanding the Output

After processing, you'll find outputs in `output/[session_name]/`:

```
output/
└── video_recording_2025-11-10T11_52_19/
    ├── transcripts/                    # Individual files
    │   ├── note_001.txt               # Transcript with timestamp
    │   ├── note_001.json              # Metadata
    │   ├── note_002.txt
    │   ├── note_002.json
    │   └── ...
    ├── combined_transcript.txt         # All transcripts combined
    ├── combined_transcript.json        # All data in JSON format
    └── processing_report.txt           # Statistics and info
```

### Individual Transcript Files

**TXT Format** (`transcripts/note_001.txt`):
```
[VIDEO TIMESTAMP: 00:00:05.693]

The participant described their experience here.
```

**JSON Format** (`transcripts/note_001.json`):
```json
{
  "audio_file": "note_001.wav",
  "has_video_timestamp": true,
  "video_timestamp_sec": 5.693,
  "video_timestamp_formatted": "00:00:05.693",
  "audio_duration_sec": 5.668,
  "transcription": "The participant described their experience here.",
  "word_count": 6,
  "character_count": 47
}
```

### Combined Transcript (TXT)

Human-readable file with all transcripts in chronological order:

```
================================================================================
MICRO-PHENOMENOLOGICAL INTERVIEW TRANSCRIPT
================================================================================
Session: video_recording_2025-11-10T11_52_19
Video File: video_recording_2025-11-10T11_52_19.mkv
Total Recordings: 8
Transcription Model: Whisper small.en
Processing Date: 2025-11-10 19:28:30
================================================================================


────────────────────────────────────────────────────────────────────────────────
ANNOTATION #1
VIDEO TIMESTAMP: 00:00:05.693 (5.693 seconds)
AUDIO FILE: note_001.wav
DURATION: 5.7 seconds
────────────────────────────────────────────────────────────────────────────────

The participant described their experience here.


────────────────────────────────────────────────────────────────────────────────
ANNOTATION #2
VIDEO TIMESTAMP: 00:00:19.727 (19.727 seconds)
...
```

### Combined JSON

Machine-readable format with complete metadata:

```json
{
  "session_metadata": {
    "session_id": "video_recording_2025-11-10T11_52_19",
    "video_file": "video_recording_2025-11-10T11_52_19.mkv",
    "total_recordings": 8,
    "total_with_timestamps": 7,
    "total_orphaned": 1,
    "transcription_model": "whisper-small.en"
  },
  "annotations": [
    {
      "id": 1,
      "video_timestamp_sec": 5.693,
      "transcription": "...",
      "word_count": 23
    },
    ...
  ],
  "orphaned_recordings": [...],
  "statistics": {...}
}
```

### Processing Report

Statistics about the transcription process:

```
FILES PROCESSED
────────────────────────────────────────────────────────────────────────────────
Total audio files found:        8
With JSON timestamps:           7
Orphaned (no JSON):             1
Successfully transcribed:       8
Success rate:                   100.0%

TIMING
────────────────────────────────────────────────────────────────────────────────
Total processing time:          0m 33s
Average per file:               4.1s
Audio duration / processing:    3.66x (realtime)

CONTENT STATISTICS
────────────────────────────────────────────────────────────────────────────────
Total audio duration:           122.6 seconds
Total words transcribed:        121
Average words per recording:    15
```

---

## Configuration Options

Edit `pipeline/config.py` to customize the pipeline.

### Change Whisper Model

```python
WHISPER_MODEL = "small.en"
```

**Available models**:

| Model | Size | Speed | Accuracy | Use When |
|-------|------|-------|----------|----------|
| `tiny.en` | 39M | Fastest | Good | Testing, low-end hardware |
| `base.en` | 74M | Fast | Better | Quick processing needed |
| `small.en` | 244M | Medium | High ⭐ | **Recommended for research** |
| `medium.en` | 769M | Slow | Very High | Maximum accuracy needed |
| `large` | 1550M | Slowest | Highest | Critical transcriptions |

**After changing**, the new model will download on first run.

### Change Output Options

```python
# Choose what files to generate
GENERATE_INDIVIDUAL_TRANSCRIPTS = True  # Create individual TXT + JSON files
GENERATE_COMBINED_TXT = True            # Create combined_transcript.txt
GENERATE_COMBINED_JSON = True           # Create combined_transcript.json
GENERATE_PROCESSING_REPORT = True       # Create processing_report.txt

# Cleanup
DELETE_INTERMEDIATE_FILES = True        # Delete processed audio after transcription
```

### Performance Tuning

```python
# Parallel processing (None = use all CPU cores)
NUM_PARALLEL_PROCESSES = None  # or set to specific number like 4
```

**Recommendations**:
- Leave as `None` for fastest processing
- Set to `2` or `4` if your computer is slow or overheating
- Set to `1` for lowest CPU usage (sequential processing)

### Audio Settings

Usually don't need to change these:

```python
TARGET_SAMPLE_RATE = 16000      # Whisper is optimized for 16kHz
TARGET_CHANNELS = 1             # Mono (stereo is converted automatically)
NORMALIZE_AUDIO = True          # Loudness normalization (recommended)
```

---

## Troubleshooting

### Error: "FFmpeg not found"

**Problem**: FFmpeg is not installed or not in PATH

**Solution**:
```bash
# macOS
brew install ffmpeg

# Ubuntu/Debian
sudo apt install ffmpeg

# Windows - download from ffmpeg.org and add to PATH
```

Verify installation:
```bash
ffmpeg -version
```

### Error: "No module named 'whisper'"

**Problem**: Whisper is not installed

**Solution**:
```bash
pip install openai-whisper
```

Or if using pip3:
```bash
pip3 install openai-whisper
```

### Slow Transcription

**Problem**: Transcription takes too long

**Solutions**:
1. **Use smaller model**: Change to `base.en` or `tiny.en` in `config.py`
2. **Check CPU usage**: Close other programs
3. **Reduce parallel processes**: Set `NUM_PARALLEL_PROCESSES = 2` in `config.py`

### Poor Transcription Quality

**Problem**: Transcriptions are inaccurate

**Solutions**:
1. **Use larger model**: Change to `medium.en` or `large` in `config.py`
2. **Check audio quality**: Ensure recordings are clear
3. **Check microphone**: Better audio quality = better transcription
4. **Review manually**: Always validate automated transcriptions

### Memory Error

**Problem**: System runs out of memory

**Solutions**:
1. **Use smaller model**: `tiny.en` or `base.en`
2. **Close other programs**: Free up RAM
3. **Process one session at a time**: Use `--session` flag
4. **Reduce parallel processes**: `NUM_PARALLEL_PROCESSES = 1`

### No Sessions Found

**Problem**: "No sessions found in input directory!"

**Solution**: Check your directory structure:
```bash
ls -la "vid annos/"
```

Make sure you have:
```
vid annos/
└── [some-folder]/
    └── video_recording_*/
        └── *.wav files
```

### Orphaned Files Warning

**Not an error!** This just means some `.wav` files don't have matching `.json` files.

If you want timestamps:
1. Create `.json` files with the same name as the `.wav` files
2. Add `{"video_timestamp_sec": X.XXX}` where X.XXX is the timestamp in seconds

---

## Common Scenarios

### Scenario 1: First-Time Use

```bash
# 1. Install dependencies
pip install openai-whisper
brew install ffmpeg  # or apt/download

# 2. Verify setup
python3 pipeline/config.py

# 3. Place your recordings in vid annos/
# 4. Run pipeline
python3 pipeline/run_pipeline.py

# 5. Check output/
```

### Scenario 2: Process Only New Sessions

```bash
# Process specific session
python3 pipeline/run_pipeline.py --session video_recording_2025-11-10
```

### Scenario 3: Re-transcribe with Different Model

```bash
# 1. Edit config.py
# Change: WHISPER_MODEL = "medium.en"

# 2. Delete old output
rm -rf output/video_recording_2025-11-10/

# 3. Re-run
python3 pipeline/run_pipeline.py --session video_recording_2025-11-10
```

### Scenario 4: Check Audio Before Transcription

```bash
# Run with --no-cleanup to keep preprocessed files
python3 pipeline/run_pipeline.py --no-cleanup

# Check preprocessed audio
ls processed/video_recording_*/normalized_audio/

# Listen to preprocessed files to verify quality
# (They should be 16kHz mono WAV files)
```

### Scenario 5: Batch Process Multiple Sessions

```bash
# Just run without --session flag
python3 pipeline/run_pipeline.py

# It will process all sessions in vid annos/
```

### Scenario 6: Export Data for Analysis

The `combined_transcript.json` file is perfect for data analysis:

**Python example**:
```python
import json

# Load transcriptions
with open('output/session_name/combined_transcript.json') as f:
    data = json.load(f)

# Get all transcriptions
for annotation in data['annotations']:
    timestamp = annotation['video_timestamp_sec']
    text = annotation['transcription']
    print(f"At {timestamp}s: {text}")
```

**Excel/R/SPSS**: Open the JSON file with your analysis tool or convert to CSV.

---

## Tips & Best Practices

### ✅ Do's

- **Validate transcriptions**: Always manually review at least a sample
- **Use version control**: Keep track of which model version you used
- **Document settings**: Note model and configuration in your research methods
- **Backup originals**: Keep original audio files safe
- **Test first**: Try with 1-2 files before processing hundreds

### ❌ Don'ts

- **Don't delete originals**: Always keep source audio files
- **Don't skip validation**: Automated ≠ 100% accurate
- **Don't mix models**: Use same model for all recordings in a study
- **Don't ignore warnings**: Check what they mean
- **Don't assume perfection**: AI makes mistakes, especially with unclear audio

---

## Getting Help

### Check Configuration

```bash
python3 pipeline/config.py
```

### Test with Sample File

Process just one session to test:
```bash
python3 pipeline/run_pipeline.py --session [session_name]
```

### Check Logs

The processing report has detailed statistics:
```bash
cat output/[session_name]/processing_report.txt
```

### Common Commands

```bash
# List all sessions
ls "vid annos/"

# Check specific session files
ls "vid annos/[participant]/video_recording_*/"

# View output
ls output/

# Check model cache
ls models/

# Check preprocessed audio (if using --no-cleanup)
ls processed/
```

---

## Next Steps

1. **Read OVERVIEW.md** for scientific validity and privacy information
2. **Test with sample data** before processing real recordings
3. **Validate accuracy** on your specific data
4. **Document your workflow** for research methods section
5. **Contact IRB** if using for research with human participants

---

**Questions?** See `OVERVIEW.md` for detailed information about privacy, scientific validity, and licensing.

**Last Updated**: 2025-11-10
**Pipeline Version**: 1.0.0
