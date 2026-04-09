from flask import Flask, request, jsonify, send_from_directory
import subprocess
import os
import uuid

app = Flask(__name__)

DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)


# ✅ MP3 indirme
@app.route("/download", methods=["POST"])
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
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError:
        return jsonify({"error": "İndirme başarısız"}), 500

    return jsonify({
        "status": "ok",
        "file": filename
    })


# ✅ MP3 dosyasını gönderme
@app.route("/file/<filename>", methods=["GET"])
def get_file(filename):
    return send_from_directory(
        DOWNLOAD_DIR,
        filename,
        as_attachment=True
    )



if __name__ == "__main__":
    import os
    port = os.environ.get("PORT", 5000)
    app.run(host="0.0.0.0", port=port)
