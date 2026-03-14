"""
Transcription service using OpenAI Whisper
Handles model loading and audio transcription
"""

import whisper
import os
from typing import Dict, Any, Optional

# Model cache to avoid reloading models
model_cache = {}

AVAILABLE_MODELS = [
    {"name": "tiny", "description": "Tiny (fastest, less accurate)", "size_mb": 39},
    {"name": "base", "description": "Base (balanced)", "size_mb": 74},
    {"name": "small", "description": "Small (more accurate)", "size_mb": 244},
    {"name": "medium", "description": "Medium (very accurate)", "size_mb": 769},
    {"name": "large-v3", "description": "Large v3 (best accuracy)", "size_mb": 1550},
]


def get_available_models():
    """Get list of available Whisper models"""
    return AVAILABLE_MODELS


def load_model(model_name: str = "base"):
    """Load a Whisper model with caching"""
    if model_name not in model_cache:
        print(f"Loading Whisper model: {model_name}")
        model_cache[model_name] = whisper.load_model(model_name)
        print(f"Model {model_name} loaded successfully")

    return model_cache[model_name]


def transcribe_audio(
    file_path: str, model_name: str = "base", language: Optional[str] = None
) -> Dict[str, Any]:
    """
    Transcribe an audio file using Whisper

    Args:
        file_path: Path to audio file
        model_name: Whisper model to use (tiny, base, small, medium, large-v3)
        language: Language code (e.g., 'it', 'en') or None for auto-detect

    Returns:
        Dictionary with transcription result including segments and word timestamps
    """
    print(f"Transcribing {file_path} with model {model_name}...")

    # Load model
    model = load_model(model_name)

    # Transcribe with word-level timestamps
    result = model.transcribe(
        file_path,
        word_timestamps=True,
        language=language,
        verbose=False,  # Set to True for debugging
    )

    print(f"Transcription complete: {len(result.get('segments', []))} segments")

    return result


def format_duration(seconds: float) -> str:
    """Format duration in seconds to readable string"""
    minutes = int(seconds // 60)
    secs = int(seconds % 60)
    return f"{minutes}:{secs:02d}"


def detect_language(file_path: str, model_name: str = "base") -> str:
    """
    Detect the language of an audio file

    Args:
        file_path: Path to audio file
        model_name: Whisper model to use

    Returns:
        Detected language code (e.g., 'it', 'en')
    """
    model = load_model(model_name)

    # Load audio and detect language
    audio = whisper.load_audio(file_path)
    audio = whisper.pad_or_trim(audio)
    mel = whisper.log_mel_spectrogram(audio).to(model.device)

    _, probs = model.detect_language(mel)

    # Get the language with highest probability
    detected_lang = max(probs, key=probs.get)

    return detected_lang
