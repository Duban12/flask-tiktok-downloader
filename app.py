from flask import Flask, request, jsonify, render_template, send_file
import yt_dlp
import os

app = Flask(__name__)

# Carpeta de descargas en el servidor (Render)
DOWNLOAD_FOLDER = "downloads"
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

def descargar_video(url):
    """ Descarga un video de TikTok en la mejor calidad disponible. """
    try:
        opciones = {
            'outtmpl': os.path.join(DOWNLOAD_FOLDER, '%(title)s.%(ext)s'),
            'format': 'bestvideo+bestaudio/best',
        }

        with yt_dlp.YoutubeDL(opciones) as ydl:
            info = ydl.extract_info(url, download=True)
            return ydl.prepare_filename(info)  # Ruta del archivo descargado

    except Exception as e:
        return None

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    """ API para descargar un video desde TikTok. """
    try:
        data = request.get_json()
        url = data.get("url")

        if not url:
            return jsonify({"error": "No se proporcionó una URL"}), 400

        file_path = descargar_video(url)

        if not file_path:
            return jsonify({"error": "No se pudo descargar"}), 500

        return send_file(file_path, as_attachment=True)  # Permite descargar el archivo

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)

