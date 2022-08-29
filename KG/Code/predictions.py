'''
Developed by Shivika Prasanna on 05/17/2021.
Last updated on 09/10/2021.
Get predictions using Keras-OCR retrained weights.
Run in terminal as:  python3 predictions.py -i <images_path> -o <output_path> -j <json_path> -m <model_path>
'''

import numpy as np
import pandas as pd
import json

import os.path
import argparse

import matplotlib.pyplot as pyplot
import keras_ocr

# UNCOMMENT THE FOLLOWING SECTION IF USING THIS AS A STAND-ALONE CODE.
# import cleanImage

# ap = argparse.ArgumentParser()
# ap.add_argument("-m", "--model", required=True, help="model path")
# ap.add_argument("-i", "--input", required=True, help="input path")
# ap.add_argument("-o", "--output", required=True, help="output path")
# ap.add_argument("-j", "--json", required=True, help="output json path")
# args = vars(ap.parse_args())

# model_path = str(args["model"])
# image_input_path = str(args["input"])
# image_output_path = str(args["output"])
# json_output_path = str(args["json"])

# cleanImage.clean(image_input_path, image_output_path)

def predict(model_path, image_output_path, json_output_path):
    
    DEFAULT_ALPHABET = ''.join(['"', '=', 'C', 'D', 'J', 'N', 'R', '_', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'x', 'y', 'z', 'ç', 'ñ', 'ü'])

    detector = keras_ocr.detection.Detector()
    recognizer = keras_ocr.recognition.Recognizer(alphabet=DEFAULT_ALPHABET)
    recognizer.model.load_weights(model_path)

    for folder in os.listdir(image_output_path):
        if not folder.startswith('.'):
            for filename in os.listdir(os.path.join(image_output_path, folder)):
                dir_path = os.path.join(json_output_path, folder)
                os.makedirs(dir_path, exist_ok=True)
                image_result = {}
                json_file = filename.replace('.jpg', '.json')
                image_path = os.path.join(image_output_path, folder, filename)
                json_path = os.path.join(dir_path, json_file)
                print("Storing JSON here: ", json_path)

                image = keras_ocr.tools.read(image_path)
                boxes = detector.detect(images=[image])[0]
                predictions = recognizer.recognize_from_boxes(
                    images=[image], box_groups=[boxes.tolist()])

                image_result["filename"] = filename
                image_result["output"] = []

                for index, item in enumerate(zip(boxes.tolist(), predictions[0])):
                    image_result["output"].append(
                        {"prediction": item[1], "box": item[0]})

                json.dump(image_result, open(json_path, "w"))

    print("Done predicting!")

# UNCOMMENT THE FOLLOWING SECTION IF USING THIS AS A STAND-ALONE CODE.
# predict(model_path, image_output_path, json_output_path)