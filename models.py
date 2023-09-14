import json
import requests
import io
import base64
from PIL import Image, PngImagePlugin
import random

url = "http://127.0.0.1:5000"


# with open("/home/yerinyoon/automatic111/API_test/sample image/female/face_0.jpg", "rb") as img:
#     base64_image=base64.b64encode(img.read()).decode("utf8")

# #####
a=str(random.random())
b=str(random.random())
c=str(random.random())
d=str(random.random())
e=str(random.random())
f=str(random.random())
seed=random.random()

room_seed=random.random()

# print(a, b, c, d, e, f)
prompt_girl=[
    ## age_1
    f" age:1, extremely clear white skin, baby eyes,   1baby, Korean baby, extremely young baby, cuty face, innocent baby, extremely beautiful big black sparkling eyes, clear skin,  chubby face,\
ultra detailed eyes, black eyes, extremely detailed, simple nostalgic, nice spring afternoon lighting, (professional iPhone photo), baby lips", 
    ## age_2
    f" age:7 , 1baby, Korean baby, extremely young girl, cuty face, innocent baby, extremely beautiful big black sparkling eyes, clear skin,  \
ultra detailed eyes, black eyes, extremely detailed, simple nostalgic, nice spring afternoon lighting, (professional iPhone photo)",
    ## age_3
    f"age:13, Korean young beautiful teenager girl, 1girl, cuty face, innocent girl,  \
        beautiful big black sparkling eyes, clear skin, very small face, oval face, Photo of a Beautiful Korean kpop idol girl,  very slim chin,\
    ultra detailed eyes, black eyes, extremely detailed, simple nostalgic, nice spring afternoon lighting, (professional iPhone photo) ,<lora:koreanDollLikeness_v15:{a}>, <lora:aespakarinalora:{b}>, <lora:asian_beauty_v2:{c}>,\
    <lora:majicmixRealistic_betterV2V25:{d}>, <lora:majicmixSombre_v20:{e}>,<lora:jesslynjkt48:{f}>",
    ##age_4
    f"extremely clear skin, extremely realistic face, age:20, Korean young beautiful girl, 1girl, cuty face, innocent girl,  beautiful big black sparkling eyes, actress face, mascara, clear skin, very small face, oval face, Photo of a Beautiful Korean kpop idol girl,  very slim chin,\
    ultra detailed eyes, black eyes, extremely detailed, simple nostalgic, nice spring afternoon lighting, (professional iPhone photo) ,<lora:koreanDollLikeness_v15:{a}>, <lora:aespakarinalora:{b}>, <lora:asian_beauty_v2:{c}>,\
    <lora:majicmixRealistic_betterV2V25:{d}>, <lora:majicmixSombre_v20:{e}>,<lora:jesslynjkt48:{f}>",
    ##age_5
    f"extremely realistic face, age:70, old woman, Korean beautiful graceful woman, wrinkle face, 1woman, cuty face, innocent girl,  beautiful big black sparkling eyes, actress face, mascara, clear skin, very small face, oval face, Photo of a Beautiful Korean kpop idol girl,  very slim chin,\
    ultra detailed eyes, black eyes, extremely detailed, simple nostalgic, nice spring afternoon lighting, (professional iPhone photo) ,<lora:koreanDollLikeness_v15:0.1>, <lora:aespakarinalora:{b}>, <lora:asian_beauty_v2:0.1>,\
    <lora:majicmixRealistic_betterV2V25:{d}>, <lora:majicmixSombre_v20:0.1>,<lora:jesslynjkt48:{f}>",
    ##age_6
    f"extremely realistic face, beautiful Korean woman, age:70, beautiful graceful woman, 1woman, beautiful grandma, innocent girl,  beautiful big black sparkling eyes, actress face, mascara,  very small face, oval face,  very slim chin,\
    ultra detailed eyes, black eyes, extremely detailed, simple nostalgic, nice spring afternoon lighting, (professional iPhone photo), ,<lora:koreanDollLikeness_v15:0.1>, <lora:aespakarinalora:0.1>, <lora:asian_beauty_v2:0.1>,\
    <lora:majicmixRealistic_betterV2V25:{d}>, <lora:majicmixSombre_v20:0.1>,<lora:jesslynjkt48:0.1>"       
        ]

prompt_man=[
    ## age_1
    f"age:1 ,baby face, 1baby, Korean baby, extremely young baby, cuty face, innocent baby, extremely beautiful big black sparkling eyes, clear skin,  chubby face,\
ultra detailed eyes, black eyes, extremely detailed, simple nostalgic, nice spring afternoon lighting, (professional iPhone photo), baby lips", 
    ## age_2
    f"age:7 , 1boy, 1baby, Korean baby, extremely young boy, cuty face, innocent baby, extremely beautiful big black sparkling eyes, clear skin,  \
ultra detailed eyes, black eyes, extremely detailed, simple nostalgic, nice spring afternoon lighting, (professional iPhone photo)",
    ## age_3
    f"age:13,thick eyebrows, young handsome teenager boy, 1boy, beautiful face, innocent boy,  beautiful big black sparkling eyes, clear skin, very small face, oval face, Photo of a Beautiful Korean kpop idol boy,  very slim chin,\
    ultra detailed eyes, black eyes, extremely detailed, simple nostalgic, nice spring afternoon lighting, (professional iPhone photo) , <lora:aespakarinalora:{b}>,\
    <lora:majicmixRealistic_betterV2V25:{d}>, <lora:jesslynjkt48:{f}>",
    ##age_4
    f"age:20, thick eyebrows,expert man, boyish, masculine, young handsome boy, 1boy, beautiful face, charming man,  beautiful big black sparkling eyes, actor face,  clear skin,  oval face, Photo of a Beautiful Korean kpop idol boy,  very slim chin,\
    ultra detailed eyes, black eyes, extremely detailed, simple nostalgic, nice spring afternoon lighting, (professional iPhone photo), straight teeth",
    ##age_5
    f" age:50,thick eyebrows,old Korean man, wrinkle face, beard, expert man,mustache, masculine, boyish ,beautiful graceful man,gentle man, 1man, beautiful face, charming man,  beautiful big black sparkling eyes, actor face,  clear skin, oval face, Photo of a Beautiful Korean kpop idol boy,\
    ultra detailed eyes, black eyes, extremely detailed, simple nostalgic, nice spring afternoon lighting, (professional iPhone photo), straight teeth",
    ##age_6
    f" age:90,thick eyebrows, old Korean man, extremely wrinkle face, old gentle man,  beard,expert man ,mustache, masculine, boyishbeautiful graceful man, 1man, grandpa, charming man,  beautiful big black sparkling eyes, actor face, \
    ultra detailed eyes, black eyes, extremely detailed, simple nostalgic, nice spring afternoon lighting, (professional iPhone photo) , straight teeth"       
        ]

negative_prompt_woman="(worst_quality:2.0) low quality, blur ,deformed ugly, pixelated, accessory, ring, ear ring, face distortion, monkey face, big lip, bloodshot eyes"
negative_prompt_man="woman, madam, makeup, mascara, lipstick(worst_quality:2.0) low quality, blur ,deformed ugly, pixelated, accessory, ring, ear ring, face distortion, monkey face, big lip, bloodshot eyes"
    
    
#####################################################################################################
#               ROOM
#####################################################################################################


controlnet_module =  "depth_midas"
controlnet_model="control_depth-fp16 [400750f6]"#control_v11f1p_sd15_depth [e3b0c442]",
   
style_list = [
    "modern",
    "minimal",
    "natural",
    "North European",
    "retro",
    "classic",
    "antique",
    "provence",
    "romantic",
    "industrial",
]
nurl = "http://127.0.0.1:5000"

# prompt=prompt_girl[3]
# age=4

# payload = {
#     "init_images": [base64_image],
#     "prompt":prompt[age-1],
#     "negative_prompt": negative_prompt,
#    # "height":height,
#    # "width": width,
#     "steps":20,
#     "cfg_scale":7,
#     "seed": seed,
#     "restore_face":False,
#     "denoising_strength": 0.05,
#     "sampler_name":"Euler",
#     "alwayson_scripts": {
#     "ADetailer": {
#       "args": [
#         True,
#         {
#           "ad_model": "face_yolov8n.pt",
#           "ad_prompt": prompt,
#           "ad_negative_prompt":negative_prompt,
#           "ad_denoising_strength": 0.2,
#           "ad_inpaint_only_masked": True,
#           "ad_inpaint_width": 512,
#           "ad_inpaint_height": 512,
#           "ad_use_steps": True,
#           "ad_steps": 40,
#           "ad_use_cfg_scale": True,
#           "ad_cfg_scale": 7.0,
#           "ad_use_sampler":True,
#           "ad_sampler": "Euler",
#           "ad_use_noise_multiplier": True,
#           "ad_noise_multiplier": 1.0,
#           "ad_use_clip_skip": True,
#           "ad_clip_skip": 2,
#           "ad_restore_face": False,
#           "ad_controlnet_model": "None"
#         } ]
#     }
#   }}
    
    

# response = requests.post(url=f'{url}/sdapi/v1/img2img', json=payload)
# r = response.json()

# for i in r['images']:
#     image = Image.open(io.BytesIO(base64.b64decode(i.split(",",1)[0])))

#     png_payload = {
#         "image": "data:image/png;base64," + i
#     }
#     response2 = requests.post(url=f'{url}/sdapi/v1/png-info', json=png_payload)

#     pnginfo = PngImagePlugin.PngInfo()
#     pnginfo.add_text("parameters", response2.json().get("info"))
#     image.save('output_control_1.png', pnginfo=pnginfo)

def generate_room(image, mask, width, height):
    try: 
        seed=mask["seed"]
        mask=mask["style"]
                
    except:
        seed=int(random.random()*10000)    
    try:
        style=style_list[mask-1]
    except:
        mask=1
        style=style_list[mask-1]
    main_prompt = f"a photo of a {style} styled room"
    
    base64_image=base64.b64encode(image.getvalue()).decode("utf8")
    # with open(image, "rb") as f_img:
    #     base64_image = base64.b64encode(f_img.read()).decode('utf-8')
    
    # base64_image=base64.b64encode(encoded_image.getvalue()).decode("utf8")
    
    
   # print(base64_image)
    
    
    payload = {
                "prompt": main_prompt,
                "negative_prompt": "",
                "batch_size": 1,
                "steps": 20,
                "cfg_scale": 7,
                "width": width,
                "height": height,
                # "enable_hr": False,
                # "hr_upscaler": "ESRGAN_4x",
                "sampler_index": "Euler a",
                "save_images": True,
                "alwayson_scripts": {
                    "controlnet": {
                        "args": [
                            {
                                "input_image": base64_image,
                                "module": controlnet_module,
                                "model": controlnet_model
                                # "processor_res": 512,
                            }
                        ]
                    }
                }
            }
    response = requests.post(url=f'{url}/sdapi/v1/txt2img', json=payload)

    r = response.json()
    result = r['images'][0]
    image = Image.open(io.BytesIO(base64.b64decode(result.split(",", 1)[0])))
    
   
    matrix={
        "seed":seed,
        "style": mask        
    }
    print("room_done")
    return image, matrix
    
    
    
## face1, face2 모두 이 함수를 쓰고, face 2일 경우 None이던 mask에 (a, b, c, d, e,f seed) 담아서 해당 부분 픽스하기.
def generate_character(image, age, gender, mask):
    if gender: negative_prompt=negative_prompt_woman
    
    else: negative_prompt=negative_prompt_man
    
    url = "http://127.0.0.1:5000"
    
    base64_image=base64.b64encode(image.getvalue()).decode("utf8")
    if mask==None:
        a=0.8#str(random.random())
        b=str(random.random())
        c=str(random.random())
        d=str(random.random())
        e=str(random.random())
        f=0#str(random.random())
        seed=int(random.random()*10000)
    else:
        a, b,c, d, e, f=mask["lora"]
        seed=mask["seed"]      
    
    # print(a, b, c, d, e, f, seed)
    
    if gender:
        prompt=prompt_girl
    else: prompt=prompt_man
    print(f"base64:{base64_image}")
    # print(age-1)
    # print(prompt[int(age)])
    payload = {
    "init_images": [base64_image],
    "prompt":prompt[int(age)],
    "negative_prompt": negative_prompt,
   # "height":height,
   # "width": width,
    "steps":20,
    "cfg_scale":7,
    "seed": seed,
    "restore_face":False,
    "denoising_strength": 0.1,
    "sampler_name":"Euler",
    "alwayson_scripts": {
    "ADetailer": {
      "args": [
        True,
        {
          "ad_model": "face_yolov8n.pt",
          "ad_prompt": prompt[int(age)],
          "ad_negative_prompt":negative_prompt,
          "ad_denoising_strength": 0.3,
          "ad_inpaint_only_masked": True,
          "ad_inpaint_width": 512,
          "ad_inpaint_height": 512,
          "ad_use_steps": True,
          "ad_steps": 40,
          "ad_use_cfg_scale": True,
          "ad_cfg_scale": 7.0,
          "ad_use_sampler":True,
          "ad_sampler": "Euler",
          "ad_use_noise_multiplier": True,
          "ad_noise_multiplier": 1.0,
          "ad_use_clip_skip": True,
          "ad_clip_skip": 2,
          "ad_restore_face": False,
          "ad_controlnet_model": "None"
        } ]
    }
  }}
    print(payload)
    response = requests.post(url=f'{url}/sdapi/v1/img2img', json=payload)
    r = response.json()
    print(r)
    i=r["images"][0]
    
    image = Image.open(io.BytesIO(base64.b64decode(i.split(",",1)[0])))
    #image.save(f"./{seed}.jpg")
    matrix={
        "seed":seed ,
        "lora":[a, b, c, d, e, f]       
    }
    
    return image, matrix