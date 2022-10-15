import logging
import os
import re
import time
import mimetypes
from datetime import datetime
from urllib import response
import base64
from PIL import Image, ImageGrab
import cv2

from flask import Flask, Response, render_template, send_file, request

app = Flask(__name__)

VIDEO_PATH = '/video'
VIDEO_WIDTH = 640
VIDEO_HEIGHT = 360

FFMPEG_PATH = "C:/Users/Admin/ffmpeg/bin/ffmpeg.exe"

MB = 1 << 20
BUFF_SIZE = 10 * MB   

@app.route(f'/play/<video>')
def home(video):
    response = render_template('index.html', path=f'{VIDEO_PATH}/{video}', video=video)
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

@app.route(f'{VIDEO_PATH}/<video>')
def video(video):
    global path
    path = f'.{VIDEO_PATH}/{video}'
    start, end = get_range(request)
    return partial_response(path, start, end)

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
def draw():
    global currenttimestamp
    if request.method == 'GET':
        return render_template('index.html')
    elif request.method == 'POST':
        data_url = request.values.get('image')
        print(data_url)
        currenttimestamp = float(data_url)
        try:
            os.remove("frameeee.jpg")
        except:
            print('nuts')
        os.system(f"{FFMPEG_PATH} -i " + path + " -ss " + data_url + " -frames 1 frameeee.jpg")
        return "nuts"

@app.route('/draw1', methods = ['GET', 'POST'])
def draw1():
    if request.method == 'GET':
        return render_template('index2.html')
    elif request.method == 'POST': 
        print("yeeeeet")
        data_url = request.values.get('image')
        timestamplen = request.values.get('timestamp')
        content = data_url.split(';')[1]
        im_b64 = content.split(',')[1]
        im_bytes = base64.b64decode(im_b64)
        print(timestamplen)
        print(currenttimestamp)
        imgdata = base64.b64decode(im_b64)
        filename = "imagelmao.png"
        with open(filename, 'wb') as f:
            f.write(imgdata)
        img = cv2.imread("imagelmao.png")

        dim = (VIDEO_WIDTH, VIDEO_HEIGHT)
        
        img1 = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
        os.remove("imagelmao.png")
        cv2.imwrite("imagelmao.png", img1)
        os.system(f"{FFMPEG_PATH} -y -i videos/demo.mp4 -i imagelmao.png -filter_complex \"[1][0]scale2ref[i][m];[m][i]overlay[v] \"-map \"[v]\" -map 0:a? -ac 2 output.mp4")
        return "nuts"

@app.route('/images')
def image():
    filename = "frameeee.jpg"
    return send_file(filename, mimetype='image/gif')


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000, debug=True)
