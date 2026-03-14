"""
Utility functions for Open Transcriber
"""

import os
from datetime import datetime


def format_duration(seconds: float) -> str:
    """Format duration in seconds to readable string"""
    if not seconds:
        return "0:00"

    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)

    if hours > 0:
        return f"{hours}:{minutes:02d}:{secs:02d}"
    else:
        return f"{minutes}:{secs:02d}"


def format_date(date_string: str) -> str:
    """Format ISO date string to readable format"""
    try:
        dt = datetime.fromisoformat(date_string)
        return dt.strftime("%b %d, %Y")
    except:
        return date_string


def format_datetime(date_string: str) -> str:
    """Format ISO datetime string to readable format"""
    try:
        dt = datetime.fromisoformat(date_string)
        return dt.strftime("%b %d, %Y at %I:%M %p")
    except:
        return date_string


def get_file_extension(filename: str) -> str:
    """Get file extension from filename"""
    return os.path.splitext(filename)[1].lower()


def is_audio_file(filename: str) -> bool:
    """Check if file is an audio file based on extension"""
    audio_extensions = [".mp3", ".m4a", ".wav", ".mp4", ".mpeg", ".mpg", ".oga", ".ogg"]
    return get_file_extension(filename) in audio_extensions


def format_file_size(bytes_size: int) -> str:
    """Format file size in bytes to readable string"""
    size = float(bytes_size)
    for unit in ["B", "KB", "MB", "GB"]:
        if size < 1024.0:
            return f"{size:.1f} {unit}"
        size /= 1024.0
    return f"{size:.1f} TB"


def get_language_name(code: str) -> str:
    """Get full language name from language code"""
    language_map = {
        "en": "English",
        "it": "Italian",
        "es": "Spanish",
        "fr": "French",
        "de": "German",
        "pt": "Portuguese",
        "ru": "Russian",
        "zh": "Chinese",
        "ja": "Japanese",
        "ko": "Korean",
        "ar": "Arabic",
        "hi": "Hindi",
    }
    return language_map.get(code, code.upper())


def safe_filename(filename: str) -> str:
    """Make filename safe for filesystem"""
    # Remove any directory components
    filename = os.path.basename(filename)

    # Replace unsafe characters
    unsafe_chars = '<>:"/\\|?*'
    for char in unsafe_chars:
        filename = filename.replace(char, "_")

    return filename
