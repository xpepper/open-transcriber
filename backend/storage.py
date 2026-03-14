"""
Storage management for Open Transcriber
Handles file storage, deduplication, and metadata management
"""

import os
import json
import hashlib
import shutil
from datetime import datetime
from pathlib import Path

# Configuration
TRANSCRIPTIONS_DIR = Path("data/transcriptions")
UPLOADS_DIR = Path("uploads")


def ensure_directories():
    """Ensure all required directories exist"""
    TRANSCRIPTIONS_DIR.mkdir(parents=True, exist_ok=True)
    UPLOADS_DIR.mkdir(parents=True, exist_ok=True)


def get_storage_path(date_str=None):
    """Get the storage path for a specific date"""
    if date_str is None:
        date_str = datetime.now().strftime("%Y-%m-%d")
    return TRANSCRIPTIONS_DIR / date_str


def calculate_file_hash(file_path):
    """Calculate SHA256 hash of a file"""
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()


def create_transcription_folder():
    """Create a new transcription folder with date and unique ID"""
    date_str = datetime.now().strftime("%Y-%m-%d")
    date_path = get_storage_path(date_str)
    date_path.mkdir(parents=True, exist_ok=True)

    # Generate unique ID based on timestamp
    unique_id = datetime.now().strftime("%Y%m%d%H%M%S")
    transcription_path = date_path / unique_id
    transcription_path.mkdir(exist_ok=True)

    return transcription_path, unique_id


def save_transcription(
    result, audio_file_path, original_filename, model_used, language=None
):
    """Save transcription and audio file to permanent storage"""
    ensure_directories()

    # Calculate file hash for deduplication
    file_hash = calculate_file_hash(audio_file_path)

    # Check for duplicate
    existing = find_by_hash(file_hash)
    if existing:
        return existing["id"], True  # Return existing ID, is_duplicate=True

    # Create new folder
    transcription_path, transcription_id = create_transcription_folder()

    # Save audio file
    audio_extension = Path(original_filename).suffix
    audio_filename = f"audio{audio_extension}"
    audio_dest_path = transcription_path / audio_filename
    shutil.copy2(audio_file_path, audio_dest_path)

    # Prepare metadata
    metadata = {
        "id": transcription_id,
        "original_filename": original_filename,
        "audio_filename": audio_filename,
        "model_used": model_used,
        "language": language,
        "created_at": datetime.now().isoformat(),
        "file_hash": file_hash,
    }

    # Add duration if available
    if "segments" in result and len(result["segments"]) > 0:
        last_segment = result["segments"][-1]
        metadata["duration"] = last_segment.get("end", 0)

    # Add word/segment counts
    if "segments" in result:
        metadata["segment_count"] = len(result["segments"])
        metadata["word_count"] = sum(
            len(seg.get("words", [])) for seg in result["segments"]
        )

    # Get file size
    metadata["file_size_bytes"] = os.path.getsize(audio_dest_path)

    # Save transcription JSON
    transcription_data = {
        "id": transcription_id,
        "metadata": metadata,
        "segments": result.get("segments", []),
        "full_text": result.get("text", ""),
    }

    transcription_json_path = transcription_path / "transcription.json"
    with open(transcription_json_path, "w", encoding="utf-8") as f:
        json.dump(transcription_data, f, ensure_ascii=False, indent=2)

    # Save metadata separately
    metadata_path = transcription_path / "metadata.json"
    with open(metadata_path, "w", encoding="utf-8") as f:
        json.dump(metadata, f, ensure_ascii=False, indent=2)

    return transcription_id, False  # Return new ID, is_duplicate=False


def load_transcription(transcription_id):
    """Load a full transcription by ID"""
    ensure_directories()

    # Search in all date folders
    for date_folder in TRANSCRIPTIONS_DIR.iterdir():
        if not date_folder.is_dir():
            continue

        transcription_path = date_folder / transcription_id
        if transcription_path.exists():
            json_path = transcription_path / "transcription.json"
            if json_path.exists():
                with open(json_path, "r", encoding="utf-8") as f:
                    return json.load(f)

    return None


def load_metadata(transcription_id):
    """Load metadata only by ID"""
    ensure_directories()

    # Search in all date folders
    for date_folder in TRANSCRIPTIONS_DIR.iterdir():
        if not date_folder.is_dir():
            continue

        transcription_path = date_folder / transcription_id
        if transcription_path.exists():
            metadata_path = transcription_path / "metadata.json"
            if metadata_path.exists():
                with open(metadata_path, "r", encoding="utf-8") as f:
                    return json.load(f)

    return None


def get_audio_path(transcription_id):
    """Get the path to the audio file for a transcription"""
    ensure_directories()

    # Search in all date folders
    for date_folder in TRANSCRIPTIONS_DIR.iterdir():
        if not date_folder.is_dir():
            continue

        transcription_path = date_folder / transcription_id
        if transcription_path.exists():
            # Look for audio file
            for file in transcription_path.iterdir():
                if file.suffix in [".mp3", ".m4a", ".wav", ".mp4", ".mpeg"]:
                    return file

    return None


def list_all_transcriptions():
    """List all transcriptions with metadata, sorted by date (newest first)"""
    ensure_directories()

    transcriptions = []

    # Iterate through all date folders
    for date_folder in sorted(TRANSCRIPTIONS_DIR.iterdir(), reverse=True):
        if not date_folder.is_dir():
            continue

        # Iterate through all transcription folders in this date folder
        for transcription_folder in date_folder.iterdir():
            if not transcription_folder.is_dir():
                continue

            metadata_path = transcription_folder / "metadata.json"
            if metadata_path.exists():
                try:
                    with open(metadata_path, "r", encoding="utf-8") as f:
                        metadata = json.load(f)
                        transcriptions.append(metadata)
                except Exception as e:
                    print(f"Warning: Failed to load metadata from {metadata_path}: {e}")

    # Sort by created_at desc
    transcriptions.sort(key=lambda x: x.get("created_at", ""), reverse=True)

    return transcriptions


def find_by_hash(file_hash):
    """Find a transcription by file hash"""
    transcriptions = list_all_transcriptions()
    for transcription in transcriptions:
        if transcription.get("file_hash") == file_hash:
            return transcription
    return None


def delete_transcription(transcription_id):
    """Delete a transcription and its files"""
    ensure_directories()

    # Search in all date folders
    for date_folder in TRANSCRIPTIONS_DIR.iterdir():
        if not date_folder.is_dir():
            continue

        transcription_path = date_folder / transcription_id
        if transcription_path.exists():
            shutil.rmtree(transcription_path)
            return True

    return False


def save_temp_file(file):
    """Save an uploaded file to temporary storage"""
    ensure_directories()

    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    filename = f"{timestamp}_{file.filename}"
    temp_path = UPLOADS_DIR / filename

    file.save(str(temp_path))

    return temp_path


def cleanup_temp_file(file_path):
    """Remove a temporary file"""
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
    except Exception as e:
        print(f"Warning: Failed to cleanup temp file {file_path}: {e}")
