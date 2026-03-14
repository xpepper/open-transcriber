#!/usr/bin/env python3
"""
Open Transcriber - Setup Script
Installs dependencies and verifies the environment.
"""

import subprocess
import sys
import os


def check_python_version():
    """Check if Python version is 3.8 or higher"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        print(f"   Current version: {sys.version}")
        sys.exit(1)
    print(f"✅ Python version: {sys.version_info.major}.{sys.version_info.minor}")


def check_ffmpeg():
    """Check if FFmpeg is installed"""
    try:
        result = subprocess.run(["ffmpeg", "-version"], capture_output=True, text=True)
        if result.returncode == 0:
            version_line = result.stdout.split("\n")[0]
            print(f"✅ FFmpeg installed: {version_line}")
            return True
    except FileNotFoundError:
        pass
    print("❌ FFmpeg not found")
    print("   Install with:")
    print("   macOS: brew install ffmpeg")
    print("   Windows: choco install ffmpeg")
    print("   Ubuntu/Debian: sudo apt install ffmpeg")
    return False


def install_dependencies():
    """Install Python dependencies"""
    print("\n📦 Installing Python dependencies...")
    try:
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "-r", "requirements.txt"]
        )
        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to install dependencies")
        return False


def create_directories():
    """Create necessary directories"""
    directories = [
        "data/transcriptions",
        "uploads",
        "frontend/static/css",
        "frontend/static/js",
        "frontend/templates",
    ]

    print("\n📁 Creating directories...")
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"   Created: {directory}/")
    print("✅ Directories created")


def verify_whisper():
    """Verify Whisper can be imported"""
    print("\n🎙️  Verifying Whisper installation...")
    try:
        import whisper

        print(f"✅ Whisper {whisper.__version__} installed")

        # Try to load the smallest model to verify everything works
        print("   Testing model download (may take a moment)...")
        model = whisper.load_model("tiny")
        print("✅ Whisper model test successful")
        return True
    except ImportError as e:
        print(f"❌ Failed to import Whisper: {e}")
        return False
    except Exception as e:
        print(f"⚠️  Whisper verification warning: {e}")
        return True


def main():
    print("=" * 60)
    print("🎓 Open Transcriber - Setup")
    print("=" * 60)

    check_python_version()
    ffmpeg_ok = check_ffmpeg()
    create_directories()

    if not ffmpeg_ok:
        print("\n⚠️  Please install FFmpeg before continuing")
        sys.exit(1)

    if not install_dependencies():
        sys.exit(1)

    if not verify_whisper():
        print("\n⚠️  Whisper verification failed, but continuing...")

    print("\n" + "=" * 60)
    print("✅ Setup complete!")
    print("=" * 60)
    print("\n🚀 Run the application with:")
    print("   python run.py")
    print("\n   Then open http://localhost:5000 in your browser")
    print("=" * 60)


if __name__ == "__main__":
    main()
