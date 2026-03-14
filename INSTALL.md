# 🚀 Installation Guide - Open Transcriber

This guide will walk you through installing and running Open Transcriber on your computer.

## 📋 Prerequisites Checklist

Before you begin, ensure you have:

- [ ] **Python 3.8 or higher** installed
- [ ] **FFmpeg** installed (required for audio processing)
- [ ] **Internet connection** (for first-time model download)
- [ ] **4GB+ RAM** available (8GB+ recommended)
- [ ] **2GB+ free disk space** (4GB+ for larger models)

## 🔧 Step 1: Install FFmpeg

FFmpeg is required for audio processing. Choose your operating system:

### macOS (Homebrew)
```bash
# Install Homebrew if you don't have it:
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install FFmpeg
brew install ffmpeg
```

### Windows (Chocolatey)
```powershell
# Install Chocolatey if you don't have it:
# Run PowerShell as Administrator and run:
Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -s 256; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))

# Install FFmpeg
choco install ffmpeg
```

### Ubuntu/Debian
```bash
sudo apt update
sudo apt install ffmpeg
```

### Verify Installation
```bash
ffmpeg -version
```

You should see version information printed.

## 🐍 Step 2: Verify Python Installation

Check your Python version:

```bash
python3 --version
```

You should see **Python 3.8.0** or higher.

If Python is not installed:
- **macOS**: `brew install python3`
- **Windows**: Download from [python.org](https://www.python.org/downloads/)
- **Ubuntu**: `sudo apt install python3`

## 📦 Step 3: Install Python Dependencies

Run the setup script:

```bash
cd open-transcriber
python3 setup.py
```

This script will:
1. ✅ Check your Python version
2. ✅ Verify FFmpeg is installed
3. ✅ Create necessary directories
4. ✅ Install Python packages (Flask, Whisper, etc.)
5. ✅ Download and test the "tiny" Whisper model

**Expected output:**
```
============================================================
🎓 Open Transcriber - Setup
============================================================
✅ Python version: 3.12
✅ FFmpeg installed: ffmpeg version 6.1.1
📁 Creating directories...
   Created: data/transcriptions/
   Created: uploads/
   ...

📦 Installing Python dependencies...
✅ Dependencies installed successfully

🎙️  Verifying Whisper installation...
✅ Whisper 20231117 installed
   Testing model download (may take a moment)...
✅ Whisper model test successful

============================================================
✅ Setup complete!
============================================================
```

**If setup fails:**

1. **FFmpeg not found:**
   - Ensure FFmpeg is installed and in your PATH
   - Restart your terminal after installation

2. **Permission errors:**
   - Try using a virtual environment (recommended)
   - Or use `pip install --user` instead

3. **Network errors:**
   - Check your internet connection
   - Models are downloaded from GitHub, ensure access is not blocked

## 🎯 Step 4: Run the Application

Start the server:

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

 * Serving Flask app 'app'
 * Running on http://127.0.0.1:5000
```

## 🌐 Step 5: Open in Browser

Open your web browser and navigate to:

```
http://localhost:5000
```

You should see the Open Transcriber interface with:
- 🎓 Header
- 📚 Empty library (on first run)
- ➕ Upload button

## 🎤 Step 6: Test with Example Audio

The project includes example audio files for testing:

1. Click **"+ Upload New"**
2. Select the **"base"** model (recommended)
3. Navigate to `examples/small-example.m4a`
4. Wait for transcription to complete (~30-60 seconds)
5. Click **"View"** to see the transcription with audio player

## 🎉 Congratulations!

You're now ready to transcribe your lectures!

## 📚 Next Steps

- Read the [README.md](README.md) for usage instructions
- Try uploading your own lecture recordings
- Experiment with different Whisper models
- Explore the keyboard shortcuts for efficient navigation

## ⚠️ Troubleshooting

### Port 5000 already in use

If you see `Address already in use`, edit `run.py` and change the port:

```python
app.run(host='127.0.0.1', port=5001, debug=True)
```

Then navigate to `http://localhost:5001`

### ModuleNotFoundError: No module named 'flask'

This means dependencies weren't installed. Run:

```bash
pip3 install -r requirements.txt
```

### Slow transcription

- Use a smaller/faster model (tiny or base)
- Ensure you have sufficient RAM (8GB+ recommended)
- Close other applications

### Out of memory

- Use the "tiny" model
- Process shorter audio files
- Increase your system's available RAM

## 🔄 Updating

To update the application in the future:

```bash
# Pull latest changes (if using git)
git pull

# Update dependencies
pip3 install --upgrade -r requirements.txt
```

## 💡 Tips

1. **Use a virtual environment** (recommended):
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Keep the server running** in a separate terminal tab

3. **Bookmark** `http://localhost:5000` for quick access

4. **Backup your data**: Transcriptions are stored in `data/transcriptions/`

## 🆘 Still Having Issues?

1. Check that all prerequisites are installed
2. Verify you're in the correct directory
3. Try running `python3 setup.py` again
4. Check the terminal output for specific error messages
5. Ensure you have sufficient disk space and RAM

---

**Enjoy transcribing your lectures! 🎓**
