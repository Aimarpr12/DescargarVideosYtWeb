from flask import Flask, render_template, request, send_from_directory, redirect, url_for, jsonify
from pytube import YouTube, exceptions
from googleapiclient.discovery import build
from dotenv import load_dotenv
import os
import subprocess

app = Flask(__name__)

load_dotenv()
API_KEY = os.getenv('API_KEY')
youtube = build("youtube", "v3", developerKey=API_KEY)

DOWNLOAD_FOLDER = os.path.join(os.getcwd(), 'downloads')
if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

def is_live_stream(video_id):
    response = youtube.videos().list(part="snippet,liveStreamingDetails", id=video_id).execute()
    if 'items' in response:
        video_details = response['items'][0]
        if 'liveStreamingDetails' in video_details:
            return True
    return False

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        video_url = request.form.get('video_url')
        if not video_url:
            return "No se ha proporcionado ninguna URL.", 400
        try:
            yt = YouTube(video_url)
            video_id = yt.video_id
            if is_live_stream(video_id):
                save_path = os.path.join(DOWNLOAD_FOLDER, f"{yt.title}.mp4")
                subprocess.run(['yt-dlp', video_url, '-o', save_path])
                return redirect(url_for('download_file', filename=f"{yt.title}.mp4"))
            else:
                video_stream = yt.streams.get_highest_resolution()
                save_path = os.path.join(DOWNLOAD_FOLDER, f"{yt.title}.mp4")
                video_stream.download(output_path=DOWNLOAD_FOLDER, filename=f"{yt.title}.mp4")
                return redirect(url_for('download_file', filename=f"{yt.title}.mp4"))
        except exceptions.RegexMatchError:
            return "Enlace de video no válido. Por favor, introduce un enlace válido."
        except exceptions.VideoUnavailable:
            return "El video no está disponible o no se puede acceder. Verifica el enlace y la disponibilidad."
        except Exception as e:
            return f"Se produjo un error: {str(e)}"
    return render_template('index.html')

@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(DOWNLOAD_FOLDER, filename, as_attachment=True)

@app.route('/download_audio', methods=['POST'])
def download_audio():
    video_url = request.form.get('video_url')
    if not video_url:
        return "No se ha proporcionado ninguna URL.", 400

    try:
        yt = YouTube(video_url)
        if check_copyright(yt.video_id):
            print(f"Video URL: {video_url}")
            video_stream = yt.streams.get_audio_only()
            save_path = os.path.join(DOWNLOAD_FOLDER, f"{yt.title}.mp3")
            video_stream.download(output_path=DOWNLOAD_FOLDER, filename=f"{yt.title}.mp3")
            return redirect(url_for('download_file', filename=f"{yt.title}.mp3"))
        else:
            if request.form.get('confirmed') == 'true': 
                try:
                    video_stream = yt.streams.get_audio_only()
                    save_path = os.path.join(DOWNLOAD_FOLDER, f"{yt.title}.mp3")
                    video_stream.download(output_path=DOWNLOAD_FOLDER, filename=f"{yt.title}.mp3")
                    return redirect(url_for('download_file', filename=f"{yt.title}.mp3"))
                except exceptions.RegexMatchError:
                    return "Enlace de video no válido. Por favor, introduce un enlace válido."
                except exceptions.VideoUnavailable:
                    return "El video no está disponible o no se puede acceder. Verifica el enlace y la disponibilidad."
                except Exception as e:
                    return f"Se produjo un error: {str(e)}"
            else:
                return jsonify({'warning': True, 'video_url': video_url})
    except exceptions.RegexMatchError:
        return "Enlace de video no válido. Por favor, introduce un enlace válido."
    except exceptions.VideoUnavailable:
        return "El video no está disponible o no se puede acceder. Verifica el enlace y la disponibilidad."
    except Exception as e:
        return f"Se produjo un error: {str(e)}"

def check_copyright(video_id):
    if video_id:
        try:
            response = youtube.videos().list(part="snippet", id=video_id).execute()
            
            if "items" in response:
                video = response["items"][0]
                description = video["snippet"]["description"]
                
                if "copyright" in description.lower():
                    return True  
                else:
                    return False 
            else:
                print("Video no encontrado")
        except Exception as e:
            print(f"Error: {str(e)}")
    
    return False

if __name__ == '__main__':
    app.run(debug=True, port=8888)
