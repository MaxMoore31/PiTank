echo "Connecting to:"
echo $1
mplayer -fps 200 -demuxer h264es ffmpeg://tcp://$1:8090
