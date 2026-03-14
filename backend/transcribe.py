"""
Transcription service using OpenAI Whisper
Handles model loading and audio transcription with GPU acceleration
"""

import whisper
import os
import torch
from typing import Dict, Any, Optional

# Model cache to avoid reloading models
model_cache = {}


# Detect available hardware acceleration
def get_device():
    """
    Automatically detect and return the best available device
    Priority: CUDA (NVIDIA) > MPS (Apple Silicon) > CPU
    """
    if torch.cuda.is_available():
        device = "cuda"
        print(f"🎮 Using NVIDIA GPU (CUDA)")
        print(f"   GPU: {torch.cuda.get_device_name(0)}")
        print(
            f"   VRAM: {torch.cuda.get_device_properties(0).total_memory / 1024**3:.1f} GB"
        )
    elif hasattr(torch.backends, "mps") and torch.backends.mps.is_available():
        device = "mps"
        print(f"🍎 Using Apple Silicon GPU (MPS)")
    else:
        device = "cpu"
        print(f"💻 Using CPU (no GPU detected)")

    return device


# Global device variable
DEVICE = get_device()

AVAILABLE_MODELS = [
    {
        "name": "tiny",
        "description": "Tiny (fastest, less accurate)",
        "size_mb": 39,
        "gpu_ram_mb": 500,
    },
    {
        "name": "base",
        "description": "Base (balanced)",
        "size_mb": 74,
        "gpu_ram_mb": 1000,
    },
    {
        "name": "small",
        "description": "Small (more accurate)",
        "size_mb": 244,
        "gpu_ram_mb": 2000,
    },
    {
        "name": "medium",
        "description": "Medium (very accurate)",
        "size_mb": 769,
        "gpu_ram_mb": 5000,
    },
    {
        "name": "large-v3",
        "description": "Large v3 (best accuracy)",
        "size_mb": 1550,
        "gpu_ram_mb": 10000,
    },
]


def get_device_info():
    """Get information about the current device"""
    info = {
        "device": DEVICE,
        "device_name": None,
        "available_memory_gb": None,
    }

    if DEVICE == "cuda":
        info["device_name"] = torch.cuda.get_device_name(0)
        info["available_memory_gb"] = (
            torch.cuda.get_device_properties(0).total_memory / 1024**3
        )
    elif DEVICE == "mps":
        info["device_name"] = "Apple Silicon GPU"
        # MPS doesn't expose memory info easily
        info["available_memory_gb"] = "N/A (unified memory)"
    else:
        info["device_name"] = "CPU"
        info["available_memory_gb"] = "N/A"

    return info


def get_available_models():
    """Get list of available Whisper models"""
    return AVAILABLE_MODELS


def load_model(model_name: str = "base"):
    """Load a Whisper model with caching and GPU acceleration"""
    if model_name not in model_cache:
        print(f"Loading Whisper model: {model_name}")

        # Load model on detected device
        model = whisper.load_model(model_name, device=DEVICE)

        # Move model to device
        model = model.to(DEVICE)

        model_cache[model_name] = model
        print(f"Model {model_name} loaded successfully on {DEVICE}")

        # Show memory info for GPU
        if DEVICE == "cuda":
            memory_allocated = torch.cuda.memory_allocated(0) / 1024**2
            print(f"   VRAM allocated: {memory_allocated:.1f} MB")
        elif DEVICE == "mps":
            print(f"   GPU acceleration enabled")

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
