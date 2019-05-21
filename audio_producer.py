import os
import requests
import json
import yaml
from multiprocessing import Process, Lock
import subprocess
import asyncio
import datetime
import time
import os
import signal
from kafka import KafkaProducer 

#kafka_producer = KafkaProducer(bootstrap_servers=config["kafka"]["boostrap_servers"])

def main():
    
    lock = Lock()
    if os.path.exists("config.yaml"):
        with open("config.yaml") as file:
            config = yaml.load(file.read(), Loader=yaml.Loader)
    else:
        print("No {} file found".format("config.yaml"))
        exit()
    
    processes = []
    for i in range(len(config["cameras"])):
        processes.append(Process(target=run, args=(str(config["cameras"][i]["url"]), str(config["cameras"][i]["file-name"]), lock, str(config["kafka"]["topic"]) )))

    try:
        for process in processes:
            process.start()
        for process in processes:
            process.join()
    except KeyboardInterrupt:
        for process in processes:
            process.terminate()

def run(url, file_name, lock, topic): 
    success = fetch_audio(url, file_name)
    if success: 
        prediction = process_audio(url, file_name, lock) 
        produce(topic, prediction) 

def fetch_audio(url, file_name):
    if os.path.exists("{}.wav".format(file_name)):
        os.remove("{}.wav".format(file_name))
    try:
        subproc = subprocess.Popen('ffmpeg -i {}/axis-media/media.amp?videocodec=h264  -map 0:1 -c pcm_s16le {}.wav'.format(url, file_name), shell=True, preexec_fn=os.setpgrp, stdin=subprocess.PIPE)
        time.sleep(15)
        os.killpg(os.getpgid(subproc.pid), signal.SIGTERM)
        return True
    except KeyboardInterrupt:
        os.killpg(os.getpgid(subproc.pid), signal.SIGTERM)
    except: 
        return False

def process_audio(url, file_name, lock):
    lock.acquire()
    try: 
        output = os.popen('curl -X POST "http://localhost:5000/model/predict?start_time=0" -H "accept: application/json" -H "Content-Type: multipart/form-data" -F "audio=@{}.wav;type=audio/wav"'.format(file_name)).read()
    except: 
        print("Request Failed") 
    lock.release()
    return output 
    #print(json.loads(output))

def produce(topic, prediction):
    print("TEEST")
    print(prediction) 

    
    try: 
        obj = json.loads(prediction)
        if obj["status"] == "ok": 
            pred_list = obj["predictions"]
            print(pred_list)
            print(pred_list[1])
            
            ts = time.time()
            
            st = datetime.datetime.fromtimestamp(ts).strftime("%Y/%m/%dT%H:%M:%Sz")
            print("TIME")
            #print(get_timestamp())
            print(st)
            #print(ts) 
            audio_event = {}
            #audio_event['camera_id'] = 
            #audio_event['intersection'] = 
            #audio_event['pole_id'] = 
            #audio_event['timestamp'] = 
    except ValueError:
        print("Error loading JSON")

    #producer.send(topic, key, json.dumps(prediction).encode())


def get_timestamp():
    return 1000 * datetime.strptime(time.time(), "%Y/%m/%dT%H:%M:%Sz").timestamp()


if __name__ == '__main__': 
    main()    



# Run this through the system because Requests is a butt about the -F switch
#output = os.popen('curl -X POST "http://localhost:5000/model/predict?start_time=0" -H "accept: application/json" -H "Content-Type: multipart/form-data" -F "audio=@SirenTest.wav;type=audio/wav"').read()
#print(json.loads(output))



#ffmpeg -i rtsp://root:2u9JRlI#h6Ul@mlk-douglas-cam-3.research.utc.edu/axis-media/media.amp?videocodec=h264  -map 0:1 -c pcm_s16le audio.wav

#http://consumer:IyKv4uY7%g^8@10.199.51.162/axis-cgi/mjpg/video.cgi?resolution=1920x1080










 # subproc = subprocess.Popen('ffmpeg -i rtsp://root:2u9JRlI#h6Ul@mlk-douglas-cam-3.research.utc.edu/axis-media/media.amp?videocodec=h264  -map 0:1 -c pcm_s16le audio.wav', shell=True, preexec_fn=os.setpgrp, stdin=subprocess.PIPE)

































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
