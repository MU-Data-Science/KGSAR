"""
Created on %(September 2020)
@author: %(Nouf Arasheed)
This script is to get the unique words and count them 
"""

import csv
words = []
input_path = '/home/nouf/DL_Spanish/words/datasets/words-dataset/Feb2021-words.txt'
words_file=open(input_path, "r")
reader = csv.reader(words_file,delimiter=' ')
for line in reader:
    word=line[9]
    print(word)
    word = word.strip() #or some other preprocessing
    words.append(word) #storing everything in memory!

c=0
unique_words = []
for word in words:
    if word not in unique_words:
        unique_words.append(word)
        c +=1

print(c)

output_path = "/home/nouf/DL_Spanish/words/datasets/words-dataset/Feb2021-unique-words.txt"
unique_words_file=open(output_path, "w")
writer = csv.writer(unique_words_file, delimiter=' ')

for uw in unique_words:
    writer.writerow([uw])
#    print(uw)
