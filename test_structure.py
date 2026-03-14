#!/usr/bin/env python3
"""
Quick test to verify project structure
"""

import sys
import os
from pathlib import Path

print("=" * 60)
print("🔍 Open Transcriber - Structure Test")
print("=" * 60)

# Check Python version
print(f"\n✅ Python version: {sys.version_info.major}.{sys.version_info.minor}")

# Check required directories
required_dirs = [
    "backend",
    "frontend/static/css",
    "frontend/static/js",
    "frontend/templates",
    "data",
    "uploads",
]

print("\n📁 Checking directories...")
for dir_path in required_dirs:
    if Path(dir_path).exists():
        print(f"   ✅ {dir_path}")
    else:
        print(f"   ❌ {dir_path} - MISSING")

# Check required files
required_files = [
    "backend/app.py",
    "backend/transcribe.py",
    "backend/storage.py",
    "backend/utils.py",
    "frontend/templates/index.html",
    "frontend/static/css/styles.css",
    "frontend/static/js/app.js",
    "frontend/static/js/player.js",
    "requirements.txt",
    "run.py",
    "setup.py",
    "README.md",
]

print("\n📄 Checking files...")
for file_path in required_files:
    if Path(file_path).exists():
        print(f"   ✅ {file_path}")
    else:
        print(f"   ❌ {file_path} - MISSING")

print("\n" + "=" * 60)
print("✅ Structure test complete!")
print("=" * 60)
print("\n🚀 Next steps:")
print("   1. Run: python3 setup.py")
print("   2. Run: python3 run.py")
print("   3. Open: http://localhost:5000")
