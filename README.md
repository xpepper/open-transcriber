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

## ❓ Frequently Asked Questions

### Do I need an internet connection?

- **For setup:** Yes, to download Python packages and Whisper models
- **For transcribing:** No, everything runs locally after setup
- **For browser:** No, the application runs on your local machine

### How accurate is the transcription?

Accuracy depends on several factors:
- **Audio quality** - Clear, noise-free recordings work best
- **Model size** - Larger models (medium, large-v3) are more accurate
- **Language** - Works best with clear speech
- **Background noise** - Minimize noise for best results

**Typical accuracy:**
- Base model: ~85-95% for clear speech
- Large-v3 model: ~95-98% for clear speech

### Can I transcribe other languages besides Italian?

Yes! Whisper supports 99 languages including:
- English, Italian, Spanish, French, German
- Chinese, Japanese, Korean, Arabic
- And many more

The language is auto-detected, but accuracy is best for the languages listed above.

### How long does transcription take?

Approximate times for a 10-minute audio file:
- **Tiny model:** ~1 minute
- **Base model:** ~2-3 minutes (recommended)
- **Small model:** ~4-5 minutes
- **Medium model:** ~8-10 minutes
- **Large-v3 model:** ~15-20 minutes

**Tip:** Use the base model for best balance of speed and accuracy.

### Can I edit the transcription?

Not directly in the current version, but you can:
- Export the JSON file from `data/transcriptions/`
- Edit it in a text editor
- The transcription is stored as plain text in the JSON file

Future versions may include an edit feature.

### Where are my transcriptions stored?

In the `data/transcriptions/` folder, organized by date:
```
data/transcriptions/
└── 2025-03-14/
    └── <transcription-id>/
        ├── transcription.json  # Full transcript with timestamps
        ├── metadata.json       # File information
        └── audio.m4a          # Original audio file
```

Both the transcript and original audio are preserved.

### Can I use this on multiple computers?

Yes, but:
- Each computer needs its own installation
- Transcriptions are stored locally (not synced)
- You can copy the `data/transcriptions/` folder between computers
- Both computers need the same Whisper models installed

### Is my data private?

Yes! 100% private:
- All processing happens on your computer
- No data is sent to the cloud
- No internet connection needed after setup
- No tracking or analytics
- Your lectures never leave your machine

### What audio formats are supported?

Supported formats include:
- **MP3** - Most common
- **M4A** - Apple devices
- **WAV** - Uncompressed audio
- **MP4** - Audio from video files
- **OGG, WEBM** - Other formats

### Can I transcribe video files?

Not directly. You need to:
1. Extract audio from video first
2. Save as MP3/M4A/WAV
3. Then upload to Open Transcriber

**Tools to extract audio:**
- macOS: Use QuickTime or online converters
- Windows: Use VLC Media Player → Convert/Save
- Online: Search for "video to audio converter"

### How do I backup my transcriptions?

Simply copy the entire `data/transcriptions/` folder:
- **macOS:** Copy to external drive or cloud storage
- **Windows:** Copy to USB drive or backup service
- The folder contains all transcriptions and original audio

**Tip:** Regular backups are recommended as these are your lecture notes!

### Can I share transcriptions with others?

Yes! To share a transcription:
1. Navigate to `data/transcriptions/YYYY-MM-DD/<id>/`
2. Share the `transcription.json` file
3. The recipient can view it in any text editor
4. To share with audio, include the `audio.m4a` file too

The JSON format is human-readable and can be opened in any text editor.

### What if transcription fails or is inaccurate?

Try these solutions:
1. **Use a larger model** (small, medium, or large-v3)
2. **Improve audio quality** - reduce background noise
3. **Specify language manually** - if auto-detect is wrong
4. **Split long recordings** into shorter segments
5. **Check audio format** - ensure it's not corrupted

### Can I use this for commercial purposes?

This tool is intended for personal educational use. For commercial use:
- Check OpenAI Whisper's license
- Consider your intended use case
- Ensure compliance with your institution's policies

## 🚀 Installation Guide

Follow the step-by-step guide for your operating system:

---

### 🍎 macOS Installation

#### Step 1: Install Homebrew (if not already installed)

Open **Terminal** and run:

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

**Press Enter** when prompted and enter your password if asked.

#### Step 2: Install FFmpeg

In **Terminal**, run:

```bash
brew install ffmpeg
```

**Verification:** Type `ffmpeg -version` - you should see version information.

#### Step 3: Verify Python Installation

macOS comes with Python, but let's ensure you have Python 3.8+:

```bash
python3 --version
```

You should see **Python 3.8.0** or higher.

**Note:** Always use `python3` (not `python`) on macOS.

#### Step 4: Navigate to Project Directory

```bash
cd /path/to/open-transcriber
```

**Example:** If you extracted the file to Downloads:
```bash
cd ~/Downloads/open-transcriber
```

Or if you cloned from git:
```bash
cd ~/Documents/workspace/ai/open-transcriber
```

#### Step 5: Run Setup Script

```bash
python3 setup.py
```

This will:
- ✅ Verify Python version
- ✅ Check FFmpeg installation
- ✅ Create necessary directories
- ✅ Install Python packages (Flask, Whisper, etc.)
- ✅ Download the "tiny" Whisper model (~39MB)

**Expected output:**
```
============================================================
🎓 Open Transcriber - Setup
============================================================
✅ Python version: 3.12
✅ FFmpeg installed
📦 Installing Python dependencies...
✅ Dependencies installed successfully
🎙️  Verifying Whisper installation...
✅ Whisper installed successfully
============================================================
✅ Setup complete!
============================================================
```

**If setup fails:**
- Make sure you're in the correct directory (check with `ls`)
- Ensure you have internet connection (for downloading packages)
- Try running with sudo if you get permission errors: `sudo python3 setup.py`

#### Step 6: Start the Application

```bash
python3 run.py
```

**Expected output:**
```
============================================================
🎓 Open Transcriber
============================================================

🚀 Starting server...
   Open http://localhost:5000 in your browser

   Press Ctrl+C to stop the server
============================================================
```

**Keep this Terminal window open!** The server needs to keep running.

#### Step 7: Open in Browser

Open Safari or Chrome and navigate to:

```
http://localhost:5000
```

You should see the Open Transcriber interface!

---

### 🪟 Windows Installation

#### Step 1: Install Python 3

1. Go to **[python.org](https://www.python.org/downloads/)**
2. Click **Download Python 3.12.x** (or latest 3.x version)
3. Run the installer

**IMPORTANT:** During installation:
- ✅ **Check the box** "Add Python to PATH"
- Click "Install Now"

4. **Verify installation:** Open **Command Prompt** and type:
   ```cmd
   python --version
   ```
   
   You should see **Python 3.8.0** or higher.
   
   **Note:** On Windows, use `python` (not `python3`).

#### Step 2: Install FFmpeg

You have two options:

**Option A: Using Chocolatey (Recommended)**

1. Open **Command Prompt as Administrator**
   - Press `Windows Key`, type "cmd"
   - Right-click "Command Prompt" → "Run as administrator"

2. Install Chocolatey (if not already installed):
   ```cmd
   setx PATH "%PATH%;%ALLUSERSPROFILE%\chocolatey\bin"
   ```
   Then run:
   ```cmd
   powershell -Command "Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -s 256; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))"
   ```

3. Install FFmpeg:
   ```cmd
   choco install ffmpeg
   ```

4. **Restart Command Prompt** to refresh PATH

**Option B: Manual Installation**

1. Download FFmpeg from **[ffmpeg.org](https://ffmpeg.org/download.html#build-windows)**
2. Extract the ZIP file
3. Move the extracted folder to `C:\ffmpeg`
4. Add `C:\ffmpeg\bin` to your system PATH:
   - Press `Windows Key`, type "environment variables"
   - Click "Edit the system environment variables"
   - Click "Environment Variables"
   - Under "System variables", find "Path" and click "Edit"
   - Click "New" and add: `C:\ffmpeg\bin`
   - Click OK on all dialog boxes
5. **Restart Command Prompt**

**Verification:** In Command Prompt, type:
```cmd
ffmpeg -version
```

You should see version information.

#### Step 3: Navigate to Project Directory

In **Command Prompt**, navigate to where you extracted/opened the project:

```cmd
cd C:\path\to\open-transcriber
```

**Example:** If you extracted to Downloads:
```cmd
cd %USERPROFILE%\Downloads\open-transcriber
```

**Tip:** You can type `cd ` (with a space) and then drag the folder into the Command Prompt window to auto-fill the path.

#### Step 4: Run Setup Script

```cmd
python setup.py
```

This will:
- ✅ Verify Python version
- ✅ Check FFmpeg installation
- ✅ Create necessary directories
- ✅ Install Python packages (Flask, Whisper, etc.)
- ✅ Download the "tiny" Whisper model (~39MB)

**Expected output:**
```
============================================================
🎓 Open Transcriber - Setup
============================================================
✅ Python version: 3.12
✅ FFmpeg installed
📦 Installing Python dependencies...
✅ Dependencies installed successfully
🎙️  Verifying Whisper installation...
✅ Whisper installed successfully
============================================================
✅ Setup complete!
============================================================
```

**If setup fails:**
- Make sure you're in the correct directory (check with `dir`)
- Ensure you have internet connection
- If you see "Access denied", run Command Prompt as Administrator

#### Step 5: Start the Application

```cmd
python run.py
```

**Expected output:**
```
============================================================
🎓 Open Transcriber
============================================================

🚀 Starting server...
   Open http://localhost:5000 in your browser

   Press Ctrl+C to stop the server
============================================================
```

**Keep this Command Prompt window open!** The server needs to keep running.

#### Step 6: Open in Browser

Open Edge or Chrome and navigate to:

```
http://localhost:5000
```

You should see the Open Transcriber interface!

---

### 🐧 Linux (Ubuntu/Debian) Installation

#### Step 1: Install FFmpeg

```bash
sudo apt update
sudo apt install ffmpeg
```

#### Step 2: Verify Python

```bash
python3 --version
```

#### Step 3: Navigate and Setup

```bash
cd /path/to/open-transcriber
python3 setup.py
python3 run.py
```

Then open `http://localhost:5000` in your browser.

---

### ✅ Installation Verification

After installation, verify everything works:

1. **Check the application is running:**
   - Open your browser to `http://localhost:5000`
   - You should see the Open Transcriber interface with a library view

2. **Test with example audio:**
   - Click "+ Upload New"
   - Select "base" model
   - Navigate to `examples/small-example.m4a`
   - Wait for transcription (~30-60 seconds)
   - Click "View" to see the synchronized player

3. **Verify all features:**
   - ✅ Audio plays correctly
   - ✅ Words highlight during playback
   - ✅ Clicking words jumps to that moment
   - ✅ Keyboard shortcuts work (Space, ←, →)

---

### 🔄 Starting the Application (After Initial Installation)

**Once setup is complete, you only need to do this each time:**

#### macOS/Linux:
```bash
cd /path/to/open-transcriber
python3 run.py
```

#### Windows:
```cmd
cd C:\path\to\open-transcriber
python run.py
```

Then open `http://localhost:5000` in your browser.

---

### 🛑 Stopping the Application

To stop the server:
- Go to the Terminal/Command Prompt window where it's running
- Press **Ctrl+C**
- The window will show "Server has stopped"

You can then close the window.

---

## ⚡ GPU Acceleration (Optional)

Open Transcriber automatically uses GPU acceleration when available, providing **3-10x faster** transcription speeds.

### 🎮 Supported Hardware

| Hardware Type | Supported | Performance Gain | Status |
|---------------|-----------|------------------|--------|
| **NVIDIA GPU** | ✅ Yes | **5-10x faster** | CUDA |
| **Apple Silicon** | ✅ Yes | **3-5x faster** | MPS (M1/M2/M3/M4) |
| **AMD GPU** | ⚠️ Limited | 1.5-2x faster | ROCm (Linux only) |
| **Intel Arc** | ⚠️ Limited | 1.5-2x faster | OneAPI (Linux only) |
| **CPU** | ✅ Default | Baseline | Any system |

### 🍎 Apple Silicon (M1/M2/M3/M4) - macOS

**Automatic!** GPU acceleration works out of the box on Apple Silicon Macs.

**Verification:**
```bash
# Check if MPS is available
python3 -c "import torch; print('MPS available:', hasattr(torch.backends, 'mps') and torch.backends.mps.is_available())"
```

**Expected output:** `MPS available: True`

**What you'll see:**
```
Loading Whisper model: base
🍎 Using Apple Silicon GPU (MPS)
Model base loaded successfully on mps
   GPU acceleration enabled
```

**Performance:**
- Base model: ~2-3 minutes for 10-minute audio (vs ~8-10 minutes on CPU)
- Large-v3 model: ~10-15 minutes for 10-minute audio (vs ~60+ minutes on CPU)

**⚠️ Apple Silicon Limitations:**

MPS (Apple Silicon GPU) has a known limitation with **word-level timestamps** for larger models (small, medium, large-v3):

- **Tiny & Base models:** Work perfectly with word timestamps ✅
- **Small/Medium/Large models:** May need CPU fallback for word alignment

**What happens:**
- Transcription will succeed with GPU acceleration
- Word timestamps may use CPU fallback (slower but works)
- You'll see a message: "Falling back to CPU for alignment"

**Workaround if needed:**
If you encounter errors with large models, you can:
1. Use the "tiny" or "base" model (recommended for most use cases)
2. Accept CPU fallback (slower but complete)
3. Disable word timestamps (segment-level timestamps still work)

**Recommended:** Use "base" model for best balance of speed, accuracy, and features on Apple Silicon.

---

### 🪟 NVIDIA GPU - Windows

**Requires:** NVIDIA GeForce, RTX, or Quadro GPU with 4GB+ VRAM

#### Step 1: Install NVIDIA CUDA Toolkit

1. **Check your GPU:**
   ```cmd
   nvidia-smi
   ```
   You should see your GPU details and CUDA version.

2. **Download CUDA Toolkit:**
   - Go to [NVIDIA CUDA Downloads](https://developer.nvidia.com/cuda-downloads)
   - Select: Windows → x86_64 → 11 → exe (local)
   - Install with default options

3. **Verify installation:**
   ```cmd
   nvcc --version
   ```

#### Step 2: Install PyTorch with CUDA Support

**Uninstall current PyTorch (if already installed):**
```cmd
pip uninstall torch torchaudio
```

**Install PyTorch with CUDA:**
```cmd
# For CUDA 12.1 (recommended)
pip install torch==2.10.0+cu121 torchaudio==2.10.0+cu121 --index-url https://download.pytorch.org/whl/cu121
```

#### Step 3: Verify GPU Support

```cmd
python -c "import torch; print('CUDA available:', torch.cuda.is_available()); print('GPU:', torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'N/A')"
```

**Expected output:**
```
CUDA available: True
GPU: NVIDIA GeForce RTX 3060
```

#### Step 4: Run Open Transcriber

```cmd
python run.py
```

**What you'll see:**
```
Loading Whisper model: base
🎮 Using NVIDIA GPU (CUDA)
   GPU: NVIDIA GeForce RTX 3060
   VRAM: 12.0 GB
Model base loaded successfully on cuda
   VRAM allocated: 950.0 MB
```

**Performance:**
- Base model: ~1-2 minutes for 10-minute audio
- Large-v3 model: ~5-8 minutes for 10-minute audio

---

### 🐧 NVIDIA GPU - Linux

Similar to Windows but use Linux CUDA downloads:

```bash
# Install PyTorch with CUDA
pip install torch==2.10.0+cu121 torchaudio==2.10.0+cu121 --index-url https://download.pytorch.org/whl/cu121
```

---

### 💡 GPU Performance Tips

1. **VRAM Requirements by Model:**
   - Tiny: ~500MB VRAM
   - Base: ~1GB VRAM
   - Small: ~2GB VRAM
   - Medium: ~5GB VRAM
   - Large-v3: ~10GB VRAM

2. **Choose the right model for your GPU:**
   - **GTX 1650 or lower** (4GB VRAM): Use tiny or base
   - **RTX 3060 or better** (8-12GB VRAM): Use small or medium
   - **RTX 3080 or better** (10GB+ VRAM): Use any model including large-v3

3. **Maximize GPU performance:**
   - Close other applications using GPU
   - Use a smaller model if you run out of VRAM
   - For long audio files, consider splitting into shorter segments

4. **Troubleshooting GPU issues:**
   ```bash
   # Check if GPU is detected
   python -c "import torch; print(torch.cuda.is_available())"
   
   # Check GPU memory (Windows)
   nvidia-smi
   
   # If False, reinstall PyTorch with CUDA support
   ```

---

### 📊 Performance Comparison

10-minute audio file transcription time:

| Model | CPU | Apple Silicon | NVIDIA RTX 3060 |
|-------|-----|---------------|-----------------|
| **Tiny** | ~1 min | ~30s | ~15s |
| **Base** | ~8 min | ~2.5 min | ~1.5 min |
| **Small** | ~25 min | ~6 min | ~3 min |
| **Medium** | ~60 min | ~15 min | ~7 min |
| **Large-v3** | ~90+ min | ~20 min | ~10 min |

*Times are approximate and vary by hardware*

---

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

### Platform-Specific Issues

#### macOS Issues

**"command not found: python3"**
- Python is not installed or not in PATH
- Install from [python.org](https://www.python.org/downloads/macos/)
- Or use Homebrew: `brew install python3`

**"command not found: brew"**
- Homebrew is not installed
- Install from [brew.sh](https://brew.sh)
- Run the install command in Terminal

**"Permission denied" when running setup.py**
- Run with sudo: `sudo python3 setup.py`
- Enter your macOS password when prompted

**FFmpeg not found after installing with Homebrew**
- Restart your Terminal
- Run: `hash -r`
- Then try: `ffmpeg -version`

**Port 5000 already in use (AirPlay often uses this port)**
- Edit `run.py` and change port 5000 to 5001:
  ```python
  app.run(host='127.0.0.1', port=5001, debug=True)
  ```
- Then navigate to `http://localhost:5001`

**Application runs but browser shows "Unable to connect"**
- Check that Terminal shows server is running
- Try: `http://127.0.0.1:5000` instead of `http://localhost:5000`
- Check firewall settings (System Preferences → Security & Privacy → Firewall)

---

#### Windows Issues

**"python is not recognized as an internal or external command"**
- Python is not in your PATH
- Reinstall Python and **check "Add Python to PATH"**
- Or manually add Python to PATH:
  1. Search for "Environment Variables" in Windows
  2. Click "Edit the system environment variables"
  3. Click "Environment Variables"
  4. Under "System variables", find "Path" and click "Edit"
  5. Add Python's installation path (usually `C:\Python312\` and `C:\Python312\Scripts\`)
  6. Click OK and **restart Command Prompt**

**"ffmpeg is not recognized as an internal or external command"**
- FFmpeg is not in your PATH
- Reinstall FFmpeg and ensure it's added to PATH (see Step 2 in Windows installation)
- Restart Command Prompt after installation
- Verify with: `ffmpeg -version`

**"Access denied" when running setup.py**
- Right-click Command Prompt and select "Run as administrator"
- Then run: `python setup.py`

**"pip is not recognized"**
- Python was not added to PATH during installation
- Reinstall Python with "Add Python to PATH" checked
- Or use `python -m pip` instead of `pip`

**ModuleNotFoundError: No module named 'flask'**
- Dependencies were not installed
- Run: `python setup.py` again
- Or manually install: `pip install -r requirements.txt`

**Firewall blocking the application**
- When you see Windows Firewall alert, click "Allow access"
- Or manually allow Python in Windows Defender Firewall:
  1. Search for "Windows Defender Firewall"
  2. Click "Allow an app through Windows Defender Firewall"
  3. Click "Change settings" → "Allow another app"
  4. Browse to `python.exe` and add it

**Server starts but browser shows "This site can't be reached"**
- Try `http://127.0.0.1:5000` instead of `http://localhost:5000`
- Check Windows Firewall settings
- Temporarily disable antivirus to test

---

### General Issues

#### FFmpeg not found
**Install FFmpeg for your system:**

**macOS:**
```bash
brew install ffmpeg
```

**Windows (Chocolatey):**
```cmd
choco install ffmpeg
```

**Windows (Manual):**
1. Download from [ffmpeg.org](https://ffmpeg.org/download.html)
2. Add to PATH as shown in Windows installation guide

**Ubuntu/Debian:**
```bash
sudo apt update && sudo apt install ffmpeg
```

**Verification:**
```bash
ffmpeg -version
```

---

#### Port 5000 already in use

**Symptoms:** Error message "Address already in use" or "Port 5000 is already in use"

**Solutions:**

1. **Use a different port** - Edit `run.py`:
   ```python
   app.run(host='127.0.0.1', port=5001, debug=True)
   ```
   Then navigate to `http://localhost:5001`

2. **Kill the process using port 5000:**
   
   **macOS/Linux:**
   ```bash
   lsof -ti:5000 | xargs kill -9
   ```
   
   **Windows:**
   ```cmd
   netstat -ano | findstr :5000
   taskkill /PID <PID_NUMBER> /F
   ```

---

#### Transcription is slow

**Solutions:**
- Use a smaller/faster model (tiny or base)
- Ensure you have sufficient RAM (8GB+ recommended)
- Close other applications to free up resources
- On Windows, close unnecessary background apps
- Process shorter audio files (split long lectures into smaller parts)

**Expected transcription times (approximate):**
- 10-minute file with "base" model: ~2-3 minutes
- 10-minute file with "tiny" model: ~1 minute
- 10-minute file with "large-v3" model: ~10-15 minutes

---

#### Poor transcription accuracy

**Solutions:**
- Use a larger model (small, medium, or large-v3)
- Ensure audio quality is good (clear recording, minimal background noise)
- Try specifying the language manually if auto-detection is wrong
- For Italian lectures, the model should auto-detect correctly
- Position microphone closer to speaker for better audio quality

---

#### Out of memory errors

**Symptoms:** Application crashes, "MemoryError", or system becomes very slow

**Solutions:**
- Use a smaller model (tiny or base)
- Process shorter audio files
- Close other applications
- Restart your computer before transcribing long files
- On Windows, check Task Manager for memory usage
- On macOS, check Activity Monitor for memory usage

---

#### Setup script fails

**Symptoms:** Error during `python setup.py`

**Solutions:**

1. **Check internet connection** - Required for downloading packages
2. **Verify Python version:** `python3 --version` (macOS) or `python --version` (Windows)
3. **Manually install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
4. **Install FFmpeg first** if setup fails at FFmpeg check
5. **Run with admin/sudo privileges:**
   - macOS/Linux: `sudo python3 setup.py`
   - Windows: Run Command Prompt as Administrator

---

#### Audio player not working

**Symptoms:** Audio doesn't play or controls don't respond

**Solutions:**
- Try a different browser (Chrome recommended)
- Update your browser to the latest version
- Check browser console for errors (F12 → Console tab)
- Ensure audio file format is supported (MP3, M4A, WAV)
- Clear browser cache and reload page
- Try playing the audio file directly in your browser (drag file into browser)

---

#### Transcript not showing

**Symptoms:** Transcription completes but no text appears

**Solutions:**
- Open browser console (F12) to check for JavaScript errors
- Refresh the page
- Check if transcription JSON was created in `data/transcriptions/`
- Verify transcription completed successfully (no error messages)
- Try transcribing the file again

---

#### Application crashes or freezes

**Symptoms:** Application stops responding or window closes

**Solutions:**
- Check available RAM (close other apps if needed)
- Use a smaller Whisper model
- Try transcribing a shorter audio file
- Check Terminal/Command Prompt for error messages
- Restart the application
- Restart your computer if problem persists

---

### Getting Help

If issues persist:

1. **Check the error message** - Read it carefully, it often points to the problem
2. **Verify your installation:**
   - macOS/Linux: `python3 test_structure.py`
   - Windows: `python test_structure.py`
3. **Check system resources:** RAM, disk space, CPU usage
4. **Try the example audio files** to rule out file-specific issues
5. **Consult platform-specific sections above** for your OS
6. **Ensure all prerequisites are installed** (Python, FFmpeg)

**Useful diagnostic commands:**

**macOS:**
```bash
python3 --version
ffmpeg -version
python3 test_structure.py
```

**Windows:**
```cmd
python --version
ffmpeg -version
python test_structure.py
```

These will help identify which component is causing issues.

## 🎯 Keyboard Shortcuts

- **Space** - Play/Pause
- **← (Left Arrow)** - Rewind 5 seconds
- **→ (Right Arrow)** - Forward 5 seconds

## 📊 System Requirements

### Minimum Requirements

| Component | Minimum | Recommended |
|-----------|---------|-------------|
| **Python** | 3.8+ | 3.10+ |
| **RAM** | 4GB | 8GB+ |
| **Disk Space** | 2GB | 4GB+ |
| **Processor** | Any modern CPU | Multi-core CPU |
| **Operating System** | macOS 10.14+, Windows 10+, Ubuntu 18.04+ | Latest versions |

### Why These Requirements?

- **Python 3.8+**: Required for Whisper and modern libraries
- **4GB RAM**: Minimum for running base model and processing audio
- **8GB+ RAM**: Recommended for large models (medium, large-v3) and long audio files
- **2GB disk space**: For Python packages, Whisper models, and transcriptions
- **4GB+ disk space**: If using multiple Whisper models or storing many transcriptions

### Performance by Model

| Model | RAM Usage | Disk Space | Transcription Speed* |
|-------|-----------|------------|---------------------|
| **tiny** | ~1GB | 39MB | ⚡⚡⚡ Fastest (1x) |
| **base** | ~2GB | 74MB | ⚡⚡ Fast (2x slower than tiny) |
| **small** | ~3GB | 244MB | ⚡ Moderate (4x slower than tiny) |
| **medium** | ~5GB | 769MB | 🐢 Slow (8x slower than tiny) |
| **large-v3** | ~8GB+ | 1.5GB | 🐢🐢 Slowest (16x slower than tiny) |

*Approximate for 10-minute audio on modern CPU

### Tips for Better Performance

1. **Use SSD storage** - Faster model loading and file access
2. **Close other apps** - Free up RAM for transcription
3. **Use appropriate model** - Base model is best for most use cases
4. **Process shorter files** - Split long lectures into 30-minute chunks
5. **Restart regularly** - Especially on Windows, to clear memory

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
