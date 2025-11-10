# Transcription Methodology for Micro-Phenomenological Interviews

## Overview

This document describes the complete methodology used for transcribing micro-phenomenological interview recordings. All processing was performed locally with no cloud services or data sharing.

---

## 1. Data Collection

### Recording Protocol
- **Method**: Participants viewed their task videos and paused at significant moments
- **Action**: At each pause, participants recorded verbal descriptions of their phenomenological experience
- **Metadata**: Video timestamps stored in JSON files alongside audio recordings
- **Format**: Audio recorded as WAV files (16kHz, stereo, 32-bit float PCM)

### File Structure
```
Session/
├── video_recording_[timestamp].mkv          # Original task video
└── video_recording_[timestamp]/             # Recording folder
    ├── note_[timestamp].wav                 # Audio recording
    ├── note_[timestamp].json                # Video timestamp metadata
    └── ... (multiple recordings per session)
```

---

## 2. Audio Preprocessing

### Tool
- **Software**: FFmpeg 7.x
- **Purpose**: Normalize audio levels and convert to optimal format for transcription

### Processing Steps
1. **Loudness Normalization**: Applied FFmpeg's `loudnorm` filter for consistent volume
2. **Channel Conversion**: Stereo → Mono (reduces file size, optimal for speech recognition)
3. **Sample Rate**: Maintained at 16kHz (already optimal for Whisper)
4. **Bit Depth Conversion**: 32-bit float → 16-bit PCM (standard format, reduces memory usage)

### FFmpeg Command
```bash
ffmpeg -i input.wav \
  -vn \
  -ar 16000 \
  -ac 1 \
  -sample_fmt s16 \
  -af loudnorm \
  -y output.wav
```

### Rationale
- Loudness normalization improves transcription accuracy across recordings with varying volumes
- Mono audio is sufficient for single-speaker recordings and reduces processing time
- 16-bit PCM is the standard input format for Whisper models

---

## 3. Speech-to-Text Transcription

### Model
- **Name**: OpenAI Whisper small.en
- **Parameters**: 244 million
- **Size**: 466 MB
- **Language**: English-optimized
- **Version**: 20250625 (openai-whisper Python package)

### Model Selection Rationale
- **small.en**: Balances high accuracy (95-99% WER on English) with reasonable processing speed
- **English-optimized**: Better performance than multilingual models for English speech
- **Appropriate for non-native speakers**: Trained on diverse English accents, including European speakers

### Transcription Settings
```python
model.transcribe(
    audio_file,
    language="en",           # Force English (prevent language detection errors)
    task="transcribe",       # Transcribe (not translate)
    temperature=0.0,         # Deterministic output (reproducible results)
    verbose=False,
    word_timestamps=False    # Not needed (we have video timestamps)
)
```

### Key Parameters
- **Temperature 0.0**: Ensures deterministic, reproducible transcriptions (scientific requirement)
- **Language forced**: Prevents misdetection of language, especially for non-native speakers
- **No post-processing**: Preserves verbatim speech including filler words ("um", "uh", "like")

### Verbatim Transcription
- **Filler words preserved**: "um", "uh", "like", "you know", etc.
- **Pauses maintained**: Natural speech patterns kept intact
- **No correction**: Vague or unusual terminology (mystical language) transcribed as spoken
- **Non-native accents**: Handled without "correction" to native pronunciation

---

## 4. Timestamp Integration

### Process
1. Match audio files with corresponding JSON timestamp files by filename
2. Parse `video_timestamp_sec` from JSON metadata
3. Combine transcription text with video timestamp
4. Sort annotations chronologically by video timestamp

### Orphaned Files
- **Definition**: Audio files without matching JSON timestamp files
- **Handling**: Still transcribed but marked as "ORPHANED" in output
- **Sorting**: Ordered by file creation timestamp when no video timestamp available

---

## 5. Output Generation

### Individual Transcript Files
- **Format**: Plain text (.txt)
- **Header**: Video timestamp or "ORPHANED" marker
- **Content**: Verbatim transcribed text
- **Location**: `output/[session]/transcripts/`

Example format:
```
[VIDEO TIMESTAMP: 00:00:05.693]

Um, so at that moment, I felt this kind of overwhelming...
```

### Combined Transcript (TXT)
- **Format**: Human-readable plain text
- **Structure**: All annotations in chronological order with headers
- **Metadata**: Session info, processing date, model used
- **Statistics**: Total duration, word count
- **Location**: `output/[session]/combined_transcript.txt`

### Combined Transcript (JSON)
- **Format**: Structured JSON for computational analysis
- **Fields**: Timestamps, transcriptions, word counts, durations
- **Metadata**: Complete session and processing information
- **Location**: `output/[session]/combined_transcript.json`

### Processing Report
- **Format**: Plain text summary
- **Contents**:
  - File counts and success rates
  - Processing timing statistics
  - Content statistics (word counts, durations)
  - Video coverage span
  - System information
- **Location**: `output/[session]/processing_report.txt`

---

## 6. Data Privacy & Security

### Local Processing
- ✅ **All processing performed locally** on researcher's machine
- ✅ **No internet required** after initial model download
- ✅ **No cloud services** used at any stage
- ✅ **No data sharing** or upload to external servers
- ✅ **No telemetry** or usage tracking

### Data Flow
```
Original WAV files (local)
    ↓
FFmpeg preprocessing (local)
    ↓
Whisper transcription (local, in-memory)
    ↓
Output files (local)
```

### Software Used
- **FFmpeg**: Open-source, local audio processing
- **OpenAI Whisper**: Open-source model, runs locally (no API calls)
- **Python 3.13**: Open-source programming language
- **All code**: Custom scripts, fully auditable

---

## 7. Reproducibility

### Software Versions
- **Operating System**: macOS 14.6.0 (Sequoia)
- **Python**: 3.13
- **openai-whisper**: 20250625
- **FFmpeg**: 7.x
- **PyTorch**: 2.9.0 (Whisper dependency)
- **Pipeline Version**: 1.0.0

### Model Reproducibility
- **Model**: Whisper small.en (fixed version)
- **Temperature**: 0.0 (deterministic)
- **Random seed**: Not applicable (temperature=0.0 removes randomness)

### Verification
Re-running the same audio file through the pipeline will produce **identical transcriptions** due to:
1. Fixed model version
2. Deterministic temperature setting (0.0)
3. No random sampling

### How to Reproduce
1. Install dependencies: `pip install openai-whisper`
2. Use same Whisper model: `small.en`
3. Use same temperature: `0.0`
4. Use same preprocessing: FFmpeg loudnorm, mono, 16kHz, 16-bit
5. Run pipeline: `python pipeline/run_pipeline.py`

---

## 8. Quality Assurance

### Validation Steps
1. **Manual verification**: Random sample of transcriptions compared to audio
2. **Filler word check**: Verify "um", "uh", etc. are preserved
3. **Terminology check**: Ensure vague/mystical language not "corrected"
4. **Timestamp alignment**: Verify JSON timestamps correctly integrated
5. **Consistency check**: Re-run same file to verify identical output

### Expected Accuracy
- **Clear native English**: 95-99% Word Error Rate (WER)
- **Non-native speakers**: 90-95% WER
- **Vague terminology**: May require minor manual review for proper nouns or neologisms

### Limitations
- Very strong accents may have reduced accuracy
- Technical terminology or neologisms may be transcribed phonetically
- Overlapping speech or extreme background noise may affect quality
- Very quiet passages may be missed

---

## 9. Scientific Standards

### Transparency
- ✅ Complete source code available
- ✅ Processing parameters documented
- ✅ Software versions specified
- ✅ Method fully described

### Objectivity
- ✅ No manual editing of transcriptions
- ✅ Automated processing (removes human bias)
- ✅ Verbatim output (no interpretation)
- ✅ Deterministic results (reproducible)

### Documentation
- ✅ Processing report generated for each session
- ✅ Metadata preserved in JSON output
- ✅ Methodology document (this file)
- ✅ Audit trail via file timestamps

---

## 10. Citation

If using this methodology in academic work, please cite:

```
Transcription performed using OpenAI Whisper small.en model (244M parameters)
with deterministic sampling (temperature=0.0). Audio preprocessed with FFmpeg
loudness normalization. All processing performed locally with no cloud services.
Pipeline version 1.0.0.
```

### References
- Radford, A., et al. (2022). "Robust Speech Recognition via Large-Scale Weak Supervision."
  *arXiv preprint arXiv:2212.04356*.
- OpenAI Whisper: https://github.com/openai/whisper
- FFmpeg: https://ffmpeg.org/

---

## 11. Contact & Support

For questions about this methodology or pipeline:
- **Pipeline Location**: `/Users/namsjain01/Desktop/Breathwork transcribe/`
- **Configuration**: `pipeline/config.py`
- **Main Script**: `pipeline/run_pipeline.py`

---

**Document Version**: 1.0
**Last Updated**: 2025-11-10
**Author**: Automated transcription pipeline
