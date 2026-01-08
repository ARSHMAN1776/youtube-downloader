
from flask import Flask, request, jsonify, Response
from flask_cors import CORS
from yt_dlp import YoutubeDL
import requests

app = Flask(__name__, static_folder="static", static_url_path="")
CORS(app)

@app.route("/")
def home():
    return app.send_static_file("index.html")

@app.route("/info", methods=["POST"])
def get_info():
    data = request.get_json()
    url = data.get("url")
    if not url:
        return jsonify({"error": "URL is required"}), 400

    try:
        ydl_opts = {"quiet": True, "skip_download": True}
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            return jsonify({
                "title": info.get("title"),
                "uploader": info.get("uploader"),
                "duration": info.get("duration"),
                "thumbnail": info.get("thumbnail"),
            })
    except Exception as e:
        print(f"[INFO ERROR] {e}")
        return jsonify({"error": "Failed to fetch video info. Try another link."}), 500

@app.route("/download", methods=["GET"])
def download():
    url = request.args.get("url")
    format_type = request.args.get("format")

    if not url or format_type not in ["audio", "video"]:
        return jsonify({"error": "Missing or invalid parameters"}), 400

    try:
        ydl_opts = {
            "format": "bestaudio/best" if format_type == "audio" else "best",
            "quiet": True,
            "outtmpl": "-",
            "noplaylist": True,
        }

        if format_type == "audio":
            ydl_opts["postprocessors"] = [{
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }]

        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            stream_url = info["url"]
            title = info.get("title", "video")

        def generate():
            r = requests.get(stream_url, stream=True)
            for chunk in r.iter_content(chunk_size=1024):
                if chunk:
                    yield chunk

        return Response(
            generate(),
            mimetype="audio/mpeg" if format_type == "audio" else "video/mp4",
            headers={
                "Content-Disposition": f"attachment; filename=\"{title}.{ 'mp3' if format_type == 'audio' else 'mp4' }\""
            }
        )

    except Exception as e:
        print(f"[DOWNLOAD ERROR] {e}")
        return jsonify({"error": "Failed to stream video."}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
