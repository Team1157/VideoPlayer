#!/bin/sh
sudo pkill omxplayer

#omxplayer --loop --fs ./Video.mp4

# get rid of the cursor so we don't see it when videos are running
setterm -cursor off

# set here the path to the directory containing your videos
VIDEOPATH="./Videos"

# you can normally leave this alone
while true
do
  for entry in $VIDEOPATH/*
  do
    omxplayer --device x11 --no-osd $entry
    xset dpms force off
    xset dpms force on
  done
done
