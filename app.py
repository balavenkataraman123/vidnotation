from genericpath import isfile
import os
import re
import json
import mimetypes
from flask import Flask, Response, render_template, request

app = Flask(__name__)

VIDEO_PATH = '/video'

MB = 1 << 20
BUFF_SIZE = 10 * MB   

@app.route(f'/play/<video>')
def home(video):
    response = render_template('index.html', path=f'{VIDEO_PATH}/{video}', video=video, fps=25)
    return response

@app.route(f'/annotations/<video>/')
def get_annotations(video):
    path = f'.{VIDEO_PATH}/{video}.json'
    if os.path.isfile(path):
        with open(path) as f:
            return f.read()


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

@app.route('/annotate/', methods=['GET', 'POST'])
def annotate():
    vid = request.args.get('video')
    start = request.args.get('start')
    dur = request.args.get('dur')

    if vid and start and dur:
        fp = f'.{vid}.json'
        if os.path.isfile(fp):
            try: jf = json.loads(open(fp).read())
            except:  jf = {}
        else: jf = {}

        strokes = {'start': int(start), 'dur': int(dur), 'end': int(start) + int(dur), 'strokes': json.loads(request.data)['strokes']}

        try: jf['annotations'].append(strokes)
        except KeyError: jf['annotations'] = [strokes]

        with open(fp, 'w+') as f: f.write(json.dumps(jf))

        return "OK"

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000, debug=True)
