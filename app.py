from flask import Flask, request, jsonify
import yt_dlp
import os
import uuid

app = Flask(__name__)
DOWNLOAD_FOLDER = 'downloads'

if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

@app.route('/download', methods=['POST'])
def download_video():
    data = request.get_json()
    url = data.get('url')
    
    if not url:
        return jsonify({'success': False, 'error': 'No URL provided'}), 400
    
    try:
        ydl_opts = {
            'outtmpl': os.path.join(DOWNLOAD_FOLDER, '%(title)s.%(ext)s'),
            'format': 'mp4'
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            download_link = f"/downloaded/{os.path.basename(filename)}"
            return jsonify({'success': True, 'download_link': download_link})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/downloaded/<filename>', methods=['GET'])
def serve_video(filename):
    return send_from_directory(DOWNLOAD_FOLDER, filename)

if __name__ == '__main__':
    app.run(debug=True)
