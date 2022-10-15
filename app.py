import logging
import os
import re
import time
import mimetypes
from datetime import datetime
from urllib import response

from flask import Flask, Response, render_template, send_file, request
path = "nuts"
currenttimestamp = 0

app = Flask(__name__)

VIDEO_PATH = '/video'

MB = 1 << 20
BUFF_SIZE = 10 * MB   

@app.route('/')
def home():
    response = render_template('index.html', video=VIDEO_PATH, timestamp=69)
    print('deez nuts')
    return response

def partial_response(path, start, end=None):
    file_size = os.path.getsize(path)

    # Determine (end, length)
    if end is None:
        end = start + BUFF_SIZE - 1
    end = min(end, file_size - 1)
    end = min(end, start + BUFF_SIZE - 1)
    length = end - start + 1

    # Read file
    with open(path, 'rb') as fd:
        fd.seek(start)
        bytes = fd.read(length)
    assert len(bytes) == length

    response = Response(
        bytes,
        206,
        mimetype=mimetypes.guess_type(path)[0],
        direct_passthrough=True,
    )
    response.headers.add(
        'Content-Range', 'bytes {0}-{1}/{2}'.format(
            start, end, file_size,
        ),
    )
    response.headers.add(
        'Accept-Ranges', 'bytes'
    )
    return response

def get_range(request):
    range = request.headers.get('Range')
    m = re.match('bytes=(?P<start>\d+)-(?P<end>\d+)?', range)
    if m:
        start = m.group('start')
        end = m.group('end')
        start = int(start)
        if end is not None:
            end = int(end)
        return start, end
    else:
        return 0, None
    
@app.route('/draw', methods = ['GET','POST'])
def index():
    global currenttimestamp
    if request.method == 'GET':
        return render_template('index.html')
    elif request.method == 'POST':
        data_url = request.values.get('image')
        print(data_url)
        try:
            os.remove("frameeee.jpg")
        except:
            print('nuts')
        os.system("ffmpeg -i " + path + " -ss " + data_url + " -frames 1 frameeee.jpg")
@app.route('/draw1', methods = ['GET', 'POST'])
def draw():
    if request.method == 'GET':
        return render_template('index2.html')


@app.route(VIDEO_PATH)
def video():
    global path
    path = 'videos/demo.mp4'
    start, end = get_range(request)
    return partial_response(path, start, end)
@app.route('/images')
def image():
    filename = "frameeee.jpg"
    return send_file(filename, mimetype='image/gif')



if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000, debug=True)
