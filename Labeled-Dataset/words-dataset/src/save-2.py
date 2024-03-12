"""
Created on %(January 2020)
@author: %(Nouf Arasheed)
This script reads the word image's transcription and coordinates from the csv file and save each image as .png image. It Also create directory for each page to store the words written in that page
"""

# Improting Image class from PIL module
from PIL import Image
import csv
import random
import sys
import os
pages = os.listdir("/home/nouf/DL_Spanish/words/de_Cray/imgs/")
inpath = "/home/nouf/DL_Spanish/words/de_Cray/"

outpath = "/home/nouf/DL_Spanish/words/datasets/words-dataset/"


#for name in pages:
    #directory1= outpath+"a"+name
    #directory2= directory1 + "/" + "-000u"
    #os.makedirs(directory1)
    #os.makedirs(directory2)

#for name in pages:
 #   directory= "a"+name+
  #  os.makedirs(directory)

for p in pages:
    name = os.path.splitext(p)[0]
    print(name)   
    directory1= outpath+"a"+name
    directory2= directory1 + "/" + "a"+name+"-000u"
    if not os.path.exists(directory1):
        os.makedirs(directory1)
    if not os.path.exists(directory2):
        os.makedirs(directory2)
    folder = directory2 
    #im = Image.open(inpath+"pages/"+name+".jpg")
    im = Image.open(inpath+name+".jpg")
    width, height = im.size
    with open(inpath+name+"_labels.csv") as f:
    #with open(inpath+"words-files/"+name+"_labels.csv") as f:
        cf = csv.reader(f,delimiter =' ')
        for row in cf:
            left=int(row[4])
            top=int(row[5])
            right=int(row[6])
            bottom=int(row[7])
            im1 = im.crop((left, top, right, bottom))
            print(folder+"/"+row[0]+".png")
            im1.save(folder+"/"+row[0]+".png","PNG")

        #im1.save(outpath+row[0]+"/"+str(random.randint(1,7000))+".png","PNG")

