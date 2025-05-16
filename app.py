from flask import Flask, request, jsonify
import subprocess
import os
import uuid

app = Flask(__name__)

@app.route("/")
def home():
    return "yt-dlp Downloader API is running."

@app.route("/download", methods=["GET"])
def download_video():
    url = request.args.get("url")
    if not url:
        return jsonify({"error": "Missing URL"}), 400

    filename = f"{uuid.uuid4()}.%(ext)s"
    output_path = f"downloads/{filename}"
    os.makedirs("downloads", exist_ok=True)

    try:
        result = subprocess.run([
            "yt-dlp", "-o", output_path, url
        ], capture_output=True, text=True)

        if result.returncode != 0:
            return jsonify({"error": result.stderr}), 500

        return jsonify({"message": "Downloaded successfully", "file": filename})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
