import os, re
from datetime import datetime
from flask import Response, Flask, render_template, request, jsonify
from moviepy.editor import VideoFileClip
import sqlite3
import requests

app = Flask(__name__, static_folder='storage')
conn = sqlite3.connect('database.db')
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS video (filename TEXT, duration FLOAT)''')
conn.commit()
conn.close()

def convert_filename(filename):
    timestamp = filename[:-4]
    time_object = datetime.strptime(timestamp, '%Y%m%d%H%M%S')
    new_format = time_object.strftime('%H:%M:%S')
    return new_format

def count_duration(filename):
    try:
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM video WHERE filename=?", (filename,))
        saved_video = cursor.fetchone()
        duration = None
        if not saved_video:
            video = VideoFileClip(filename)
            duration = video.duration
            video.close()
            cursor.execute("INSERT INTO video (filename, duration) VALUES (?, ?)", (filename, duration))
            conn.commit()
        else:
            duration = saved_video[1]
        conn.close()
        return duration
    except Exception as err:
        # print(err)
        return None

def get_video_duration(filename):
    try:
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM video WHERE filename=?", (filename,))
        saved_video = cursor.fetchone()
        if not saved_video:
            return '?'
        duration = saved_video[1]
        minutes = int(duration // 60)
        seconds = int(duration % 60)
        return f'{minutes} menit {seconds} detik' if minutes != 0 else f'{seconds} detik'
    except Exception as err:
        # print(err)
        return '?'

@app.route('/')
def index():
    directory = 'storage/motion'
    folders = [{'name': folder, 'port': str(8000 + int(re.sub(r"\D", "", folder))), 'id': re.sub(r"\D", "", folder)} for folder in os.listdir(directory) if os.path.isdir(os.path.join(directory, folder))]
    return render_template('index.html', folders=folders)

@app.route('/cam/<camera_id>')
def record(camera_id):
    selected_date =  request.args.get('date', None)
    if not selected_date:
        current_datetime = datetime.now()
        selected_date = current_datetime.strftime("%Y-%m-%d")
    date = datetime.strptime(selected_date, "%Y-%m-%d").strftime("%Y%m%d")
    storage_dir = f'storage/motion/cam{camera_id}'
    files = os.listdir(storage_dir)
    filtered_files = [file for file in files if file[:-10] == date]
    files_list = [{'filename': file, 'name': convert_filename(file), 'duration': get_video_duration('storage/motion/cam' + camera_id + '/' + file)} for file in filtered_files]
    sorted_files = sorted(files_list, key=lambda x: datetime.strptime(x['filename'][:-4], '%Y%m%d%H%M%S'))
    return render_template('camera.html', files_list=sorted_files, camera_id=camera_id)

@app.route('/live/<camera_id>')
def live_camera(camera_id):
    port = str(8000 + int(camera_id))
    stream_url = f'http://localhost:{port}'
    response = requests.get(stream_url, stream=True)
    return Response(response.iter_content(chunk_size=1024), content_type=response.headers['content-type'])

@app.route('/video-duration')
def count_video_duration():
    path = 'storage/motion'
    for directory in [folder for folder in os.listdir(path) if os.path.isdir(os.path.join(path, folder))]:
        storage_dir = f'storage/motion/{directory}'
        files = os.listdir(storage_dir)
        for file in files:
            count_duration(f'storage/motion/{directory}/{file}')
    return jsonify({'message': 'success'})
    

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
