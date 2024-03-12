"""
Created on %(January 2020)
@author: %(Nouf Arasheed)
This script is used to resize & pad word image with white space to make all images have the same size

"""

import cv2
import sys
import random
import os
from imutils import paths
path = "/home/nouf/DL_Spanish/words/one-shot-dataset/" 
outpath = '/home/nouf/DL_Spanish/words/one-shot-train/'
# grab the image paths and randomly shuffle them
imagePaths = sorted(list(paths.list_images((path))))
random.seed(42)
random.shuffle(imagePaths)
target_size = 200
color = [255, 255, 255]

# loop over the input images
for imagePath in imagePaths:
    head, tail = os.path.split(imagePath)
    wordpath=os.path.basename(head)
    image = cv2.imread(imagePath)
    old_size = image.shape[:2] # old_size is in (height, width) format

    ratio = float(target_size)/max(old_size)
    new_size = tuple([int(x*ratio) for x in old_size])

    # new_size should be in (width, height) format
    image = cv2.resize(image, (new_size[1], new_size[0]))

    delta_w = target_size - new_size[1]
    delta_h = target_size - new_size[0]
    top, bottom = delta_h//2, delta_h-(delta_h//2)
    left, right = delta_w//2, delta_w-(delta_w//2)
    new_image = cv2.copyMakeBorder(image, top, bottom, left, right, cv2.BORDER_CONSTANT,value=color)
    
    save_path = outpath+wordpath+"/"
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    cv2.imwrite(save_path+tail, new_image)
