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
dirin = "/Users/tAku/Nextremer/data/wikidata_p_only_sameTopicANDsameSection2/wikidata_hierarchical/"

fout = open("/Users/tAku/Nextremer/data/wikidata_p_only_sameTopicANDsameSection2/wikidata_hierarchical/sentence_analyze.txt", "w", encoding="utf-8")
files = [f for f in listdir(dirin) if isfile(join(dirin, f))]
num_files = len(files)
max_length = 0
max_sentence = ""
ave_length = 0
num_sentence = 0
SD = 0
less60 = 0
num = 0
for _file in files:
    if re.search(".txt",_file) != None:
        num_files -= 1
        # print(_file + "  残り：" + str(num_files))
        fin = open(dirin + _file, encoding="utf-8")
        lines = fin.readlines()
        if len(lines) > 1:
            line = lines[0][:-1]
            line = line.split("::")
            if line[0] == line[1]:
                continue
            else:
                num += 1
            for line in lines:
                num_sentence += 1
                # line = line.split("::")[1]
                # _id = line.split("::")[0].split(" ")[0]
                # morphemes = wakati.parse(line).split(" ")
                # ave_length += (len(morphemes))
                # SD += (len(morphemes) - 30) * (len(morphemes) - 30)
                # if len(morphemes) > max_length:
                #     max_length = len(morphemes)
                #     max_sentence = line
                # if len(morphemes) <= 60:
                #     less60 += 1
                fout.write(line)
print("num sentences = " + str(num_sentence))
print("num file = " + str(num))
#
# print("max_length is " + str(max_length))
# print("max_sentence is " + max_sentence)
# print("ave_length is " + str(ave_length/num_sentence))
# print("SD is " + str(SD/num_sentence))
# print("less than 60 is " + str(less60))
# print("num of sentences is " + str(num_sentence))
