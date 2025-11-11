# Breathwork Transcription Pipeline

**Automated speech-to-text transcription for voice recordings with video timestamps**

🔒 **100% Local Processing** - Your data never leaves your computer
🔬 **Scientifically Valid** - Reproducible, deterministic results
📊 **Complete Metadata** - Timestamps, statistics, and audit trail

---

## Table of Contents

- [What This Does](#what-this-does)
- [How It Works](#how-it-works)
- [Privacy & Data Security](#privacy--data-security)
- [Quick Start](#quick-start)
- [Installation](#installation)
- [Usage](#usage)
- [Input File Requirements](#input-file-requirements)
- [Output Files](#output-files)
- [Technologies Used](#technologies-used)
- [License](#license)
- [Troubleshooting](#troubleshooting)

---

## What This Does

This pipeline automatically transcribes audio recordings (voice notes) and links them to specific timestamps in video recordings. It's designed for:

- **Micro-phenomenological interviews** - Research method where participants describe subjective experiences
- **Video annotation workflows** - Linking voice notes to specific moments in video
- **Qualitative research** - Transcribing interview recordings with timestamps
- **Any timestamped audio** - General-purpose transcription with temporal metadata

**Input:** Audio files (.wav) + JSON files with video timestamps
**Output:** Text transcripts with timestamps, combined transcripts, metadata reports

---

## How It Works

### Pipeline Workflow

```
1. DETECT STRUCTURE
   └─> Auto-detect if processing single session or multiple sessions

2. FIND & MATCH FILES
   └─> Match .wav audio files with .json timestamp files

3. PREPROCESS AUDIO
   └─> Normalize volume, convert to optimal format (16kHz mono 16-bit PCM)
   └─> Uses FFmpeg for audio processing

4. TRANSCRIBE WITH AI
   └─> OpenAI Whisper model (small.en, 244M parameters)
   └─> Runs locally on your CPU/GPU
   └─> Temperature 0.0 for deterministic results

5. MERGE WITH TIMESTAMPS
   └─> Combine transcripts with video timestamps
   └─> Generate individual + combined transcripts

6. OUTPUT RESULTS
   └─> Save TXT (human-readable) and JSON (machine-readable)
   └─> Create processing report with statistics
```

### Processing Details

- **Audio Preprocessing**: FFmpeg converts audio to Whisper-optimized format (16kHz mono, 16-bit PCM) with loudness normalization
- **Transcription**: Whisper AI model processes audio locally, no internet required
- **Verbatim Output**: Preserves filler words, hesitations, and natural speech patterns
- **Deterministic**: Temperature 0.0 ensures identical results on repeated runs

---

## Privacy & Data Security

### 🔒 Your Data Stays Local - Guaranteed

**ZERO data leaves your computer. Here's proof:**

#### 1. **No Network Code in Pipeline**
- The pipeline scripts contain NO network/HTTP requests
- No API calls to external services
- No telemetry or analytics
- Verify yourself: Search pipeline code for `requests`, `urllib`, `http`, `socket` - you won't find them

#### 2. **Whisper Runs 100% Locally**
- Whisper is an open-source model that runs on YOUR computer
- Model downloaded ONCE during first setup
- After download, NO internet connection needed
- See Whisper code: https://github.com/openai/whisper

#### 3. **No Cloud Services**
- Not using OpenAI API (that would send data to cloud)
- Not using any transcription services
- All processing happens on your CPU/GPU

#### 4. **Verify Yourself**

Test with internet OFF:
```bash
# 1. Download model (requires internet, ONE TIME)
python3 pipeline/run_pipeline.py --input /your/folder

# 2. Turn OFF internet connection

# 3. Run again - it will work without internet!
python3 pipeline/run_pipeline.py --input /your/folder
```

#### Privacy Summary

✅ Audio files never leave your device
✅ No internet connection required (after setup)
✅ No cloud services used
✅ No data sent to OpenAI or any third party
✅ No telemetry, analytics, or tracking
✅ Your recordings stay private, period.

**Perfect for:**
- HIPAA-regulated healthcare research
- GDPR-compliant European research
- IRB-approved sensitive research
- Confidential interview data
- Personal recordings

---

## Quick Start

```bash
# 1. Clone the repository
git clone https://github.com/Namsjain01/breathwork-transcription.git
cd breathwork-transcription

# 2. Install dependencies
pip install -r requirements.txt
brew install ffmpeg  # macOS (or: apt install ffmpeg for Linux)

# 3. Verify setup
python3 pipeline/config.py

# 4. Run pipeline on your recordings
python3 pipeline/run_pipeline.py --input /path/to/your/recordings

# Output will be in: /path/to/your/recordings/transcripts/
```

---

## Installation

### Prerequisites

- **Python 3.8 or higher**
- **FFmpeg** (audio processing)
- **8GB+ RAM recommended** (for Whisper model)

### Step 1: Install Python Dependencies

```bash
pip install -r requirements.txt
```

This installs:
- `openai-whisper` - Local transcription AI
- `torch` - PyTorch (required by Whisper)
- `ffmpeg-python` - Audio processing bindings
- `numpy`, `tiktoken` - Supporting libraries

### Step 2: Install FFmpeg

**macOS:**
```bash
brew install ffmpeg
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install ffmpeg
```

**Windows:**
Download from https://ffmpeg.org/download.html and add to PATH

### Step 3: Verify Installation

```bash
python3 pipeline/config.py
```

You should see:
```
✓ Configuration validated successfully
```

---

## Usage

### Basic Usage

Point the pipeline at ANY folder containing .wav and .json files:

```bash
python3 pipeline/run_pipeline.py --input /path/to/your/recordings
```

Transcripts will be created in `/path/to/your/recordings/transcripts/`

### Single Session

Process one folder with recordings:

```bash
# Your folder structure:
my_recording_session/
├── note1.wav
├── note1.json
├── note2.wav
├── note2.json
└── note3.wav
    note3.json

# Run pipeline
python3 pipeline/run_pipeline.py --input /path/to/my_recording_session

# Output created at:
my_recording_session/transcripts/
├── transcripts/              # Individual transcript files
│   ├── note1.txt
│   ├── note1.json
│   ├── note2.txt
│   └── ...
├── combined_transcript.txt   # All transcripts together
├── combined_transcript.json  # Machine-readable format
└── processing_report.txt     # Statistics and metadata
```

### Multiple Sessions (Batch Processing)

Process multiple session folders at once:

```bash
# Your folder structure:
all_my_sessions/
├── session_2024_01_15/
│   ├── note1.wav
│   └── note1.json
├── session_2024_01_20/
│   ├── note1.wav
│   └── note1.json
└── session_2024_02_01/
    ├── note1.wav
    └── note1.json

# Run pipeline
python3 pipeline/run_pipeline.py --input /path/to/all_my_sessions

# Output created in each session folder:
session_2024_01_15/transcripts/
session_2024_01_20/transcripts/
session_2024_02_01/transcripts/
```

### Advanced Options

```bash
# Process specific session by name
python3 pipeline/run_pipeline.py --input /path/to/all_sessions --session session_2024_01_15

# Keep intermediate audio files (for debugging)
python3 pipeline/run_pipeline.py --input /path/to/folder --no-cleanup

# Use current directory
cd /path/to/my/recordings
python3 /path/to/pipeline/run_pipeline.py --input .

# Get help
python3 pipeline/run_pipeline.py --help
```

---

## Input File Requirements

### Required File Structure

Each audio recording needs a matching JSON file:

```
note_001.wav  ←→  note_001.json
```

### JSON Format

The JSON file must contain a video timestamp in seconds:

```json
{
  "video_timestamp_sec": 125.693
}
```

This number represents the timestamp in the video where this voice note was recorded.

### Example

If you recorded a voice note at 2 minutes and 5.693 seconds into a video:

**note_002min05sec.json:**
```json
{
  "video_timestamp_sec": 125.693
}
```

**note_002min05sec.wav:** (your audio recording)

### Audio Format

- **Supported formats**: `.wav`, `.WAV`
- **Any sample rate** (pipeline converts to 16kHz)
- **Any channels** (pipeline converts to mono)
- **Any bit depth** (pipeline converts to 16-bit)

### Files Without Timestamps

Audio files WITHOUT matching JSON files will still be transcribed but marked as "orphaned" (no video timestamp).

---

## Output Files

### Folder Structure

```
your_recordings/
├── note1.wav                     # Your original files
├── note1.json
├── note2.wav
├── note2.json
└── transcripts/                  # ← Output folder (created automatically)
    ├── transcripts/              # Individual transcript files
    │   ├── note1.txt             # Human-readable transcript
    │   ├── note1.json            # Machine-readable with metadata
    │   ├── note2.txt
    │   └── note2.json
    │
    ├── combined_transcript.txt   # All transcripts in one file
    ├── combined_transcript.json  # All transcripts + full metadata
    └── processing_report.txt     # Statistics and processing info
```

### Individual Transcript (TXT)

**note1.txt:**
```
[VIDEO TIMESTAMP: 00:02:05.693]

This is the transcribed text from the audio recording.
All words are preserved verbatim including um, uh, etc.
```

### Individual Transcript (JSON)

**note1.json:**
```json
{
  "audio_file": "note1.wav",
  "has_video_timestamp": true,
  "video_timestamp_sec": 125.693,
  "video_timestamp_formatted": "00:02:05.693",
  "audio_duration_sec": 7.234,
  "transcription": "This is the transcribed text...",
  "word_count": 42,
  "character_count": 215
}
```

### Combined Transcript (TXT)

All transcripts merged into one file, sorted by timestamp:

```
================================================================================
MICRO-PHENOMENOLOGICAL INTERVIEW TRANSCRIPT
================================================================================
Session: my_recording_session
Total Recordings: 5
Transcription Model: Whisper small.en
Processing Date: 2025-11-11 10:30:15
================================================================================

────────────────────────────────────────────────────────────────────────────────
ANNOTATION #1
VIDEO TIMESTAMP: 00:00:05.693 (5.693 seconds)
AUDIO FILE: note1.wav
DURATION: 6.2 seconds
────────────────────────────────────────────────────────────────────────────────

First transcribed text here...

────────────────────────────────────────────────────────────────────────────────
ANNOTATION #2
VIDEO TIMESTAMP: 00:02:15.420 (135.420 seconds)
...
```

### Combined Transcript (JSON)

Complete structured data:

```json
{
  "session_metadata": {
    "session_id": "my_recording_session",
    "processing_timestamp": "2025-11-11T10:30:15",
    "transcription_model": "whisper-small.en",
    "total_recordings": 5,
    "pipeline_version": "1.0.0"
  },
  "annotations": [
    {
      "id": 1,
      "video_timestamp_sec": 5.693,
      "audio_file": "note1.wav",
      "transcription": "...",
      "word_count": 42
    },
    ...
  ],
  "statistics": {
    "total_audio_duration_sec": 187.5,
    "total_words": 324,
    "average_words_per_annotation": 65
  }
}
```

### Processing Report

**processing_report.txt:**
```
================================================================================
TRANSCRIPTION PROCESSING REPORT
================================================================================
Session: my_recording_session
Date: 2025-11-11 10:30:15
Model: Whisper small.en (244M parameters)
================================================================================

FILES PROCESSED
────────────────────────────────────────────────────────────────────────────────
Total audio files found:        5
Successfully transcribed:       5
Success rate:                   100.0%

TIMING
────────────────────────────────────────────────────────────────────────────────
Total processing time:          2m 15s
Average per file:               27.0s

CONTENT STATISTICS
────────────────────────────────────────────────────────────────────────────────
Total audio duration:           187.5 seconds
Total words transcribed:        324
Average words per recording:    65
```

---

## Technologies Used

### Core Technologies

| Component | Technology | Purpose | License |
|-----------|-----------|---------|---------|
| **Transcription AI** | OpenAI Whisper (small.en model) | Speech-to-text recognition | MIT License |
| **Audio Processing** | FFmpeg | Audio format conversion & normalization | LGPL/GPL |
| **Python Runtime** | Python 3.8+ | Pipeline execution | PSF License |
| **ML Framework** | PyTorch | Neural network inference (for Whisper) | BSD License |

### Whisper Model Details

- **Model**: `small.en` (English-only)
- **Parameters**: 244 million
- **Size**: 466 MB
- **Accuracy**: High-quality transcription for English
- **Speed**: ~3-5x realtime on CPU, faster on GPU
- **License**: MIT (fully open source)

### Why These Technologies?

1. **Whisper** - State-of-the-art transcription accuracy, runs locally, open source
2. **FFmpeg** - Industry-standard audio processing, handles all audio formats
3. **Python** - Cross-platform, extensive scientific computing ecosystem
4. **PyTorch** - Efficient neural network inference, GPU acceleration support

---

## License

### This Project

**MIT License** - You can use, modify, and distribute this code freely.

See [LICENSE](LICENSE) file for full text.

### Dependencies

All dependencies are open source and permissively licensed:

- **Whisper**: MIT License (OpenAI)
- **PyTorch**: BSD License (Meta/Facebook)
- **FFmpeg**: LGPL/GPL (depends on build configuration)
- **NumPy**: BSD License

**No proprietary software required.**

---

## Troubleshooting

### FFmpeg Not Found

**Error:**
```
EnvironmentError: FFmpeg not found
```

**Solution:**
```bash
# macOS
brew install ffmpeg

# Linux
sudo apt install ffmpeg

# Verify installation
ffmpeg -version
```

### Out of Memory

**Error:**
```
RuntimeError: CUDA out of memory
```

**Solution:** Whisper model requires ~2GB RAM. Close other applications or use a smaller model:

Edit `pipeline/config.py`:
```python
WHISPER_MODEL = "tiny.en"  # Smaller model (39MB, less accurate)
# or
WHISPER_MODEL = "base.en"  # Medium model (74MB)
```

### Slow Processing

**Issue:** Transcription taking too long

**Solutions:**
1. **Use GPU**: If you have NVIDIA GPU, install PyTorch with CUDA support (10-50x faster)
2. **Smaller model**: Use `tiny.en` or `base.en` (faster but less accurate)
3. **Parallel preprocessing**: Already enabled by default

### No Audio Files Found

**Error:**
```
FileNotFoundError: No audio files found
```

**Solution:**
- Ensure your folder contains `.wav` or `.WAV` files
- Check file extensions are correct
- Verify you're pointing to the right folder

### Python Version Issues

**Error:**
```
SyntaxError or ModuleNotFoundError
```

**Solution:** Requires Python 3.8 or higher:
```bash
python3 --version  # Should show 3.8 or higher
```

### Still Having Issues?

1. Check the processing report in `transcripts/processing_report.txt`
2. Run with `--no-cleanup` to inspect intermediate files
3. Test with a single small audio file first
4. Verify `python3 pipeline/config.py` runs without errors

---

## Additional Information

### System Requirements

- **OS**: macOS, Linux, Windows
- **Python**: 3.8 or higher
- **RAM**: 8GB minimum (16GB recommended)
- **Storage**: 2GB for model + space for your audio files
- **CPU**: Any modern CPU (faster is better)
- **GPU**: Optional but significantly faster with CUDA-capable NVIDIA GPU

### Performance Expectations

- **Preprocessing**: ~1-2 seconds per audio file
- **Transcription**: ~3-5x realtime on CPU (10 seconds of audio = 30-50 seconds processing)
- **GPU**: 10-50x realtime (much faster if available)

### Scientific Use

This pipeline is designed for research:

✅ **Reproducible**: Temperature 0.0 ensures identical results on repeated runs
✅ **Verbatim**: Preserves natural speech including filler words
✅ **Auditable**: Complete processing reports with timestamps and statistics
✅ **Open Source**: All code and models are open source and inspectable
✅ **No Modification**: Transcriptions are not edited or "cleaned up"

Perfect for:
- Qualitative research
- Phenomenological studies
- Interview analysis
- Conversation analysis
- Linguistic research

---

**Version**: 1.0.0
**Last Updated**: 2025-11-11
**Repository**: https://github.com/Namsjain01/breathwork-transcription

---

**Questions or Issues?** Open an issue on GitHub: https://github.com/Namsjain01/breathwork-transcription/issues
