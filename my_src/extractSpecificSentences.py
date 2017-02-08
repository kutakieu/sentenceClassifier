import urllib.request
import urllib.parse
from bs4 import BeautifulSoup
import time
import ssl
import MeCab
from os import listdir
from os.path import isfile, join
import re
import numpy as np
from random import shuffle
import random

wakati = MeCab.Tagger("-Owakati")
chasen = MeCab.Tagger("-Ochasen")

dirin = "/Users/tAku/Nextremer/data/wikidata_p_only_sameTopicANDsameSection2/wikidata_hierarchical_modified/"
fout = open("/Users/tAku/Nextremer/data/wikidata_p_only_sameTopicANDsameSection2/sentences_s00_onlyH3_Abst_meishi.txt","w",encoding="utf-8")

files = [f for f in listdir(dirin) if isfile(join(dirin, f))]

for _file in files:
    if re.search(".txt",_file) != None:
        fin = open(dirin + _file, encoding="utf-8")
        lines = fin.readlines()
        fin.close()

        for line in lines:
            # line = line[:-1]
            sentence = line
            line = line.split(" ")
            _id = line[0]
            line = "".join(line[1:])
            line = line.split("::")
            topic = line[0]
            headline = line[1]
            text = line[2]

            first_word = wakati.parse(text).split(" ")[0]
            form = chasen.parse(first_word).split("\t")[3].split("-")[0]
            if form != "名詞":
                continue
            # print(sentence)

            if headline == "概要" or headline == topic:
                fout.write(sentence)
                continue

            s_index = _id[len(_id)-2:len(_id)]
            H_sort = int(_id[-7])
            if int(s_index) == 0 and H_sort == 3:
            # if int(s_index) == 0:
                fout.write(sentence)
        # exit()
