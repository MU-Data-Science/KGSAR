"""
Created on %(September 2020)
@author: %(Nouf Arasheed)
This script is to count the occurrence/frequency of each word
"""

import csv
from operator import itemgetter

words = []
input_path = '/home/nouf/DL_Spanish/words/datasets/words-dataset/Feb2021-words.txt'
words_file=open(input_path, "r")
reader = csv.reader(words_file,delimiter=' ')
for line in reader:
    word=line[9]
    print(word)
    word = word.strip() #or some other preprocessing
    words.append(word) #storing everything in memory!

uniqWords = sorted(set(words)) #remove duplicate words and sort
words_list= []
for word in uniqWords:
    words_list.append ([words.count(word),word])
    print (words.count(word), word)



ordered_list = sorted(words_list, key=itemgetter(0))

output_path = "/home/nouf/DL_Spanish/words/datasets/words-dataset/Feb2021-words-count.txt"
filew=open(output_path, "w")
writer = csv.writer(filew, delimiter=',')

for w in ordered_list:
    writer.writerow([w[0],w[1]])


