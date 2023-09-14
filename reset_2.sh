#!/bin/bash

# Terminate all Python processes
pkill -f "python ./room_mq_2.py*"
pkill -f "python ./face_mq_2.py*"

echo "All Python processes have been terminated." 
