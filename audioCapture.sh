#!/bin/bash
CAMS="root:2u9JRlI#h6Ul@mlk-douglas-cam-3.research.utc.edu consumer:IyKv4uY7%g^8@10.199.51.170 consumer:IyKv4uY7%g^8@10.199.51.147"

FILES=("douglas_audio.wav" "central_audio.wav" "lindsay_audio.wav")
echo ${FILES[1]}

echo "~/Desktop/${FILES[1]}"

#ffmpeg -i rtsp://root:2u9JRlI#h6Ul@mlk-douglas-cam-3.research.utc.edu/axis-media/media.amp?videocodec=h264  -map 0:1 -c pcm_s16le ~/Desktop/audiyd.wav -v debug 

for i in $CAMS
do
  echo connecting...
  ffmpeg -i rtsp://$i/axis-media/media.amp?videocodec=h264 -map 0:1 -c pcm_s16le audiyd.wav

done


