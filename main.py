from flask import Flask, request, jsonify, Response, stream_with_context
from flask_cors import CORS
import yt_dlp
import requests
import re

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return "Tony Jamer Stark Backend API - Engine Online (Force Download Active)"

@app.route('/api/extract', methods=['GET'])
def extract_info():
    url = request.args.get('url')
    if not url:
        return jsonify({"success": False, "error": "URL missing"}), 400

    # ULTRA-BYPASS SETTINGS FOR YOUTUBE & IG
    ydl_opts = {
        'format': 'best',
        'quiet': True,
        'skip_download': True,
        'no_warnings': True,
        'extractor_args': {
            'youtube': ['player_client=ios,android,web'] # Fake Mobile Request
        },
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1'
        }
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            
            # Title Fix
            title = info.get('title', 'Tony_Jamer_Stark_Media')
            
            # Instagram Thumbnail Fix (Array se nikalna)
            thumbnail = info.get('thumbnail')
            if not thumbnail and info.get('thumbnails'):
                thumbnail = info['thumbnails'][-1].get('url', '') # Best quality pic
            
            # Direct MP4 Link Fix
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
        return jsonify({"success": False, "error": str(e)}), 500

# NEW: YE VIDEO KO DIRECT DOWNLOAD KARWAYEGA BINA PLAY KIYE
@app.route('/api/download')
def download_file():
    file_url = request.args.get('url')
    title = request.args.get('title', 'Video')
    
    # Filename se faltu character hatana taaki error na aaye
    safe_title = re.sub(r'[^\w\-_\. ]', '_', title) + '.mp4'

    try:
        req = requests.get(file_url, stream=True, timeout=15)
        # Content-Disposition hi wo magic hai jo browser ko force karta hai download ke liye
        return Response(
            stream_with_context(req.iter_content(chunk_size=1024*1024)),
            content_type=req.headers.get('content-type', 'video/mp4'),
            headers={'Content-Disposition': f'attachment; filename="{safe_title}"'}
        )
    except Exception as e:
        return f"Download Failed: {str(e)}", 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
