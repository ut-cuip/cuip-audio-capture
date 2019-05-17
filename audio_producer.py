import os
import requests
import json
import yaml
from multiprocessing import Process
import subprocess
import asyncio
import time
import os
import signal


def main(): 
    if os.path.exists("config.yaml"):
        with open("config.yaml") as file:
            config = yaml.load(file.read(), Loader=yaml.Loader)
    else:
        print("No {} file found".format("config.yaml"))
        exit()
    
    processes = []

    for i in range(len(config["cameras"])):
        #camera_url = str(config["cameras"][i]["url"])
        
        processes.append(Process(target=run, args=[str(config["cameras"][i]["url"])]))
    try:
        for process in processes:
            process.start()
        for process in processes:
            process.join()
    except KeyboardInterrupt:
        for process in processes:
            process.terminate()


def run(url):
    print(url) 
    fetch_audio(url)
    #process_audio()
    #produce() 

def fetch_audio(url):
    print("fetch_audio")
    if os.path.exists("~/Desktop/python.wav"):
        os.remove("~/Desktop/python.wav")
    try:
        subproc = subprocess.Popen('ffmpeg -i rtsp://root:2u9JRlI#h6Ul@mlk-douglas-cam-3.research.utc.edu/axis-media/media.amp?videocodec=h264  -map 0:1 -c pcm_s16le ~/Desktop/python.wav', shell=True, preexec_fn=os.setpgrp, stdin=subprocess.PIPE)
        time.sleep(15)
        os.killpg(os.getpgid(subproc.pid), signal.SIGTERM)
    except KeyboardInterrupt:
        os.killpg(os.getpgid(subproc.pid), signal.SIGTERM)



#    sub_process = os.popen('ffmpeg -i rtsp://root:2u9JRlI#h6Ul@mlk-douglas-cam-3.research.utc.edu/axis-media/media.amp?videocodec=h264  -map 0:1 -c pcm_s16le ~/Desktop/python.wav').write()
 #   sub_process.kill()

def process_audio(): 
    print("process_audio")
    #os.remove("audiyd.wav")

def produce():
    print("produce to kafka")


if __name__ == '__main__': 
    main()    



# Run this through the system because Requests is a butt about the -F switch
#output = os.popen('curl -X POST "http://localhost:5000/model/predict?start_time=0" -H "accept: application/json" -H "Content-Type: multipart/form-data" -F "audio=@SirenTest.wav;type=audio/wav"').read()
#print(json.loads(output))

















































#ffmpeg -i rtsp://root:2u9JRlI#h6Ul@mlk-douglas-cam-3.research.utc.edu/axis-media/media.amp?videocodec=h264  -map 0:1 -c pcm_s16le ~/Desktop/audiyd.wav -v debug 

#headers = {
#    'accept': 'application/json',
#    'Content-Type': 'multipart/form-data',
#}

#params = (
#    ('start_time', '0'),
#)

#files = {
#    'audio': ('audio_file.wav;type', open('audio_file.wav', 'rb')),
#}
#response = requests.post('http://localhost:5000/model/predict?start_time=0', headers=headers, files=files)

#print(response)

#os.remove("audiyd.wav")
#pring("File removed")


#def get_oldest_file(path):

#    files = sorted(os.listdir(path), key=os.path.getctime)
#    oldest = files[0]
#    newest = files[-1]
    


#curl -X POST "http://localhost:5000/model/predict?start_time=0" -H "accept: application/json" -H "Content-Type: multipart/form-data" -F "audio=@crash.wav;type=audio/wav"


#from scipy.io import wavfile
#fs, data = wavfile.read('audio.wav')
