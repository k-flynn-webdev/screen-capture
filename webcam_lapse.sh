#!/bin/bash
#
# run python script screencapture 
#
export captureLocation=~/studio_capture/cam/
script_location=$(dirname $0)

# python $script_location/webcam.py 

~/studio_x_toolsfiles/ffmpeg/ffmpeg -f avfoundation -list_devices true -i ""