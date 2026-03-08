from flask import Flask, request, jsonify
from flask_cors import CORS
import yt_dlp

app = Flask(__name__)
# CORS allow karta hai aapki GitHub website ko is API se baat karne ke liye
CORS(app)

@app.route('/')
def home():
    return "Tony Jamer Stark Backend API is Running 100% OK! (Anti-Bot Active)"

@app.route('/api/extract', methods=['GET'])
def extract_info():
    url = request.args.get('url')
    
    if not url:
        return jsonify({"success": False, "error": "Bhai, koi URL nahi mila!"}), 400

    # 🔥 YAHAN HAI MAGIC: YouTube Anti-Bot Bypass Settings
    ydl_opts = {
        'format': 'best',
        'quiet': True,
        'skip_download': True,
        'no_warnings': True,
        'extractor_args': {
            # YouTube ko lagega ki ye Android App se request hai
            'youtube': ['player_client=android,ios'] 
        },
        'http_headers': {
            # Fake browser info
            'User-Agent': 'Mozilla/5.0 (Linux; Android 12; Pixel 6 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36',
        }
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            
            # Asli Data nikalna
            title = info.get('title', 'Unknown Title')
            thumbnail = info.get('thumbnail', '')
            direct_url = info.get('url', '') 
            
            return jsonify({
                "success": True,
                "developer": "Tony Jamer Stark",
                "data": {
                    "title": title,
                    "thumbnail": thumbnail,
                    "download_link": direct_url
                }
            })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
