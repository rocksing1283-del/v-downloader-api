from flask import Flask, request, jsonify, Response, stream_with_context
from flask_cors import CORS
import yt_dlp
import requests
import re

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return "Tony Jamer Stark Backend API - Engine Online (Ultra Bypass V3 Active)"

@app.route('/api/extract', methods=['GET'])
def extract_info():
    url = request.args.get('url')
    if not url:
        return jsonify({"success": False, "error": "URL missing"}), 400

    # 🔥 V3 ULTRA-BYPASS: 'tv' aur 'web_embedded' client bot protection bypass karte hain
    ydl_opts = {
        'format': 'best',
        'quiet': True,
        'skip_download': True,
        'no_warnings': True,
        'nocheckcertificate': True,
        'extractor_args': {
            'youtube': ['player_client=tv,web_embedded'] 
        },
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
        }
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            
            title = info.get('title', 'Tony_Jamer_Stark_Media')
            
            thumbnail = info.get('thumbnail')
            if not thumbnail and info.get('thumbnails'):
                thumbnail = info['thumbnails'][-1].get('url', '')
            
            direct_url = info.get('url')
            if not direct_url and info.get('formats'):
                direct_url = info['formats'][-1].get('url')

            return jsonify({
                "success": True,
                "data": {
                    "title": title,
                    "thumbnail": thumbnail,
                    "download_link": direct_url
                }
            })
    except Exception as e:
        # Error ko clean karna taaki padhne me aasan ho
        error_msg = str(e)
        if "Sign in" in error_msg:
            error_msg = "YouTube ne server ko block kar diya hai (Bot Protection). Kripya koi doosra link try karein."
        return jsonify({"success": False, "error": error_msg}), 500

@app.route('/api/download')
def download_file():
    file_url = request.args.get('url')
    title = request.args.get('title', 'Video')
    safe_title = re.sub(r'[^\w\-_\. ]', '_', title) + '.mp4'

    try:
        req = requests.get(file_url, stream=True, timeout=15)
        return Response(
            stream_with_context(req.iter_content(chunk_size=1024*1024)),
            content_type=req.headers.get('content-type', 'video/mp4'),
            headers={'Content-Disposition': f'attachment; filename="{safe_title}"'}
        )
    except Exception as e:
        return f"Download Failed: {str(e)}", 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
