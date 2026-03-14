"""
Open Transcriber - Flask Application
Main web application with API endpoints
"""

from flask import Flask, render_template, request, jsonify, send_file
from werkzeug.utils import secure_filename
import os
import sys

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from storage import (
    save_transcription,
    load_transcription,
    load_metadata,
    list_all_transcriptions,
    find_by_hash,
    delete_transcription,
    save_temp_file,
    cleanup_temp_file,
    get_audio_path,
    TRANSCRIPTIONS_DIR,
)
from transcribe import transcribe_audio, get_available_models, detect_language
from utils import is_audio_file, format_duration, format_date

# Initialize Flask app
app = Flask(
    __name__,
    static_folder="../frontend/static",
    template_folder="../frontend/templates",
)

app.config["MAX_CONTENT_LENGTH"] = 500 * 1024 * 1024  # 500MB max file size
app.config["UPLOAD_FOLDER"] = "uploads"

# Routes


@app.route("/")
def index():
    """Serve the main application page"""
    return render_template("index.html")


# API Routes


@app.route("/api/transcriptions", methods=["GET"])
def api_list_transcriptions():
    """Get list of all transcriptions"""
    try:
        transcriptions = list_all_transcriptions()
        return jsonify(transcriptions)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/transcriptions/<transcription_id>", methods=["GET"])
def api_get_transcription(transcription_id):
    """Get a specific transcription"""
    try:
        transcription = load_transcription(transcription_id)
        if transcription:
            return jsonify(transcription)
        else:
            return jsonify({"error": "Transcription not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/transcriptions/<transcription_id>/audio", methods=["GET"])
def api_get_audio(transcription_id):
    """Get the audio file for a transcription"""
    try:
        print(f"Fetching audio for transcription: {transcription_id}")
        audio_path = get_audio_path(transcription_id)

        print(f"Audio path result: {audio_path}")

        if audio_path and audio_path.exists():
            print(f"Sending audio file: {audio_path}")
            return send_file(str(audio_path))
        else:
            print(f"Audio file not found for transcription: {transcription_id}")
            return jsonify(
                {"error": "Audio file not found", "transcription_id": transcription_id}
            ), 404
    except Exception as e:
        print(f"Error serving audio: {e}")
        import traceback

        traceback.print_exc()
        return jsonify({"error": str(e)}), 500


@app.route("/api/transcribe", methods=["POST"])
def api_transcribe():
    """Upload and transcribe an audio file"""
    try:
        # Check if file is present
        if "audio" not in request.files:
            return jsonify({"error": "No audio file provided"}), 400

        file = request.files["audio"]

        if not file or not file.filename:
            return jsonify({"error": "No file selected"}), 400

        # Validate file type
        if not is_audio_file(file.filename):
            return jsonify(
                {
                    "error": "Invalid file type. Please upload an audio file (mp3, m4a, wav, etc.)"
                }
            ), 400

        # Get model selection
        model_name = request.form.get("model", "base")
        language = request.form.get("language", None)

        # Save to temporary location
        temp_path = save_temp_file(file)

        try:
            # Check for duplicate
            from storage import calculate_file_hash

            file_hash = calculate_file_hash(temp_path)
            existing = find_by_hash(file_hash)

            if existing:
                cleanup_temp_file(temp_path)
                return jsonify(
                    {
                        "status": "duplicate",
                        "message": "This file has already been transcribed",
                        "transcription": existing,
                    }
                )

            # Transcribe
            print(f"Starting transcription with model: {model_name}")
            result = transcribe_audio(str(temp_path), model_name, language)

            # Save to permanent storage
            transcription_id, is_duplicate = save_transcription(
                result,
                str(temp_path),
                file.filename,
                model_name,
                result.get("language"),
            )

            # Load and return the full transcription
            transcription = load_transcription(transcription_id)

            return jsonify(
                {
                    "status": "success",
                    "message": "Transcription completed successfully",
                    "transcription": transcription,
                }
            )

        finally:
            # Clean up temp file
            cleanup_temp_file(temp_path)

    except Exception as e:
        print(f"Error during transcription: {e}")
        import traceback

        traceback.print_exc()
        return jsonify({"error": f"Transcription failed: {str(e)}"}), 500


@app.route("/api/transcriptions/<transcription_id>", methods=["DELETE"])
def api_delete_transcription(transcription_id):
    """Delete a transcription"""
    try:
        success = delete_transcription(transcription_id)
        if success:
            return jsonify({"status": "success", "message": "Transcription deleted"})
        else:
            return jsonify({"error": "Transcription not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/health", methods=["GET"])
def api_health():
    """Health check endpoint"""
    return jsonify(
        {
            "status": "healthy",
            "transcriptions_dir": str(TRANSCRIPTIONS_DIR),
            "exists": TRANSCRIPTIONS_DIR.exists(),
        }
    )


@app.route("/api/models", methods=["GET"])
def api_get_models():
    """Get list of available Whisper models"""
    try:
        models = get_available_models()
        return jsonify(models)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/detect-language", methods=["POST"])
def api_detect_language():
    """Detect language from audio file"""
    try:
        if "audio" not in request.files:
            return jsonify({"error": "No audio file provided"}), 400

        file = request.files["audio"]

        if not file or not file.filename:
            return jsonify({"error": "No file selected"}), 400

        if not is_audio_file(file.filename):
            return jsonify({"error": "Invalid file type"}), 400

        model_name = request.form.get("model", "base")

        # Save to temporary location
        temp_path = save_temp_file(file)

        try:
            language = detect_language(str(temp_path), model_name)
            return jsonify({"language": language})
        finally:
            cleanup_temp_file(temp_path)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Error handlers


@app.errorhandler(413)
def request_entity_too_large(error):
    """Handle file too large error"""
    return jsonify({"error": "File too large. Maximum size is 500MB"}), 413


@app.errorhandler(500)
def internal_server_error(error):
    """Handle internal server error"""
    return jsonify({"error": "Internal server error"}), 500


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
