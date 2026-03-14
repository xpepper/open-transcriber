# 🎓 Open Transcriber

A local web application for transcribing university lectures with synchronized audio playback and text highlighting.

## ✨ Features

- 📁 **Upload audio files** (MP3, M4A, WAV, etc.)
- 🎙️ **Local transcription** using OpenAI Whisper (no cloud API needed)
- 📝 **Timestamped transcripts** with word-level precision
- 🎧 **Audio player** with synchronized text highlighting
- 🖱️ **Click-to-jump** - click any word to jump to that moment
- 📚 **Library view** - browse all your past lectures
- 🔍 **Duplicate detection** - automatically recognizes already-transcribed files
- 🌍 **Multi-language** support (auto-detects language)

## 🚀 Quick Start

### Prerequisites

- **Python 3.8 or higher**
- **FFmpeg** (required for audio processing)
  - macOS: `brew install ffmpeg`
  - Windows: `choco install ffmpeg`
  - Ubuntu/Debian: `sudo apt install ffmpeg`

### Installation

1. **Clone and navigate to the project** (or extract the archive)
   ```bash
   cd open-transcriber
   ```

2. **Run the setup script**
   ```bash
   python setup.py
   ```
   
   This will:
   - Check Python version
   - Verify FFmpeg installation
   - Create necessary directories
   - Install Python dependencies
   - Download the "tiny" Whisper model to verify installation

3. **Start the application**
   ```bash
   python run.py
   ```

4. **Open your browser**
   ```
   http://localhost:5000
   ```

## 📖 Usage

### Transcribing a Lecture

1. Click **"+ Upload New"** button
2. Select a Whisper model (recommended: **base** for balanced speed/accuracy)
3. Drag & drop your audio file or click "Browse Files"
4. Wait for transcription to complete (time varies by file length and model)
5. Your transcription will appear in the library

### Viewing & Playback

1. Click **"View"** on any transcription in the library
2. Use the audio player controls:
   - **Play/Pause** button or press **Space**
   - **Rewind/Forward** 5 seconds or use **Arrow keys**
3. Click any word in the transcript to jump to that moment
4. Current word highlights automatically during playback

### Managing Transcriptions

- **Delete** transcriptions you no longer need
- Transcriptions are stored in `data/transcriptions/` organized by date
- Uploading the same file twice will detect the duplicate and offer to view the existing transcription

## 🎛️ Whisper Models

| Model | Size | Speed | Accuracy | Use Case |
|-------|------|-------|----------|----------|
| **Tiny** | ~39MB | ⚡⚡⚡ | ⭐ | Quick testing, English audio |
| **Base** | ~74MB | ⚡⚡ | ⭐⭐ | **Recommended** for general use |
| **Small** | ~244MB | ⚡ | ⭐⭐⭐ | Better accuracy, slower |
| **Medium** | ~769MB | 🐢 | ⭐⭐⭐⭐ | High accuracy needed |
| **Large-v3** | ~1.5GB | 🐢🐢 | ⭐⭐⭐⭐⭐ | Best accuracy, slowest |

**Tip:** Start with "base" model. It provides good accuracy and speed for most lecture content.

## 📂 Project Structure

```
open-transcriber/
├── backend/              # Python backend
│   ├── app.py           # Flask application
│   ├── transcribe.py    # Whisper integration
│   ├── storage.py       # File management
│   └── utils.py         # Helper functions
├── frontend/            # Web interface
│   ├── static/
│   │   ├── css/styles.css
│   │   └── js/
│   │       ├── app.js
│   │       └── player.js
│   └── templates/
│       └── index.html
├── data/                # Stored transcriptions
│   └── transcriptions/
│       └── 2025-03-14/  # Organized by date
├── examples/            # Example audio files
├── uploads/             # Temporary upload location
├── requirements.txt
├── setup.py             # Installation script
├── run.py               # Application entry point
└── README.md
```

## 🌐 Browser Compatibility

- ✅ Chrome/Edge (recommended)
- ✅ Firefox
- ✅ Safari
- ⚠️ Older browsers may have limited support

## 💾 Data Storage

Transcriptions are stored locally in JSON format:

```
data/transcriptions/
└── YYYY-MM-DD/
    └── <transcription-id>/
        ├── transcription.json  # Full transcript with timestamps
        ├── metadata.json       # Metadata (duration, language, etc.)
        └── audio.<ext>         # Original audio file
```

**Note:** Both transcriptions and original audio files are preserved.

## 🔧 Troubleshooting

### FFmpeg not found
```bash
# macOS
brew install ffmpeg

# Windows (with Chocolatey)
choco install ffmpeg

# Ubuntu/Debian
sudo apt update && sudo apt install ffmpeg
```

### Port 5000 already in use
Edit `run.py` and change the port:
```python
app.run(host='127.0.0.1', port=5001, debug=True)
```

### Transcription is slow
- Try a smaller/faster model (tiny or base)
- Ensure you have sufficient RAM (8GB+ recommended)
- Close other applications to free up resources

### Poor transcription accuracy
- Use a larger model (small, medium, or large-v3)
- Ensure audio quality is good
- Try specifying the language manually if auto-detection is wrong

### Out of memory errors
- Use a smaller model
- Process shorter audio files
- Close other applications

## 🎯 Keyboard Shortcuts

- **Space** - Play/Pause
- **← (Left Arrow)** - Rewind 5 seconds
- **→ (Right Arrow)** - Forward 5 seconds

## 📊 System Requirements

**Minimum:**
- Python 3.8+
- 4GB RAM
- 2GB free disk space
- FFmpeg installed

**Recommended:**
- 8GB+ RAM
- SSD for faster model loading
- 4GB+ free disk space (for larger models)

## 🔒 Privacy

- **100% local** - all processing happens on your computer
- **No cloud services** - no data leaves your machine
- **No internet required** after initial setup
- **No tracking** or analytics

## 📝 License

This project is open source and available for personal use.

## 🤝 Support

For issues or questions:
1. Check the Troubleshooting section above
2. Ensure FFmpeg is properly installed
3. Verify Python version (3.8+)
4. Try running `python setup.py` to verify your environment

## 🎉 Enjoy transcribing your lectures!

Built with ❤️ for students who want to review their lectures effectively.
