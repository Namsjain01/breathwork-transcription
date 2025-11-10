# Breathwork Transcription Pipeline - Scientific Overview

## What This Pipeline Does

This is an **automated transcription system** for micro-phenomenological interview recordings. It converts audio annotations from video interviews into timestamped text transcripts using artificial intelligence.

### The Process

1. **Input**: You provide audio recordings (.wav files) and optional timestamp metadata (.json files)
2. **Processing**: The system processes audio locally on your computer using OpenAI's Whisper AI model
3. **Output**: You receive accurate text transcripts with timestamps, metadata, and statistics

### Key Capability

The pipeline maintains the critical link between:
- **What was said** (transcribed speech)
- **When it was said** (video timestamp)
- **The original recording** (source audio file)

This enables researchers to analyze qualitative data while preserving temporal context with the video being discussed.

---

## Privacy & Data Security

### 🔒 100% Local Processing

**ALL processing happens on your computer. Nothing is sent to the internet.**

- ✅ Audio files never leave your device
- ✅ Transcriptions are generated locally
- ✅ No internet connection required after initial setup
- ✅ No cloud services used
- ✅ No external servers contacted during processing

### 🚫 No Data Collection

**Your data is never used for training or shared with anyone.**

- ✅ No telemetry or usage tracking
- ✅ No data sent to OpenAI or any third party
- ✅ No participant data exposed to external services
- ✅ Complete data sovereignty - you control everything

### 📁 Data Flow

```
Your Computer Only:
├─ Input: Audio files (vid annos/)
├─ Processing: Local Whisper model
└─ Output: Transcripts (output/)

External Network: NONE ❌
Cloud Services: NONE ❌
Data Uploaded: NONE ❌
```

### Model Download (One-Time Only)

**First-time setup** downloads the Whisper model (~500MB) from OpenAI's servers:
- This happens ONCE when you first run the pipeline
- The model is cached locally in the `models/` folder
- After download, NO internet connection is needed
- The model is NOT trained on your data
- Your audio is NEVER sent to OpenAI

---

## Scientific Validity

### Reproducibility

This pipeline is designed for rigorous scientific research with full reproducibility:

#### Deterministic Results
- **Temperature: 0.0** - Same input always produces identical output
- Run the same audio file multiple times → Get exactly the same transcription
- Critical for peer review and validation

#### Version Control
- Pipeline version tracked in all outputs
- Model version documented (Whisper small.en)
- Processing date/time recorded
- Complete audit trail maintained

#### Metadata Preservation
All outputs include:
- Original filename
- Video timestamp (when available)
- Audio duration
- Word count and character count
- Processing parameters
- System information

### Verbatim Transcription

The pipeline preserves natural speech characteristics:

- ✅ **Filler words preserved** ("um", "uh", "like")
- ✅ **Pauses and hesitations** captured
- ✅ **Natural speech patterns** maintained
- ✅ **No post-processing** or "cleaning"
- ✅ **No interpretation** or summarization

This is critical for phenomenological research where exact wording matters.

### Accuracy & Validation

**Whisper small.en Model** (244M parameters):
- Trained on 680,000 hours of multilingual speech
- Word Error Rate (WER): ~3-5% on English speech
- Performs well on diverse accents and audio quality
- Published by OpenAI with peer-reviewed performance metrics

**Recommended Validation Workflow**:
1. Transcribe your audio with this pipeline
2. Manually review a sample (~10%) of transcriptions
3. Calculate accuracy on your specific data
4. Report validation results in your methods section

### Scientific Method Compatibility

**For Micro-Phenomenological Interviews:**
- Preserves temporal structure of experience descriptions
- Links speech to exact moments in video
- Maintains verbatim accounts without interpretation
- Supports detailed qualitative analysis

**For Phenomenological Research:**
- No algorithmic bias in interpretation
- Transparent processing pipeline
- Fully documented methodology
- Replicable across research groups

---

## Ethical Considerations

### Participant Privacy

✅ **Local processing protects participant confidentiality**
- No audio leaves your institution's computers
- No risk of data breaches from cloud storage
- No third-party access to sensitive recordings
- Full compliance with data protection regulations (GDPR, HIPAA, etc.)

### Informed Consent

When using this pipeline, your consent forms can truthfully state:
- "Audio recordings will be transcribed using AI software"
- "All transcription happens locally - no data is sent to external services"
- "Recordings are not used to train AI models"
- "Data remains under full control of the research team"

### Data Retention

You have complete control:
- Keep or delete original audio files
- Keep or delete transcriptions
- Keep or delete intermediate files
- No external copies exist

---

## Licensing & Legal

### OpenAI Whisper License

**Whisper is open-source software licensed under the MIT License**

Key permissions:
- ✅ Commercial use allowed
- ✅ Modification allowed
- ✅ Distribution allowed
- ✅ Private use allowed

**MIT License Summary**:
> Permission is granted to use, copy, modify, merge, publish, distribute,
> sublicense, and/or sell copies of the software, provided the copyright
> notice and permission notice are included.

Full license: [github.com/openai/whisper](https://github.com/openai/whisper/blob/main/LICENSE)

### This Pipeline

This pipeline code is a wrapper around Whisper and uses:
- **Whisper**: MIT License (OpenAI)
- **FFmpeg**: LGPL/GPL (depends on build configuration)
- **Python libraries**: Various open-source licenses

### Academic Citation

If you use this pipeline in research, please cite:

**For Whisper**:
```
Radford, A., Kim, J. W., Xu, T., Brockman, G., McLeavey, C., & Sutskever, I. (2022).
Robust Speech Recognition via Large-Scale Weak Supervision.
arXiv preprint arXiv:2212.04356.
```

**For this pipeline**:
Include in your methods section:
> Audio recordings were transcribed using a local processing pipeline based on
> OpenAI's Whisper model (small.en, 244M parameters). All transcription was
> performed locally with no data transmitted to external services. Temperature
> was set to 0.0 for reproducible results.

---

## Technical Guarantees

### What Happens During Processing

1. **Audio Preprocessing** (FFmpeg - Local):
   - Converts audio to optimal format for Whisper
   - Normalizes volume levels
   - Creates temporary files in `processed/` folder
   - All processing happens in RAM and local disk

2. **Transcription** (Whisper - Local):
   - Loads pre-downloaded model from `models/` folder
   - Processes audio through neural network on your CPU/GPU
   - Generates text output
   - No network calls made

3. **Output Generation** (Python - Local):
   - Combines transcriptions with timestamps
   - Generates JSON and TXT files
   - Creates statistics and reports
   - All saved to `output/` folder

### No Internet Communication

**After initial model download**, the pipeline:
- ❌ Does NOT connect to the internet
- ❌ Does NOT send data anywhere
- ❌ Does NOT check for updates
- ❌ Does NOT collect telemetry
- ❌ Does NOT use cloud APIs

You can verify this by:
1. Disconnecting from the internet after initial setup
2. Running the pipeline successfully offline
3. Using network monitoring tools (Wireshark, Little Snitch, etc.)

---

## Quality Assurance

### Validation Recommendations

For your research methods:

1. **Sample Validation**:
   - Manually transcribe 10-20% of recordings
   - Compare with pipeline output
   - Calculate Word Error Rate (WER)
   - Document accuracy in methods section

2. **Inter-Rater Reliability**:
   - Have multiple researchers check transcriptions
   - Use Cohen's Kappa or similar metrics
   - Report agreement scores

3. **Contextual Review**:
   - Review transcriptions while watching videos
   - Verify temporal alignment is correct
   - Check for systematic errors

### Limitations

Be aware of and report:

- **Accents**: May have slightly lower accuracy on heavy accents
- **Background noise**: Performance degrades with poor audio quality
- **Overlapping speech**: May not separate multiple speakers well
- **Technical terms**: May misrecognize domain-specific jargon
- **Whispers/mumbles**: May miss or misinterpret unclear speech

**Best Practice**: Always review automated transcriptions, especially for critical research data.

---

## Compliance & Regulations

### GDPR Compliance (European Union)

✅ **This pipeline supports GDPR compliance**:
- Data processing happens locally (Article 32: Security)
- No third-party processors involved (Article 28)
- Full data control and deletion capability (Article 17)
- No automated decision-making affecting individuals (Article 22)
- Supports data minimization principles (Article 5)

### HIPAA Compliance (United States Healthcare)

✅ **For healthcare research**:
- No Protected Health Information (PHI) transmitted externally
- All processing on covered entity's systems
- No Business Associate Agreement needed with cloud providers
- Supports Security Rule technical safeguards

### Institutional Review Board (IRB)

When describing this tool in IRB applications:

> "Audio recordings will be automatically transcribed using OpenAI's Whisper
> speech recognition model. This is an open-source AI model that runs entirely
> on our local research computers. No audio data or transcriptions are sent to
> external servers or used for training AI models. The model was pre-trained on
> publicly available data and does not learn from participant recordings."

---

## Trustworthiness

### Open Source Foundation

- **Whisper source code**: Publicly available and peer-reviewed
- **Published research**: Academic paper with methodology
- **Community validation**: Thousands of researchers use Whisper
- **Transparent**: No "black box" cloud APIs

### Auditable

You can verify the pipeline's behavior:
- Read the Python source code in `pipeline/`
- Monitor network traffic during processing
- Inspect model files in `models/`
- Review all output files

### No Vendor Lock-In

- Output formats are standard (JSON, TXT)
- Can switch to other transcription methods
- No proprietary formats
- Raw audio preserved

---

## Summary: Why This Pipeline is Scientifically Sound

✅ **Reproducible**: Deterministic processing (temperature 0.0)
✅ **Transparent**: Open-source model with published methodology
✅ **Private**: 100% local processing, no data leakage
✅ **Ethical**: Respects participant privacy and consent
✅ **Compliant**: Supports GDPR, HIPAA, IRB requirements
✅ **Documented**: Complete audit trail and metadata
✅ **Validated**: Published accuracy metrics, community-tested
✅ **Verbatim**: Preserves natural speech without interpretation

---

## Questions & Answers

**Q: Is my data sent to OpenAI?**
A: No. The model is downloaded once and runs locally. Your audio never leaves your computer.

**Q: Can OpenAI see my transcriptions?**
A: No. There is zero communication with OpenAI servers after the initial model download.

**Q: Is my data used to train AI models?**
A: No. The Whisper model is pre-trained and frozen. It does not learn from your data.

**Q: What if I have sensitive/confidential recordings?**
A: The pipeline is designed for this. Everything stays on your computer. Disconnect from the internet if desired.

**Q: How do I cite this in my research?**
A: See the "Academic Citation" section above for Whisper citation and methods description.

**Q: Can I use this for clinical/healthcare research?**
A: Yes, the local processing supports HIPAA compliance when used on secure systems.

**Q: How do I verify it's really private?**
A: Disconnect from the internet after setup and run the pipeline. It works offline.

**Q: What about IRB approval?**
A: The "Institutional Review Board" section above provides template language for IRB applications.

---

## Contact & Support

For scientific/ethical questions about using this pipeline:
- Review OpenAI Whisper documentation: [github.com/openai/whisper](https://github.com/openai/whisper)
- Consult your institution's Research Ethics Board
- Seek guidance from your Data Protection Officer

For technical implementation:
- See `USAGE.md` for practical how-to guide
- Test with sample data before processing real recordings
- Validate accuracy on your specific use case

---

**Last Updated**: 2025-11-10
**Pipeline Version**: 1.0.0
**Whisper Model**: small.en (244M parameters)
