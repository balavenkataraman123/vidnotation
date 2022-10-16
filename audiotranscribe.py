from email.mime import audio
import os
from time import ctime
import whisper
import json
import sys

FILE_NAME = sys.argv[1]



try:
    os.remove("audio.wav")
except:
    print('deez nuts lmao')

command = f"ffmpeg -i video/{FILE_NAME} -ab 160k -ac 2 -ar 44100 -vn audio.wav"
os.system(command)
model = whisper.load_model("base")
print("loadeddd")
result = model.transcribe("audio.wav")
data = {
    'segments' : []
}
a = (result['segments'])
for i in a:
    a = i['text']
    b = float(i['start'])
    c =  float(i['end'])
    data['segments'].append(
        {"text" : str(a), "start" : str(b), "end" : str(c)}
        )
with open(f'video/{FILE_NAME}timestamps.json', 'w') as outfile:
    json.dump(json.dumps(data), outfile)
