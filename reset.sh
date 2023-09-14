#!/bin/bash

# Terminate all Python processes
pkill -f "python ./room_mq.py*"
pkill -f "python ./face_mq.py*"

echo "All Python processes have been terminated." 
