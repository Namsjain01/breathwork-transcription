#!/usr/bin/env python3
"""
Main pipeline script for micro-phenomenological interview transcription.

This script orchestrates the complete transcription workflow:
1. Find session folders and audio/JSON pairs
2. Preprocess audio (normalize, convert format)
3. Transcribe using Whisper
4. Merge transcriptions with timestamps
5. Generate output files (TXT, JSON, report)
6. Clean up intermediate files

Usage:
    python run_pipeline.py                    # Process all sessions
    python run_pipeline.py --session NAME     # Process specific session
"""

import argparse
import shutil
from pathlib import Path
from datetime import datetime
import time

import config
import utils
import preprocess_audio
import transcribe
import merge_outputs


def process_session(session_info: dict, cleanup: bool = True) -> bool:
    """
    Process a single session.

    Args:
        session_info: Session information dict from utils.find_all_sessions()
        cleanup: Whether to delete intermediate files after processing

    Returns:
        True if successful, False otherwise
    """
    session_name = session_info['name']
    session_path = session_info['path']
    video_file = session_info['video_file']

    print(f"\n{'=' * 80}")
    print(f"Processing session: {session_name}")
    print(f"{'=' * 80}\n")

    start_time = time.time()

    # Step 1: Find audio files and match with JSON
    print("Step 1: Finding audio files and matching with timestamps...")
    paired_files, orphaned_files = utils.find_audio_json_pairs(session_path)

    print(f"  ✓ Found {len(paired_files)} files with timestamps")
    if orphaned_files:
        print(f"  ⚠ Found {len(orphaned_files)} orphaned files (no JSON timestamp)")

    if not paired_files and not orphaned_files:
        print("  ✗ No audio files found in session!")
        return False

    all_audio_files = [f['audio'] for f in paired_files] + orphaned_files

    # Step 2: Preprocess audio
    print("\nStep 2: Preprocessing audio files...")
    normalized_dir = config.PROCESSED_DIR / session_name / "normalized_audio"

    preprocessed_files = preprocess_audio.preprocess_audio_files(
        all_audio_files,
        normalized_dir,
        parallel=True
    )

    if not preprocessed_files:
        print("  ✗ Audio preprocessing failed!")
        return False

    # Step 3: Transcribe with Whisper
    print("\nStep 3: Transcribing audio with Whisper...")
    output_dir = config.OUTPUT_DIR / session_name
    utils.ensure_dir(output_dir)

    transcriber = transcribe.WhisperTranscriber(config.WHISPER_MODEL)
    transcripts = transcriber.transcribe_files(preprocessed_files, output_dir)

    if not transcripts:
        print("  ✗ Transcription failed!")
        return False

    # Step 4: Generate individual transcript files
    if config.GENERATE_INDIVIDUAL_TRANSCRIPTS:
        print("\nStep 4: Generating individual transcript files...")
        merge_outputs.generate_individual_transcripts(
            paired_files,
            orphaned_files,
            transcripts,
            output_dir
        )
        print(f"  ✓ Individual transcripts saved to: {output_dir / 'transcripts'}")

    # Step 5: Generate combined TXT
    if config.GENERATE_COMBINED_TXT:
        print("\nStep 5: Generating combined transcript (TXT)...")
        txt_file = output_dir / "combined_transcript.txt"
        merge_outputs.generate_combined_txt(
            paired_files,
            orphaned_files,
            transcripts,
            session_name,
            video_file,
            txt_file
        )
        print(f"  ✓ Combined TXT saved to: {txt_file}")

    # Step 6: Generate combined JSON
    if config.GENERATE_COMBINED_JSON:
        print("\nStep 6: Generating combined transcript (JSON)...")
        json_file = output_dir / "combined_transcript.json"
        merge_outputs.generate_combined_json(
            paired_files,
            orphaned_files,
            transcripts,
            session_name,
            video_file,
            json_file
        )
        print(f"  ✓ Combined JSON saved to: {json_file}")

    # Step 7: Generate processing report
    if config.GENERATE_PROCESSING_REPORT:
        print("\nStep 7: Generating processing report...")
        report_file = output_dir / "processing_report.txt"
        generate_processing_report(
            session_name,
            video_file,
            paired_files,
            orphaned_files,
            transcripts,
            start_time,
            report_file
        )
        print(f"  ✓ Processing report saved to: {report_file}")

    # Step 8: Cleanup intermediate files
    if cleanup and config.DELETE_INTERMEDIATE_FILES:
        print("\nStep 8: Cleaning up intermediate files...")
        if normalized_dir.exists():
            shutil.rmtree(normalized_dir)
            print(f"  ✓ Deleted: {normalized_dir}")

    # Done!
    elapsed_time = time.time() - start_time
    print(f"\n{'=' * 80}")
    print(f"✓ Session processed successfully in {elapsed_time:.1f} seconds")
    print(f"{'=' * 80}\n")

    return True


def generate_processing_report(session_name: str, video_file: Path,
                               paired_files: list, orphaned_files: list,
                               transcripts: dict, start_time: float,
                               output_file: Path) -> None:
    """Generate processing report."""
    elapsed = time.time() - start_time

    total_files = len(paired_files) + len(orphaned_files)
    successful = len(transcripts)
    total_duration = sum(utils.get_audio_duration(f['audio']) for f in paired_files if f['audio'].stem in transcripts)
    total_words = sum(utils.count_words(transcripts[f['audio'].stem]) for f in paired_files if f['audio'].stem in transcripts)
    total_chars = sum(len(transcripts[f['audio'].stem]) for f in paired_files if f['audio'].stem in transcripts)

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("=" * 80 + "\n")
        f.write("TRANSCRIPTION PROCESSING REPORT\n")
        f.write("=" * 80 + "\n")
        f.write(f"Session: {session_name}\n")
        f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Model: Whisper {config.WHISPER_MODEL} (244M parameters)\n")
        f.write("=" * 80 + "\n\n")

        f.write("FILES PROCESSED\n")
        f.write("─" * 80 + "\n")
        f.write(f"Total audio files found:        {total_files}\n")
        f.write(f"With JSON timestamps:           {len(paired_files)}\n")
        f.write(f"Orphaned (no JSON):             {len(orphaned_files)}\n")
        f.write(f"Successfully transcribed:       {successful}\n")
        f.write(f"Failed transcriptions:          {total_files - successful}\n")
        f.write(f"Success rate:                   {100 * successful / total_files:.1f}%\n\n")

        f.write("TIMING\n")
        f.write("─" * 80 + "\n")
        f.write(f"Total processing time:          {int(elapsed // 60)}m {int(elapsed % 60)}s\n")
        if successful > 0:
            f.write(f"Average per file:               {elapsed / successful:.1f}s\n")
        if total_duration > 0:
            f.write(f"Audio duration / processing:    {total_duration / elapsed:.2f}x (realtime)\n\n")

        f.write("CONTENT STATISTICS\n")
        f.write("─" * 80 + "\n")
        f.write(f"Total audio duration:           {total_duration:.1f} seconds\n")
        f.write(f"Total words transcribed:        {total_words}\n")
        f.write(f"Total characters:               {total_chars:,}\n")
        if successful > 0:
            f.write(f"Average words per recording:    {total_words // successful}\n")

        if paired_files:
            durations = [utils.get_audio_duration(f['audio']) for f in paired_files]
            f.write(f"Shortest recording:             {min(durations):.1f}s ({paired_files[durations.index(min(durations))]['audio'].name})\n")
            f.write(f"Longest recording:              {max(durations):.1f}s ({paired_files[durations.index(max(durations))]['audio'].name})\n\n")

        if paired_files and len(paired_files) > 0:
            f.write("VIDEO COVERAGE\n")
            f.write("─" * 80 + "\n")
            first_ts = paired_files[0]['timestamp_sec']
            last_ts = paired_files[-1]['timestamp_sec']
            f.write(f"First annotation timestamp:     {utils.format_timestamp(first_ts)}\n")
            f.write(f"Last annotation timestamp:      {utils.format_timestamp(last_ts)}\n")
            f.write(f"Total video span covered:       {utils.format_timestamp(last_ts - first_ts, include_milliseconds=False)} ({last_ts - first_ts:.1f} seconds)\n\n")

        f.write("OUTPUT FILES CREATED\n")
        f.write("─" * 80 + "\n")
        f.write(f"✓ {successful} individual transcript files (transcripts/*.txt)\n")
        if config.GENERATE_COMBINED_TXT:
            f.write(f"✓ combined_transcript.txt\n")
        if config.GENERATE_COMBINED_JSON:
            f.write(f"✓ combined_transcript.json\n")
        f.write(f"✓ processing_report.txt\n\n")

        f.write("SYSTEM INFO\n")
        f.write("─" * 80 + "\n")
        import platform
        import sys
        f.write(f"Operating System: {platform.system()} {platform.release()}\n")
        f.write(f"Python Version: {sys.version.split()[0]}\n")
        f.write(f"Whisper Model: {config.WHISPER_MODEL}\n")
        f.write(f"Pipeline Version: {config.PIPELINE_VERSION}\n\n")

        f.write("QUALITY NOTES\n")
        f.write("─" * 80 + "\n")
        f.write("- All transcriptions include verbatim speech (filler words preserved)\n")
        f.write(f"- Temperature: {config.TEMPERATURE} (deterministic, reproducible)\n")
        f.write(f"- Language: {config.LANGUAGE} (forced)\n")
        f.write("- No post-processing or correction applied\n\n")

        f.write("=" * 80 + "\n")
        f.write("END OF REPORT\n")
        f.write("=" * 80 + "\n")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Transcribe micro-phenomenological interview recordings"
    )
    parser.add_argument(
        '--session',
        type=str,
        help="Process specific session by name (otherwise processes all)"
    )
    parser.add_argument(
        '--no-cleanup',
        action='store_true',
        help="Keep intermediate processed audio files"
    )

    args = parser.parse_args()

    # Validate configuration
    try:
        config.validate_config()
    except Exception as e:
        print(f"✗ Configuration error: {e}")
        return 1

    # Find sessions
    print("\nScanning for sessions...")
    sessions = utils.find_all_sessions(config.INPUT_DIR)

    if not sessions:
        print("✗ No sessions found in input directory!")
        return 1

    print(f"✓ Found {len(sessions)} session(s)")

    # Filter by session name if specified
    if args.session:
        sessions = [s for s in sessions if s['name'] == args.session]
        if not sessions:
            print(f"✗ Session '{args.session}' not found!")
            return 1

    # Process each session
    cleanup = not args.no_cleanup
    success_count = 0

    for session in sessions:
        try:
            if process_session(session, cleanup=cleanup):
                success_count += 1
        except Exception as e:
            print(f"\n✗ Error processing session {session['name']}: {e}")
            import traceback
            traceback.print_exc()

    # Summary
    print(f"\n{'=' * 80}")
    print(f"PROCESSING COMPLETE")
    print(f"{'=' * 80}")
    print(f"Successfully processed: {success_count}/{len(sessions)} sessions")
    print(f"Output directory: {config.OUTPUT_DIR}")
    print(f"{'=' * 80}\n")

    return 0 if success_count == len(sessions) else 1


if __name__ == "__main__":
    exit(main())
