#!/bin/sh
sudo pkill omxplayer

#omxplayer --loop --fs ./Video.mp4

# get rid of the cursor so we don't see it when videos are running
setterm -cursor off

# set here the path to the directory containing your videos
VIDEOPATH="/mnt/storage/videos" 

# you can normally leave this alone
SERVICE="omxplayer"

for entry in $VIDEOPATH/*
do
    clear
    $SERVICE $entry > /dev/null

    while ps ax | grep -v grep | grep $SERVICE > /dev/null
    do
        sleep 5;
    done
done
