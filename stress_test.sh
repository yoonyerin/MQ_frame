#!/bin/bash

# Number of Python processes to start
num_processes=5

# Loop to start Python processes
for ((i=1; i<=3; i++))
do 
    python ./face_mq.py --model="face1" &

done

for ((i=1; i<=1; i++))
do 
    python ./face_mq.py --model="face2" &
    python ./room_mq.py
done

