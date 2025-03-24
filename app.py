from flask import Flask, request, jsonify, render_template, send_from_directory
import yt_dlp
import os

# Cambia la carpeta de descargas a un directorio dentro del proyecto
DOWNLOAD_FOLDER = os.path.join(os.getcwd(), "downloads")
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

def descargar_video(url):
    opciones = {
        'outtmpl': os.path.join(DOWNLOAD_FOLDER, '%(title)s.%(ext)s'),
        'format': 'bestvideo+bestaudio/best',
    }

    with yt_dlp.YoutubeDL(opciones) as ydl:
        info = ydl.extract_info(url, download=True)
        return ydl.prepare_filename(info)



    except Exception as e:
        return None

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    """API para descargar un video desde TikTok."""
    try:
        data = request.get_json()
        url = data.get("url")

        if not url:
            return jsonify({"error": "No se proporcionó una URL"}), 400

        file_path = descargar_video(url)

        if not file_path:
            return jsonify({"error": "No se pudo descargar"}), 500

        return jsonify({"message": "Descarga exitosa", "path": file_path})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory("static", filename)

if __name__ == '__main__':
    app.run(debug=True)



