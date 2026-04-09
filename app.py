from flask import Flask, request, jsonify, send_from_directory
import subprocess
import os
import uuid

app = Flask(__name__)

# Download klasörü
DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

# -----------------------------
# Health check (root)
# -----------------------------
@app.route("/", methods=["GET"], strict_slashes=False)
def health():
    return "OK", 200


# -----------------------------
# MP3 Download Endpoint
# -----------------------------
@app.route("/download", methods=["POST"], strict_slashes=False)
def download_mp3():
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "JSON body yok"}), 400

    url = data.get("url")
    if not url or not url.startswith("http"):
        return jsonify({"error": "Geçersiz URL"}), 400

    filename = f"{uuid.uuid4()}.mp3"
    output_path = os.path.join(DOWNLOAD_DIR, filename)

    cmd = [
        "yt-dlp",
        "-f", "bestaudio",
        "--extract-audio",
        "--audio-format", "mp3",
        "--audio-quality", "0",
        "-o", output_path,
        url
    ]

    try:
        subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
    except subprocess.CalledProcessError as e:
        return jsonify({
            "error": "İndirme başarısız",
            "details": e.stderr
        }), 500

    return jsonify({
        "status": "ok",
        "file": filename
    })


# -----------------------------
# File Download Endpoint
# -----------------------------
@app.route("/file/<filename>", methods=["GET"], strict_slashes=False)
def get_file(filename):
    return send_from_directory(
        DOWNLOAD_DIR,
        filename,
        as_attachment=True
    )


# -----------------------------
# MAIN ENTRY (CLOUD-READY)
# -----------------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)