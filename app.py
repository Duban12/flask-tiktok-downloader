from flask import Flask, request, jsonify, render_template
import yt_dlp
import os

app = Flask(__name__)

# Carpeta de descargas del usuario
DOWNLOAD_FOLDER = os.path.join(os.path.expanduser("~"), "Downloads")
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

def descargar_video(url):
    """ Descarga un video de TikTok en la mejor calidad disponible. """
    try:
        opciones = {
            'outtmpl': os.path.join(DOWNLOAD_FOLDER, '%(title)s.%(ext)s'),
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]',
            'merge_output_format': 'mp4',  # Asegura que el archivo final sea MP4
        }

        with yt_dlp.YoutubeDL(opciones) as ydl:
            info = ydl.extract_info(url, download=True)
            file_path = ydl.prepare_filename(info)  # Ruta del archivo descargado

            # Verifica si el archivo existe
            if os.path.exists(file_path):
                return file_path
            else:
                return None

    except Exception as e:
        print(f"Error en la descarga: {e}")
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

        return jsonify({
            "message": "Descarga exitosa",
            "file_path": file_path,
            "note": "Revisa la carpeta de Descargas en tu PC."
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
