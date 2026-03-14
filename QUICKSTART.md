# 🎴 Open Transcriber - Quick Reference

## 🚀 Start the App

```bash
cd open-transcriber
python3 run.py
```

Then open: **http://localhost:5000**

---

## ⌨️ Keyboard Shortcuts

| Key | Action |
|-----|--------|
| **Space** | Play/Pause |
| **←** | Rewind 5 seconds |
| **→** | Forward 5 seconds |

---

## 🎙️ Whisper Models

| Model | Size | Speed | Accuracy | Best For |
|-------|------|-------|----------|----------|
| **tiny** | 39MB | ⚡⚡⚡ | ⭐ | Quick tests |
| **base** | 74MB | ⚡⚡ | ⭐⭐ | **Recommended** |
| **small** | 244MB | ⚡ | ⭐⭐⭐ | Better accuracy |
| **medium** | 769MB | 🐢 | ⭐⭐⭐⭐ | High accuracy |
| **large-v3** | 1.5GB | 🐢🐢 | ⭐⭐⭐⭐⭐ | Best accuracy |

---

## 📂 File Storage

```
data/transcriptions/
└── YYYY-MM-DD/
    └── <id>/
        ├── transcription.json
        ├── metadata.json
        └── audio.ext
```

---

## 🎯 Common Tasks

### Upload Audio
1. Click "+ Upload New"
2. Select model
3. Drag & drop or browse
4. Wait for transcription
5. Click "View"

### Navigate Transcript
- Click any word to jump to that moment
- Current word highlights automatically
- Scroll follows playback

### Delete Lecture
- Click "Delete" button in viewer
- Or click "Delete" in library list

---

## 🔧 Troubleshooting

**Port in use?** Change port in `run.py` to 5001

**FFmpeg error?** Install: `brew install ffmpeg` (macOS)

**Slow transcription?** Use "tiny" or "base" model

**Out of memory?** Use smaller model, close other apps

---

## 📞 Need Help?

- 📖 Read [README.md](README.md)
- 🚀 Check [INSTALL.md](INSTALL.md)
- 🔍 Verify with: `python3 test_structure.py`

---

## 💡 Tips

✨ Start with "base" model for best balance  
✨ Transcriptions stored locally - 100% private  
✨ Duplicate files auto-detected  
✨ Works offline after initial setup  

---

**Made with ❤️ for students**
