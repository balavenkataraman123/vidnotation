import os
from time import ctime
import whisper

#command = "ffmpeg -i videos/demo.mp4 -ab 160k -ac 2 -ar 44100 -vn audio.wav"
#os.system(command)


model = whisper.load_model("base")
print("loadeddd")
result = model.transcribe("audio1.mp3")



seggs = []

a = (result['segments'])
for i in a:
    a = i['text']
    b = float(i['start'])
    c =  float(i['end'])
    seggs.append([str(a), str(b), str(c)])
try:
    os.remove("vids.txt")
except:
    print('deez nuts lmao')
vidtxt = open("vids.txt", "w")
print(seggs)
numseggz = 0
for [c, a, b] in seggs:
    os.system(f"ffmpeg -ss {str(a)} -i audio1.mp3 -c copy -t {str((float(b)-float(a)))} seggz_{str(numseggz)}.mp3")
    vidtxt.writelines(f"file \'seggz_{str(numseggz)}.mp3\' \n")
    numseggz += 1
vidtxt.close

os.system('ffmpeg -f concat -i vids.txt -c copy output8.mp3')
