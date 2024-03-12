"""
Created on %(January 2020)
@author: %(Nouf Arasheed)
This script is usedconcat all the labels form all the pages in one single .txt file
""" 

import os
pages = os.listdir("/home/nouf/DL_Spanish/words/de_Cray/csvs/")
inpath = "/home/nouf/DL_Spanish/words/de_Cray/"
output_path = "/home/nouf/DL_Spanish/words/datasets/words-dataset/"

for p in pages:
    print(p)
    fullpath = inpath + str(p)
    print(fullpath)
    with open(output_path + 'Feb2021-words.txt', 'a') as outfile:
        with open(fullpath) as infile:
            outfile.write(infile.read())


