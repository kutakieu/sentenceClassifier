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

wakati = MeCab.Tagger("-Owakati")
dirin = "/Users/tAku/Nextremer/data/wikidata_pNdd_sameTopicANDsameSection2/wikidata_hierarchical_modified/"
files = [f for f in listdir(dirin) if isfile(join(dirin, f))]
num_files = len(files)
max_length = 0
max_sentence = ""
ave_length = 0
num_sentence = 0
SD = 0
less60 = 0
for _file in files:
    if re.search(".txt",_file) != None:
        num_files -= 1
        print(_file + "  残り：" + str(num_files))
        fin = open(dirin + _file, encoding="utf-8")
        lines = fin.readlines()
        for line in lines:
            num_sentence += 1
            line = line.split("::")[1]
            _id = line.split("::")[0].split(" ")[0]
            morphemes = wakati.parse(line).split(" ")
            ave_length += (len(morphemes))
            SD += (len(morphemes) - 30) * (len(morphemes) - 30)
            if len(morphemes) > max_length:
                max_length = len(morphemes)
                max_sentence = line
            if len(morphemes) <= 60:
                less60 += 1

print("max_length is " + str(max_length))
print("max_sentence is " + max_sentence)
print("ave_length is " + str(ave_length/num_sentence))
print("SD is " + str(SD/num_sentence))
print("less than 60 is " + str(less60))
print("num of sentences is " + str(num_sentence))
