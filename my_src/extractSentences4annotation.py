import urllib.request
import urllib.parse
from bs4 import BeautifulSoup
import time
import ssl
import MeCab
from os import listdir
from os.path import isfile, join
import re
import random
import MeCab
from numpy.random import normal

wakati = MeCab.Tagger("-Owakati")
random.seed(1)

dirin = "/Users/tAku/Nextremer/data/wikidata_p_only_sameTopicANDsameSection/wikidata_hierarchical_modified/"
dirout = "/Users/tAku/Nextremer/data/wikidata_p_only_sameTopicANDsameSection/wikidata_extracted4annotation/"

files = [f for f in listdir(dirin) if isfile(join(dirin, f))]
fout1 = open(dirout + "10000ish.csv", "w", encoding="utf-8")
fout1.write("id,topic,sentence\n")
fout2 = open(dirout + "2000ish.csv", "w", encoding="utf-8")
fout2.write("id,topic,sentence\n")
# fout3 = open(dirout + "500ish.txt")
for _file in files:
    if re.search(".txt",_file) != None:
        print(_file)
        fin = open(dirin + _file , encoding = "utf-8")
        lines = fin.readlines()
        fin.close()
        candidates = []
        for line in lines:
            morphemes = wakati.parse(line).split(" ")
            for i in range(5):
                if morphemes[i] == "って":
                    candidates.append(line)
                    break

        #for 2000ish --- extract 1 sentences per file/topic

        if len(candidates) < 1:
            continue
        else:
            # print(len(candidates))
            i_candidate = -1
            while i_candidate < 0 and i_candidate >= len(candidates):
                i_candidate = int(normal(len(candidates)/2,len(candidates)/4))
            sentence = candidates[i_candidate]
            sentence = sentence.split(" ")
            _id = sentence[0]
            sentence = "".join(sentence[1:])
            sentence = sentence.split("::")
            topic = sentence[0]
            sentence = sentence[1]
            fout2.write(_id + "," + topic + "," + sentence + "\n")

        #for 10000ish --- extract 5 sentences per file/topic
        if len(candidates) <= 5:
            for candidate in candidates:
                fout1.write(candidate)
        else:
            index = []
            while len(index)<5:
                i_candidate = int(normal(len(candidates)/2,len(candidates)/4))
                if i_candidate >= 0 and i_candidate < len(candidates):
                    if i_candidate not in index:
                        index.append(i_candidate)
                # i_candidate = random.randint(0,len(candidates)-1)
                # if i_candidate not in index:
                #     index.append(i_candidate)

            for i in index:
                sentence = candidates[i]
                sentence = sentence.split(" ")
                _id = sentence[0]
                sentence = "".join(sentence[1:])
                sentence = sentence.split("::")
                topic = sentence[0]
                sentence = sentence[1]
                fout1.write(_id + "," + topic + "," + sentence + "\n")

fout1.close()
fout2.close()
