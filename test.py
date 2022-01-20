import os
#IF NO GPU IS AVALIABLE
os.environ["CUDA_VISIBLE_DEVICES"]=""
from detectron2.engine import DefaultPredictor

import pickle
from utils import *
import cv2 as cv
import numpy as np
import time
import datetime
import weatherStation as WS
from urllib.request import urlopen, Request
import certifi
import ssl

cfg_save_path = "OD_cfg.pickle"

with open(cfg_save_path, 'rb') as f:\
    cfg = pickle.load(f)

cfg.MODEL.WEIGHTS = os.path.join(cfg.OUTPUT_DIR, "model_final.pth")
cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.5

predictor = DefaultPredictor(cfg)

mins = 0
startTime = 12
endTime = 5
hour = datetime.datetime.now().hour
clouds = ""
    
def getAllSkyImg():
    # Get image from allsky
    ssl._create_default_https_context = ssl._create_unverified_context
    req = Request('http://200.131.64.207/allsky/imagens340/AllSkyCurrentImage.JPG', headers={'User-Agent': 'Mozilla/5.0'})
    webpage = urlopen(req)
    arr = np.asarray(bytearray(webpage.read()), dtype=np.uint8)
    #image = cv.imread('test/M.jpg') #for testing up

    #image = "test/M.jpg"
    scores, img, v = on_image(arr, predictor)
    # Get local time (for tagging img)
    x = datetime.datetime.now()
    print(scores)

    # Save the img
    if scores > 0.80:
        print('Detected with ' + str(scores) + ' percent of chance')  
               
        cv.imwrite('results/'+'meteor-'+str(x.strftime("%d"))+str(x.strftime("%b"))+str((x.year))+'-'+str(x.strftime("%H"))+str(x.strftime("%M"))+str(x.strftime("%S"))+'.jpg', img)
        # plt.figure(figsize=(14,10))
        # plt.imshow(v.get_image())
        # plt.show()
    else:
        print("No detection")   
        
    
clouds = WS.getCloudStatus()

while hour >= startTime or hour < endTime :
    if "Overcast" not in clouds:
        getAllSkyImg()    
        clouds = WS.getCloudStatus()
        hour = datetime.datetime.now().hour
        time.sleep(60)
    else:
        print("Overcast")
        time.sleep(60)



        


    
