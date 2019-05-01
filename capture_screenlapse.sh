#!/bin/bash
#
# run python script screencapture 
#
export captureLocation=~/studio_capture/images/
script_location=$(dirname $0)

python $script_location/capture_screenlapse.py 