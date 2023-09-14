#!/bin/bash

for i in 1, 2, 3, 4, 5
do
    python ./face_mq.py --gpu=0 --model=face1 &
done
for i in 1, 2
do 
    python ./face_mq.py --gpu=0 --model=face2 &
done
for i in 1, 2
do 
python ./room_mq.py --gpu=0 &
done