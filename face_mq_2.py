import pika
import time
import warnings
import sys
import tempfile
import json
from io import BytesIO
from models import *

warnings.filterwarnings(action='ignore')

#sys.path.append("/home/yerinyoon/code/anonymousNet/mobile_select_attribute/mobile_attribute_select")
#sys.path.append("/home/yerinyoon/code/anonymousNet/starGAN")
#origin_folder="/AppServer/mediozserver/someoneImage"
sys.path.append("/home/yerinyoon/code/cubig-custom")
sys.path.append('/home/choco/experiment/image_generation/photoguard')
#from deepface import DeepFace
import os 
#from  scp_utils import *
import cv2
import pandas as pd
#from face_diffusion import *
import argparse

import torchvision.transforms as T
from tqdm import tqdm
import requests


from collections.abc import Mapping

import boto3

#from src.configs.load_configs import load_configs
#import tempfile
import logging
import datetime
from PIL import Image
import argparse

parser = argparse.ArgumentParser()

parser.add_argument("--gpu", type=int, default=0)
parser.add_argument("--model", type=str, default="face1")


config = parser.parse_args()

if config.model=="face1":
    queue_name="face_queue_1"
else:
    queue_name="face_queue_2"
    
    


LOGGER = logging.getLogger(__name__)

class S3Connector:
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            configs={"s3": {
            "endpoint_url": "https://kr.object.ncloudstorage.com",
            "region_name": "kr-standard",
            "access_key": "EC979912E18255921EF5",
            "secret_key": "1A5A6F1C9623EB07DE613ED1F27C30DD37CA0D0F",
            "bucket_name": "neoda"
        },}

 
            #configs = load_configs()
            configs = configs['s3']

            service_name = 's3'
            endpoint_url = configs["endpoint_url"]
            region_name = configs["region_name"]
            access_key = configs["access_key"]
            secret_key = configs["secret_key"]
            bucket_name = configs["bucket_name"]

            cls.__instance = super(S3Connector, cls).__new__(cls)
            cls.__instance.s3_client = boto3.client(service_name, endpoint_url=endpoint_url, aws_access_key_id=access_key,
                      aws_secret_access_key=secret_key, region_name=region_name)
            cls.__instance.s3_resource = boto3.resource(service_name, endpoint_url=endpoint_url, aws_access_key_id=access_key,
                      aws_secret_access_key=secret_key, region_name=region_name)
            cls.__instance.bucket_name = bucket_name
        return cls.__instance

    def upload_file(self, s3_key, binary_data):
        try:
                       
            # self.s3_client.put_object(Bucket=self.bucket_name, Key=f"/")
            print(s3_key)
            self.s3_resource.Object(self.bucket_name, s3_key).put(Body=binary_data)
            LOGGER.info(f"File uploaded to S3: {s3_key}")
        except Exception as e:
            LOGGER.error(f"Error uploading file to S3: {e}")
            raise Exception(f"Error uploading file to S3: {e}")

    def download_file(self, s3_key, local_file_path):
        try:
            
            self.s3_client.download_fileobj(self.bucket_name, s3_key, local_file_path)
        except Exception as e:
            LOGGER.error(f"Error downloading file from S3: {e}")
            raise Exception(f"Error downloading file from S3: {e}")

    def delete_file(self, s3_key):
        try:
            self.s3_client.delete_object(Bucket=self.bucket_name, Key=s3_key)
            LOGGER.info(f"File deleted from S3: {s3_key}")
        except Exception as e:
            LOGGER.error(f"Error deleting file from S3: {e}")
            raise Exception(f"Error deleting file from S3: {e}")


def face(age, filepath, gender, device_ix, mask):
    print("start")
    try:
        age=age.split("-")[0]
        if age=="1": age=0
        elif age=="7": age=1
        elif age=="13": age=2
        elif age=="19": age=3
        elif age=="30": age=4
        else: age=5
        
    except:
        age=age
    
    
    #print(filename)
    
    # with tempfile.NamedTemporaryFile(suffix='.jpg') as temp_file:
    s3_file = BytesIO()
    #temppath=os.path.abspath(temp_file.name)
    s3.download_file(filepath, s3_file)
    print(s3_file)
    s3_data=[]
    for j in [True, False]:
        for i in range(6):
            
            gender=j
            age=i
            
            image, matrix=generate_character(s3_file, age, gender, mask)
            
            image=image.resize((1920, 1920))
            image.save(f"./{age}{gender}1{i}.jpg")
            buffer_img=io.BytesIO()
            
            image.save(buffer_img, format="png")
            image=buffer_img.getvalue()
            
            
            # print(img)
            
            #encoded_string_img = image.decode('ISO-8859-1')
                
            print("upload start")
            filename=filepath.split("/")[-1].split(".")[0]
            img_savepath=f"all/{device_ix}/private/{filename}{i}.png"
            json_savepath=f"all/{device_ix}/matrix/{filename}{i}.json"
            s3_data.append({
                "s3_file_path":f"private/{filename}{i}.png", 
                "s3_matrix_path":f"matrix/{filename}{i}.json"
                })
        
    #filename=str(datetime.datetime.now())+".jpg"
        # print(filename)
            s3.upload_file(img_savepath, image)
            s3.upload_file(json_savepath, json.dumps(matrix))
    return s3_data


def room(age, filepath, device_ix, mask):

    s3_file = BytesIO()
    #temppath=os.path.abspath(temp_file.name)
    s3.download_file(filepath, s3_file)
    s3_data=[]
    style=age
    for i in range(12):
        image, matrix=generate_room(s3_file, style, mask)
        
        buffer_img=io.BytesIO()
        image.save(buffer_img, format="png")
        image=buffer_img.getvalue()
        
        
        # print(img)
        
        #encoded_string_img = image.decode('ISO-8859-1')
            
        print("upload start")
        filename=filepath.split("/")[-1].split(".")[0]
        img_savepath=f"all/{device_ix}/private/{filename}{i}.png"
        json_savepath=f"all/{device_ix}/matrix/{filename}{i}.json"
        s3_data.append({
            "s3_file_path":f"private/{filename}{i}.png", 
            "s3_matrix_path":f"matrix/{filename}{i}.json"
            })
        
    #filename=str(datetime.datetime.now())+".jpg"
        # print(filename)
        s3.upload_file(img_savepath, image)
        s3.upload_file(json_savepath, json.dumps(matrix))
    return s3_data
    

def callback(ch, method, properties, body):
    data={}
    try:   
        print(f" [x] Received {body.decode()}")
    
        data = body.decode() # This is string data, you need to convert it back to dict using 'json' library
        data=json.loads(data)
        print(data)
        filepath=data["ori_file_path"]
        age=data["age"] #ROOM: style
        gender=data["gender"] #
        device_ix=data["device_ix"]
        model=data["model"]
        mask=data["style_data"]
        age_ix=data["age_ix"]
        favorite_ix=data["favorite_ix"]

        if model=="face1" or model=="face2":
            s3_data=face(age, filepath, gender, device_ix, mask)
    
        #elif model=="room1" or model=="room2":
            #s3_data=room(age, filepath, gender, device_ix, mask)
    
        if device_ix==None:
            data={"s3_data":s3_data,
                "model":model
                }
        
        else:        
            data={"s3_data":s3_data,
                "device_ix":device_ix,
                "model":model,
                "age_ix":age_ix,
                "favorite_ix":favorite_ix,
                "gender":gender,
                "ori_file_path":filepath
                }

    except Exception as e:
        print(str(e))
        
        image=Image.open("/home/yerin/code/i.png")
        buffer_img=io.BytesIO()            
        image.save(buffer_img, format="png")
        image=buffer_img.getvalue()
               
        # print(img)
        
        #encoded_string_img = image.decode('ISO-8859-1')
        s3_data=[]    
        print("upload start")
        for i in range(12):
            filename=filepath.split("/")[-1].split(".")[0]
            img_savepath=f"all/{device_ix}/private/{filename}{i}.png"
            json_savepath=f"all/{device_ix}/matrix/{filename}{i}.json"
            s3_data.append({
                "s3_file_path":f"private/{filename}{i}.png", 
                "s3_matrix_path":f"matrix/{filename}{i}.json"
                })
            matrix={
                    "seed":0 ,
                    "lora":[0, 0, 0, 0, 0, 0]       
                }
            
    #filename=str(datetime.datetime.now())+".jpg"
        # print(filename)
            s3.upload_file(img_savepath, image)
            s3.upload_file(json_savepath, json.dumps(matrix))
        data = {"s3_data":s3_data,
                "device_ix":device_ix,
                "model":model,
                "age_ix":age_ix,
                "favorite_ix":favorite_ix,
                "gender":gender,
                "ori_file_path": filepath
                }
            
    finally:
        print(data)
        res=requests.post("https://api.neoda.co.kr/api/v1/private_engine/mobile/result", json=data)
  
     
        # Your AI logic or function is here
        print(" [x] Done")
        ch.basic_ack(delivery_tag=method.delivery_tag)


s3=S3Connector()

try:
    # Connection parameters, including heartbeat settings
    connection_params = pika.ConnectionParameters(host='192.168.10.8', port=32001, heartbeat=600,
                                            credentials=pika.PlainCredentials('neoda', '8h4@pOGo4uchlc9lphuV'))

    connection = pika.BlockingConnection(connection_params)
    channel = connection.channel()

    channel.queue_declare(queue=queue_name, durable=True)
    channel.basic_consume(queue=queue_name, on_message_callback=callback)
    channel.basic_qos(prefetch_count=1)
    print(' [*] Waiting for messages. To exit press CTRL+C')

    # Start consuming with automatic heartbeats and reconnect on failure
    while True:
        try:
            connection.process_data_events()
        except pika.exceptions.AMQPConnectionError as e:
            print(f"Connection error: {e}. Reconnecting...")
            connection = pika.BlockingConnection(connection_params)
            channel = connection.channel()
            channel.queue_declare(queue=queue_name, durable=True)
            channel.basic_qos(prefetch_count=1)
            channel.basic_consume(queue=queue_name, on_message_callback=callback)
            continue

except KeyboardInterrupt:
    print(" [*] Exiting...")
finally:
    connection.close()

# channel.basic_qos(prefetch_count=1)

# channel.start_consuming()
