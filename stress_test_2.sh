#!/bin/bash

# Number of Python processes to start
num_processes=5

# Loop to start Python processes
for ((i=1; i<=3; i++))
do
    nohup python ./face_mq_2.py --model="face1" > logs/face1.log 2>&1 &
done

for ((i=1; i<=1; i++))
do
    nohup python ./face_mq_2.py --model="face2" > logs/face2.log 2>&1 &
    nohup python ./room_mq_2.py > logs/room.log 2>&1 &
done

