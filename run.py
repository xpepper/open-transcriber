#!/usr/bin/env python3
"""
Open Transcriber - Application Entry Point
"""

import sys
import os


def main():
    # Add backend directory to path
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), "backend"))

    from app import app

    print("=" * 60)
    print("🎓 Open Transcriber")
    print("=" * 60)
    print("\n🚀 Starting server...")
    print("   Open http://localhost:5000 in your browser")
    print("\n   Press Ctrl+C to stop the server")
    print("=" * 60 + "\n")

    app.run(host="127.0.0.1", port=5000, debug=True)


if __name__ == "__main__":
    main()
