'''
Developed by Shivika Prasanna on 05/25/2021.
Last updated on 09/20/2021.
Consume all predictions in JSON format to generate a KG.

xlrd, rdflib, imutils, matplotlib
Run in terminal as:  > java -server -Xmx4g -jar Downloads/blazegraph.jar
> time python3 kg.py -i <full path to root containing original images> -o <full path to store cleaned images> -j <full path to store JSON files> -r <path to JSON files>  -m <path to model> -e <excel file>
'''

import sys, os
from datetime import datetime
import json, csv, xlrd
import pandas as pd

import argparse

from rdflib import Graph, Literal, RDF, URIRef, Namespace
from rdflib.namespace import FOAF , XSD

import cleanImage
import predictions

ap = argparse.ArgumentParser()
ap.add_argument("-r", "--rootdir", required=True, help="root directory")
ap.add_argument("-i", "--input", required=False, help="input images path")
ap.add_argument("-o", "--output", required=True, help="output images path")
ap.add_argument("-j", "--json", required=False, help="output json path")
ap.add_argument("-m", "--model", required=True, help="model path")
ap.add_argument("-e", "--excel", required=True, help="excel document")

args = vars(ap.parse_args())
rootpath = str(args['rootdir'])
image_input_path = str(args["input"]) if args["input"] is not None else args["input"]
image_output_path = str(args["output"])
json_output_path = str(args["json"])  if args["json"] is not None else args["json"]
model_path = str(args["model"])
excel = str(args['excel'])

# STEP 1: Clean OG-Images and store in cleaned-Images
if image_input_path is not None:
    cleanImage.clean(image_input_path, image_output_path)
# STEP 2: Read cleaned-Images, get predictions and store in JSON_output_path
if json_output_path is not None:
    predictions.predict(model_path, image_output_path, json_output_path)

# STEP 3: Read JSON_output_path and store predictions and other knowledge in KG
g2 = Graph()
b = Namespace('http://kgsar.org/')

# Change .csv to JSON format
out = pd.read_excel(excel)
out.to_csv("./data.csv", index=False, encoding='utf-8')
data = pd.read_csv("./data.csv", sep=",")
mapping = {item:i for i, item in enumerate(data["Name of Notary"].unique())}
data["ID"] = data["Name of Notary"].apply(lambda x: mapping[x])
data.to_csv("./data.csv", index=False)

for index, row in data.iterrows():
    g2.add((URIRef('http://kgsar.org/notary{}'.format(str(row['ID']))), RDF.type, b.notary))
    g2.add((URIRef('http://kgsar.org/notary{}'.format(str(row['ID']))), b.hasYear, Literal(row['Year of tenure'])))
    g2.add((URIRef('http://kgsar.org/notary{}'.format(str(row['ID']))), b.writtenBy, Literal(row['Name of Notary'].strip())))

temp = {'y':[], 'k': []}
final_res = []
gramIndex = 1
ind_ctr = 0
docID = ''

for d in os.walk(rootpath):
    for dir in d[1]:
        path = os.path.join(d[0], dir)
        print("Path in kg.py: ", path)
        if os.path.isdir(path) and not dir.startswith('.'):
            for filename in os.listdir(path):
                if os.path.isfile(os.path.join(path, filename)) and filename.endswith('.json'):
                    f_path = os.path.join(path, filename)
                    documentIndex = path.split('/')[-1]
                    docID = documentIndex
                    print("Currently processing: ", path)
                    document = URIRef('http://kgsar.org/document/{}'.format(documentIndex))
                    g2.add((document, RDF.type, b.document))
                    with open(f_path) as jfile:
                        p = json.load(jfile)
                        if 'filename' in p:
                            if p['filename'].endswith('.json'):
                                pageIndex = p['filename'].replace('.json', '')
                            elif p['filename'].endswith('.jpg'):
                                pageIndex = p['filename'].replace('.jpg', '')
                            else:
                                pageIndex = p['filename']

                            page = URIRef('http://kgsar.org/document/{}/page{}'.format(documentIndex, pageIndex))
                            g2.add((page, RDF.type, b.page))
                            g2.add((document, b.hasPage, page))

                        if 'output' in p:
                            for wordIndex, item in enumerate(p['output']):
                                ind_ctr += 1
                                print("Index ctr: ", ind_ctr)
                                # wordIndex = datetime.datetime.now().time()
                                temp_word = None
                                if 'Yolo' in path:
                                    temp_word = 'y'
                                    word = URIRef(
                                        'http://kgsar.org/document/{}/page{}/word{}{}'.format(documentIndex, pageIndex, "Y", wordIndex))                         
                                elif 'Keras' in path:
                                    temp_word = 'k'
                                    word = URIRef(
                                        'http://kgsar.org/document/{}/page{}/word{}{}'.format(documentIndex, pageIndex, "K", wordIndex))

                                if (documentIndex, pageIndex, wordIndex) in temp[temp_word]:
                                    print("duplicate!!! ", pageIndex, path)
                                else:
                                    temp[temp_word].append((pageIndex, wordIndex))
                                
                                g2.add((word, RDF.type, b.word))
                                g2.add((page, b.hasWord, word))
                                if item['prediction'] is not None:
                                    if item['prediction'] != "":
                                        g2.add((word, b.wordValue, Literal(item['prediction'])))
                                
                                upper_length = len(item['prediction'])
                                lower_length = 3

                                for j in range(lower_length, (upper_length-1)):
                                    for i in range(upper_length-lower_length+1):
                                        if upper_length >= lower_length: 
                                            if 'Yolo' in path:
                                                gram = URIRef(
                                                    'http://kgsar.org/document/{}/page{}/word{}{}/gram{}'.format(documentIndex, pageIndex, "Y", wordIndex, gramIndex))
                                                gramIndex += 1
                                            elif 'Keras' in path:
                                                gram = URIRef(
                                                    'http://kgsar.org/document/{}/page{}/word{}{}/gram{}'.format(documentIndex, pageIndex, "K", wordIndex, gramIndex))
                                                gramIndex += 1
                                            g2.add((gram, RDF.type, b.gram))
                                            g2.add((word, b.hasGram, gram))
                                            g2.add((gram, b.gramValue, Literal(
                                                item['prediction'][i:i+lower_length])))
                                    lower_length += 1

                                if 'Yolo' in path:
                                    boundingBox = URIRef(
                                        'http://kgsar.org/document/{}/page{}/boundingBox{}{}'.format(documentIndex, pageIndex, "Y", wordIndex))
                                elif 'Keras' in path:
                                    boundingBox = URIRef(
                                        'http://kgsar.org/document/{}/page{}/boundingBox{}{}'.format(documentIndex, pageIndex, "K", wordIndex))
                                
                                g2.add((boundingBox, RDF.type, b.boundingBox))
                                g2.add((word, b.at, boundingBox))

                                if 'Yolo' in path:
                                    g2.add((boundingBox, b.topLeftx, Literal(item['box'][0], datatype=XSD.float)))
                                    g2.add((boundingBox, b.topLefty, Literal(item['box'][1], datatype=XSD.float)))
                                    g2.add((boundingBox, b.botRightx, Literal(item['box'][2], datatype=XSD.float)))
                                    g2.add((boundingBox, b.botRighty, Literal(item['box'][3], datatype=XSD.float)))
                                    g2.add((word, b.predictedBy, b.yolo))
                                elif 'Keras' in path:
                                    row = item["box"]
                                    x1, x2, y1, y2 = item["box"]
                                    x1 = row[0][0]
                                    x2 = row[1][0]
                                    x3 = row[2][0]
                                    x4 = row[3][0]

                                    y1 = row[0][1]
                                    y2 = row[1][1]
                                    y3 = row[2][1]
                                    y4 = row[3][1]

                                    top_left_x = min([x1,x2,x3,x4])
                                    top_left_y = min([y1,y2,y3,y4])
                                    bot_right_x = max([x1,x2,x3,x4])
                                    bot_right_y = max([y1,y2,y3,y4])

                                    g2.add((boundingBox, b.topLeftx, Literal(top_left_x, datatype=XSD.float)))
                                    g2.add((boundingBox, b.topLefty, Literal(top_left_y, datatype=XSD.float)))
                                    g2.add((boundingBox, b.botRightx, Literal(bot_right_x,  datatype=XSD.float)))
                                    g2.add((boundingBox, b.botRighty, Literal(bot_right_y,  datatype=XSD.float)))
                                    g2.add((word, b.predictedBy, b.keras))
                        #print(g2.serialize(format='turtle').decode('utf-8'))
        if docID != '':
            g2.serialize(docID + '-words-'+datetime.today().strftime('%Y-%m-%d')+'.ttl',format='turtle')
            print("Saving turtle file for DocID {}".format(docID))
            docID = ''
        
print("Populated the KG!")

