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
import operator

dirin = "/Users/tAku/Nextremer/data/wikidata_p_only_sameTopicANDsameSection/wikidata_raw/"
fout_sort = open("/Users/tAku/Nextremer/data/wikidata_p_only_sameTopicANDsameSection/headlines_sort.txt","w",encoding="utf-8")

fout_all = open("/Users/tAku/Nextremer/data/wikidata_p_only_sameTopicANDsameSection/headlines_all.txt","w",encoding="utf-8")

template = ["脚注","出典","参考文献","関連項目","外部リンク","案内メニュー","個人用ツール","名前空間","変種","表示","その他","検索","案内","ヘルプ","印刷/書き出し","他のプロジェクト","ツール","他言語版"]

head = {"h1":1, "h2":2, "h3":3, "h4":4, "h5":5, "dt":6}
files = [f for f in listdir(dirin) if isfile(join(dirin, f))]

headline2frequency = {}
# headline2frequency["概要"] = 0
for _file in files:
    if re.search(".txt",_file) != None:
        fin = open(dirin + _file, encoding="utf-8")
        lines = fin.readlines()
        fin.close()
        topic = lines[0].split("::")[1]
        topic = topic[:-1]
        for i in range(1,len(lines)):
            line = lines[i][:-1]
            if i + 1 != len(lines):
                next_line = lines[i+1][:-1]
            else:
                continue

            if "!headline!" in line:
                line = line.split("##")
                if len(line) < 3:
                    continue
                headline = line[1]
                head_sort = line[2]
                if headline in template or "!headline!" in next_line or headline in ["概要","歴史"]:
                    continue
                if headline != topic:
                    fout_all.write(topic + "," + headline + "," + str(head[head_sort]) + "\n")
                    try:
                        headline2frequency[headline] += 1
                    except:
                        headline2frequency[headline] = 1


sorted_dic = sorted(headline2frequency.items(), key=operator.itemgetter(1))
for i in range(len(sorted_dic)):
    row = sorted_dic[len(sorted_dic)-i-1]
    fout_sort.write(row[0] + " " + str(row[1]) + "\n")
# for row in sorted_dic:
#     fout.write(row[0] + " " + str(row[1]) + "\n")
# for key, value in sorted_dic.items():
#     fout.write(key + " " + str(value) + "\n")
