"""
Transcription module using OpenAI Whisper.

This module handles loading the Whisper model and transcribing audio files.
"""

from pathlib import Path
from typing import List, Dict, Optional
import whisper

import config
import utils


class WhisperTranscriber:
    """Wrapper class for Whisper transcription."""

    def __init__(self, model_name: str = None):
        """
        Initialize Whisper transcriber.

        Args:
            model_name: Whisper model to use (defaults to config.WHISPER_MODEL)
        """
        self.model_name = model_name or config.WHISPER_MODEL
        self.model = None

    def load_model(self):
        """Load the Whisper model."""
        if self.model is None:
            print(f"Loading Whisper model '{self.model_name}'...")
            print(f"(This may take a moment on first run while downloading the model)")
            self.model = whisper.load_model(self.model_name)
            print(f"✓ Model loaded successfully")

    def transcribe_file(self, audio_file: Path) -> Optional[str]:
        """
        Transcribe a single audio file.

        Args:
            audio_file: Path to audio file

        Returns:
            Transcribed text or None if error
        """
        if self.model is None:
            self.load_model()

        try:
            # Transcribe with Whisper
            result = self.model.transcribe(
                str(audio_file),
                language=config.LANGUAGE,
                task=config.TASK,
                temperature=config.TEMPERATURE,
                verbose=config.VERBOSE,
                word_timestamps=False,  # We have video timestamps already
            )

            # Extract text
            text = result["text"].strip()
            return text

        except Exception as e:
            print(f"Error transcribing {audio_file.name}: {e}")
            return None

    def transcribe_files(self, audio_files: List[Path],
                        output_dir: Path) -> Dict[Path, str]:
        """
        Transcribe multiple audio files.

        Args:
            audio_files: List of audio file paths
            output_dir: Directory to save individual transcripts

        Returns:
            Dictionary mapping audio file paths (by filename stem) to transcribed text
        """
        utils.ensure_dir(output_dir)

        # Load model once
        self.load_model()

        transcripts = {}
        total = len(audio_files)

        print(f"\nTranscribing {total} audio files...")

        for i, audio_file in enumerate(audio_files, 1):
            print(f"  [{i}/{total}] {audio_file.name}...", end=" ", flush=True)

            # Transcribe
            text = self.transcribe_file(audio_file)

            if text:
                # Key by filename stem (without extension and path) for easier matching
                transcripts[audio_file.stem] = text

                print(f"✓ ({len(text)} chars, {utils.count_words(text)} words)")
            else:
                print(f"✗ Failed")

        print(f"\n✓ Successfully transcribed {len(transcripts)}/{total} files")

        return transcripts


if __name__ == "__main__":
    # Test transcription
    print("Testing Whisper transcription...")

    # Find test session
    sessions = utils.find_all_sessions(config.INPUT_DIR)
    if not sessions:
        print("No sessions found!")
        exit(1)

    session = sessions[0]
    print(f"\nTesting with session: {session['name']}")

    # Find audio files
    paired, orphaned = utils.find_audio_json_pairs(session['path'])
    if not paired:
        print("No audio files found!")
        exit(1)

    # Test on first file only
    test_file = paired[0]['audio']
    print(f"\nTest transcription: {test_file.name}")

    # Create transcriber
    transcriber = WhisperTranscriber()
    transcriber.load_model()

    # Transcribe
    text = transcriber.transcribe_file(test_file)

    if text:
        print(f"\n✓ Transcription successful!")
        print(f"\nTranscribed text:")
        print(f"─" * 80)
        print(text)
        print(f"─" * 80)
        print(f"\nStats:")
        print(f"  Characters: {len(text)}")
        print(f"  Words: {utils.count_words(text)}")
    else:
        print("\n✗ Transcription failed!")
