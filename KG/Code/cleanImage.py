"""
Created on %(April 2019)
@author: %(Nouf Arasheed)
3x3 image bluring is used to remove background noise.
Last updated on 07/02/22 by Shivika Prasanna.
"""

import os
import sys
import numpy as np
import cv2
import random
from imutils import paths

# UNCOMMENT THE FOLLOWING SECTION IF USING THIS AS A STAND-ALONE CODE.
# import argparse

# ap = argparse.ArgumentParser()
# ap.add_argument("-i", "--input", required=True, help="input path")
# ap.add_argument("-o", "--output", required=True, help="output path")
# args = vars(ap.parse_args())

# input_path = str(args["input"])
# output_path = str(args["output"])

def clean(input_path, output_path):
    maxValue = 255
    imagePaths = sorted(list(paths.list_images((input_path))))
    print(imagePaths)
    random.shuffle(imagePaths)
    for imagePath in imagePaths:
        if imagePath.endswith('.jpg'):
            head, tail = os.path.split(imagePath)
            dir_path = os.path.join(output_path, head.split("/")[-1]+"/")
            os.makedirs(dir_path, exist_ok=True)

            img = cv2.imread(imagePath)
            blur = cv2.blur(img, (3, 3))
            th, dst = cv2.threshold(blur, 127, maxValue, cv2.THRESH_BINARY)
            
            cv2.imwrite(os.path.join(dir_path, '', tail), dst)
            print("Storing image here:", os.path.join(dir_path, tail))

    print("Done cleaning!")

# UNCOMMENT THIS IF USING THIS AS A STAND-ALONE CODE.
# clean(input_path, output_path)