# import gensim
import urllib.request
import urllib.parse
from bs4 import BeautifulSoup
import time
import ssl
import MeCab
from os import listdir
from os.path import isfile, join
import re
from gensim.models import Word2Vec
import numpy as np
from random import shuffle
import random

wakati = MeCab.Tagger("-Owakati")

fin = open("/Users/tAku/Nextremer/data/wikidata_pNdd_sameTopicANDsameSection2/2000_annotated_wakati.csv", encoding="utf-8")
lines = fin.readlines()
num_lines = len(lines)
max_length = 60
data_path = "/Users/tAku/Nextremer/data/"
model = Word2Vec.load_word2vec_format(data_path + 'foodVector.bin', binary=True)

unknown = np.zeros(200)
random.seed(0)

fout = open("/Users/tAku/Nextremer/data/wikidata_pNdd_sameTopicANDsameSection2/2000_vectorized.txt", "w", encoding="utf-8")
# for i in range(10):
#     print(lines[i].split(",")[0])

for line in lines:
    line = line.split(",")
    label = line[1]
    onehot = [1,0] if label == "t" else [0,1]
    morphemes = line[2].split(" ")
    morphemes = morphemes[:-1]
    if len(morphemes) < max_length:
        while len(morphemes) < max_length:
            morphemes.insert(0, "<unknown>")
    elif len(morphemes) > max_length:
        morphemes = morphemes[0:max_length]

    # fout.write(line[1] + ";")
    wordVecs = np.zeros((60,200))
    i = 0
    for morpheme in morphemes:
        try:
            score = model[morpheme]
            wordVecs[i] = score
        except:
            wordVecs[i] = unknown
        i += 1

    # fout.write(vector)
    print(wordVecs)
    print(wordVecs.shape)
    data = np.zeros((num_lines, 60, 200))
    data[0] = wordVecs
    print(data)
    print(data.shape)
    exit()


shuffle(lines)

def get_onehot_vector():
