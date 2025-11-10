"""
Output merging module for the transcription pipeline.

This module combines transcriptions with timestamps and generates
final output files (TXT and JSON formats).
"""

from pathlib import Path
from datetime import datetime
from typing import List, Dict

import config
import utils


def generate_individual_transcripts(paired_files: List[Dict],
                                    orphaned_files: List[Path],
                                    transcripts: Dict[str, str],
                                    output_dir: Path) -> None:
    """
    Generate individual transcript files (TXT and JSON) with timestamp headers.

    Args:
        paired_files: List of paired audio/JSON file dicts
        orphaned_files: List of orphaned audio files
        transcripts: Dictionary mapping filename stems to transcribed text
        output_dir: Output directory for transcript files
    """
    transcripts_dir = output_dir / "transcripts"
    utils.ensure_dir(transcripts_dir)

    # Process paired files
    for file_info in paired_files:
        audio_file = file_info['audio']
        timestamp_sec = file_info['timestamp_sec']
        filename_stem = audio_file.stem

        # Match by filename stem
        if filename_stem not in transcripts:
            continue

        text = transcripts[filename_stem]
        duration = utils.get_audio_duration(audio_file)

        # Create TXT file with timestamp
        txt_file = transcripts_dir / f"{filename_stem}.txt"
        with open(txt_file, 'w', encoding='utf-8') as f:
            # Write timestamp header
            f.write(f"[VIDEO TIMESTAMP: {utils.format_timestamp(timestamp_sec)}]\n\n")
            # Write transcription
            f.write(text)
            f.write("\n")

        # Create JSON file with metadata
        json_file = transcripts_dir / f"{filename_stem}.json"
        json_data = {
            "audio_file": audio_file.name,
            "has_video_timestamp": True,
            "video_timestamp_sec": timestamp_sec,
            "video_timestamp_formatted": utils.format_timestamp(timestamp_sec),
            "audio_duration_sec": round(duration, 3),
            "transcription": text,
            "word_count": utils.count_words(text),
            "character_count": len(text)
        }
        utils.save_json_data(json_data, json_file)

    # Process orphaned files
    for audio_file in orphaned_files:
        filename_stem = audio_file.stem

        # Match by filename stem
        if filename_stem not in transcripts:
            continue

        text = transcripts[filename_stem]
        duration = utils.get_audio_duration(audio_file)
        creation_time = utils.get_file_creation_time(audio_file)

        # Create TXT file
        txt_file = transcripts_dir / f"{filename_stem}.txt"
        with open(txt_file, 'w', encoding='utf-8') as f:
            # Write orphan header
            f.write(f"[ORPHANED - NO VIDEO TIMESTAMP]\n")
            f.write(f"[File created: {creation_time}]\n\n")
            f.write("This recording has no matching JSON timestamp file.\n\n")
            # Write transcription
            f.write(text)
            f.write("\n")

        # Create JSON file with metadata
        json_file = transcripts_dir / f"{filename_stem}.json"
        json_data = {
            "audio_file": audio_file.name,
            "has_video_timestamp": False,
            "file_created": creation_time,
            "audio_duration_sec": round(duration, 3),
            "transcription": text,
            "word_count": utils.count_words(text),
            "character_count": len(text),
            "note": "No matching JSON timestamp file found"
        }
        utils.save_json_data(json_data, json_file)


def generate_combined_txt(paired_files: List[Dict],
                         orphaned_files: List[Path],
                         transcripts: Dict[str, str],
                         session_name: str,
                         video_file: Path,
                         output_file: Path) -> None:
    """
    Generate combined transcript in TXT format.

    Args:
        paired_files: List of paired audio/JSON file dicts
        orphaned_files: List of orphaned audio files
        transcripts: Dictionary mapping filename stems to transcribed text
        session_name: Name of the session
        video_file: Path to video file (if exists)
        output_file: Output TXT file path
    """
    with open(output_file, 'w', encoding='utf-8') as f:
        # Header
        f.write(config.HEADER_SEPARATOR + "\n")
        f.write("MICRO-PHENOMENOLOGICAL INTERVIEW TRANSCRIPT\n")
        f.write(config.HEADER_SEPARATOR + "\n")
        f.write(f"Session: {session_name}\n")
        if video_file:
            f.write(f"Video File: {video_file.name}\n")
        f.write(f"Total Recordings: {len(paired_files) + len(orphaned_files)}\n")
        f.write(f"Transcription Model: Whisper {config.WHISPER_MODEL}\n")
        f.write(f"Processing Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(config.HEADER_SEPARATOR + "\n\n\n")

        # Paired recordings
        for i, file_info in enumerate(paired_files, 1):
            audio_file = file_info['audio']
            timestamp_sec = file_info['timestamp_sec']
            filename_stem = audio_file.stem

            # Match by filename stem
            if filename_stem not in transcripts:
                continue

            text = transcripts[filename_stem]
            duration = utils.get_audio_duration(audio_file)

            f.write(config.SECTION_SEPARATOR + "\n")
            f.write(f"ANNOTATION #{i}\n")
            f.write(f"VIDEO TIMESTAMP: {utils.format_timestamp(timestamp_sec)} ({timestamp_sec} seconds)\n")
            f.write(f"AUDIO FILE: {audio_file.name}\n")
            f.write(f"DURATION: {duration:.1f} seconds\n")
            f.write(config.SECTION_SEPARATOR + "\n\n")
            f.write(text)
            f.write("\n\n\n")

        # Orphaned recordings (if any)
        if orphaned_files and any(f.stem in transcripts for f in orphaned_files):
            f.write(config.SECTION_SEPARATOR + "\n")
            f.write("ORPHANED RECORDINGS (No Video Timestamp)\n")
            f.write(config.SECTION_SEPARATOR + "\n\n")

            for audio_file in orphaned_files:
                filename_stem = audio_file.stem

                # Match by filename stem
                if filename_stem not in transcripts:
                    continue

                text = transcripts[filename_stem]
                creation_time = utils.get_file_creation_time(audio_file)
                duration = utils.get_audio_duration(audio_file)

                f.write(f"File: {audio_file.name}\n")
                f.write(f"Created: {creation_time}\n")
                f.write(f"Duration: {duration:.1f} seconds\n\n")
                f.write(text)
                f.write("\n\n")

        # Footer
        total_duration = sum(utils.get_audio_duration(f['audio']) for f in paired_files if f['audio'].stem in transcripts)
        total_words = sum(utils.count_words(transcripts[f['audio'].stem]) for f in paired_files if f['audio'].stem in transcripts)

        f.write(config.HEADER_SEPARATOR + "\n")
        f.write("END OF TRANSCRIPT\n")
        f.write(f"Total Audio Duration: {total_duration:.1f} seconds\n")
        f.write(f"Total Word Count: {total_words} words\n")
        f.write(config.HEADER_SEPARATOR + "\n")


def generate_combined_json(paired_files: List[Dict],
                          orphaned_files: List[Path],
                          transcripts: Dict[str, str],
                          session_name: str,
                          video_file: Path,
                          output_file: Path) -> None:
    """
    Generate combined transcript in JSON format.

    Args:
        paired_files: List of paired audio/JSON file dicts
        orphaned_files: List of orphaned audio files
        transcripts: Dictionary mapping filename stems to transcribed text
        session_name: Name of the session
        video_file: Path to video file (if exists)
        output_file: Output JSON file path
    """
    # Build annotations list
    annotations = []
    for i, file_info in enumerate(paired_files, 1):
        audio_file = file_info['audio']
        timestamp_sec = file_info['timestamp_sec']
        filename_stem = audio_file.stem

        # Match by filename stem
        if filename_stem not in transcripts:
            continue

        text = transcripts[filename_stem]
        duration = utils.get_audio_duration(audio_file)

        annotations.append({
            "id": i,
            "has_video_timestamp": True,
            "video_timestamp_sec": timestamp_sec,
            "video_timestamp_formatted": utils.format_timestamp(timestamp_sec),
            "audio_file": audio_file.name,
            "audio_duration_sec": round(duration, 3),
            "transcription": text,
            "word_count": utils.count_words(text),
            "character_count": len(text)
        })

    # Build orphaned recordings list
    orphaned_recordings = []
    for audio_file in orphaned_files:
        filename_stem = audio_file.stem

        # Match by filename stem
        if filename_stem not in transcripts:
            continue

        text = transcripts[filename_stem]
        duration = utils.get_audio_duration(audio_file)
        creation_time = utils.get_file_creation_time(audio_file)

        orphaned_recordings.append({
            "id": f"orphan_{len(orphaned_recordings) + 1}",
            "has_video_timestamp": False,
            "audio_file": audio_file.name,
            "file_created": creation_time,
            "audio_duration_sec": round(duration, 3),
            "transcription": text,
            "word_count": utils.count_words(text),
            "note": "No matching JSON timestamp file found"
        })

    # Calculate statistics
    total_duration = sum(a['audio_duration_sec'] for a in annotations)
    total_words = sum(a['word_count'] for a in annotations)
    total_chars = sum(a['character_count'] for a in annotations)

    # Build complete JSON structure
    data = {
        "session_metadata": {
            "session_id": session_name,
            "video_file": video_file.name if video_file else None,
            "video_file_exists": video_file.exists() if video_file else False,
            "processing_timestamp": datetime.now().isoformat(),
            "transcription_model": f"whisper-{config.WHISPER_MODEL}",
            "total_recordings": len(paired_files) + len(orphaned_files),
            "total_with_timestamps": len(annotations),
            "total_orphaned": len(orphaned_recordings),
            "pipeline_version": config.PIPELINE_VERSION
        },
        "annotations": annotations,
        "orphaned_recordings": orphaned_recordings,
        "statistics": {
            "total_audio_duration_sec": round(total_duration, 1),
            "total_audio_duration_formatted": utils.format_timestamp(total_duration, include_milliseconds=False),
            "total_words": total_words,
            "total_characters": total_chars,
            "average_annotation_duration_sec": round(total_duration / len(annotations), 1) if annotations else 0,
            "average_words_per_annotation": round(total_words / len(annotations)) if annotations else 0,
            "video_coverage": {
                "first_timestamp_sec": annotations[0]['video_timestamp_sec'] if annotations else None,
                "last_timestamp_sec": annotations[-1]['video_timestamp_sec'] if annotations else None,
                "span_sec": round(annotations[-1]['video_timestamp_sec'] - annotations[0]['video_timestamp_sec'], 3) if len(annotations) > 1 else 0,
                "span_formatted": utils.format_timestamp(annotations[-1]['video_timestamp_sec'] - annotations[0]['video_timestamp_sec'], include_milliseconds=False) if len(annotations) > 1 else "00:00:00"
            }
        }
    }

    # Save JSON
    utils.save_json_data(data, output_file)


if __name__ == "__main__":
    print("Output merge module loaded successfully")
    print("This module is meant to be called from run_pipeline.py")
