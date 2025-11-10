# Breathwork Transcription Pipeline

Automated transcription system for micro-phenomenological interview recordings using OpenAI's Whisper AI.

**🔒 100% Local Processing** - No data sent to the internet
**🔬 Scientifically Valid** - Reproducible, deterministic results
**📊 Complete Metadata** - Timestamps, statistics, and audit trail

---

## Documentation

### 📖 [OVERVIEW.md](./OVERVIEW.md) - Read This First
**What this is, privacy, and scientific validity**

- What the pipeline does and how it works
- Privacy guarantees (100% local, no cloud, no data collection)
- Scientific validity and reproducibility
- Licensing and legal information
- Ethical considerations and IRB guidance
- Compliance (GDPR, HIPAA)

👉 **Read this if you need to understand**:
- Is my data private and secure?
- Can I use this for research?
- Is this scientifically valid?
- What are the licenses?

### 🛠️ [USAGE.md](./USAGE.md) - Practical Guide
**How to install and use the pipeline**

- Step-by-step installation
- Preparing your files
- Running the pipeline
- Understanding output files
- Configuration options
- Troubleshooting

👉 **Read this if you want to**:
- Set up the pipeline
- Process your recordings
- Customize settings
- Fix problems

---

## Quick Start

```bash
# 1. Install dependencies
pip install openai-whisper
brew install ffmpeg  # macOS (or apt install ffmpeg for Linux)

# 2. Verify setup
python3 pipeline/config.py

# 3. Run pipeline
python3 pipeline/run_pipeline.py
```

Your transcripts will be in the `output/` folder.

**Need help?** See [USAGE.md](./USAGE.md) for detailed instructions.

---

## Key Features

✅ **Automatic Transcription** - AI-powered speech-to-text using Whisper
✅ **Timestamp Preservation** - Links transcriptions to exact video moments
✅ **Multiple Formats** - TXT (human-readable) and JSON (machine-readable)
✅ **Batch Processing** - Process multiple sessions automatically
✅ **Privacy-First** - All processing local, no cloud, no data collection
✅ **Reproducible** - Deterministic results for scientific research

---

## Privacy & Security

🔒 **All processing happens on your computer**
- Audio files never leave your device
- No internet connection needed (after setup)
- No cloud services used
- No data sent to OpenAI or any third party

See [OVERVIEW.md](./OVERVIEW.md) for complete privacy documentation.

---

## Scientific Use

🔬 **Designed for rigorous research**
- Reproducible (temperature 0.0, deterministic)
- Verbatim transcription (preserves filler words)
- Complete metadata and audit trail
- Open-source model (Whisper MIT License)

See [OVERVIEW.md](./OVERVIEW.md) for scientific validity details.

---

## Support

- **Installation help**: See [USAGE.md](./USAGE.md#installation)
- **Troubleshooting**: See [USAGE.md](./USAGE.md#troubleshooting)
- **Privacy questions**: See [OVERVIEW.md](./OVERVIEW.md#privacy--data-security)
- **Scientific validity**: See [OVERVIEW.md](./OVERVIEW.md#scientific-validity)

---

**Version**: 1.0.0
**Last Updated**: 2025-11-10
**License**: MIT (Whisper), See [OVERVIEW.md](./OVERVIEW.md#licensing--legal)
