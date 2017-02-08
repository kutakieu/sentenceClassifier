import urllib.request
import urllib.parse
from bs4 import BeautifulSoup
import time
import ssl
import MeCab
from os import listdir
from os.path import isfile, join
import re
dirin = "/Users/tAku/Nextremer/data/wikidata_p_only_sameTopicANDsameSection2/wikidata_raw/"
dirout = "/Users/tAku/Nextremer/data/wikidata_p_only_sameTopicANDsameSection2/wikidata_hierarchical/"
# filein = "茶.txt"
# fileout = "茶.txt"
# fin = open(dirin + filein, encoding="utf-8")
# fout = open(dirout + fileout, "w", encoding="utf-8")

head = {"h1":1, "h2":2, "h3":3, "h4":4, "h5":5, "dt":6}

template = ["脚注","出典","参考文献","関連項目","外部リンク","案内メニュー","個人用ツール","名前空間","変種","表示","その他","検索","案内","ヘルプ","印刷/書き出し","他のプロジェクト","ツール","他言語版"]

id2sentence = {}
food2id = {}
# current_H = 0
# name_H = ""
H_index = -1
p_index = 0
s_index = 0
H_sort = 0
text = ""
headline = ""
food_id = 1
listAll = []
listTmp = []

# path2lists = "/Users/tAku/Nextremer/mecab_dictionary/foodLists_copy/"
files = [f for f in listdir(dirin) if isfile(join(dirin, f))]

for _file in files:
    if re.search(".txt",_file) != None:
        # _file = "デラウェア.txt"
        print(_file)
        id2sentence = {}
        fin = open(dirin + _file , encoding = "utf-8")
        lines = fin.readlines()
        fin.close()
        # page_topic = lines[0].split("::")[0]
        # original_topic = lines[0].split("::")[1]
        H_index = -1
        headline = ""
        for line in lines[1:]:
            line = line[:-1]
            line.replace('\n','')
            if "!headline!" in line:
                # line = line[:-1]
                words = line.split("##")
                headline = words[1]
                if headline in template:
                    break
                try:
                    H_sort = head[words[-1]]
                except Exception as e:
                    print(line)
                    continue
                H_index += 1
                p_index = 0

            else:
                sentences = line.split('。')
                s_index = 0
                for sentence in sentences:
                    if sentence != "":

                        H_index_ = (str(0) + str(H_index)) if H_index < 10 else str(H_index)
                        p_index_ = (str(0) + str(p_index)) if p_index < 10 else str(p_index)
                        s_index_ = (str(0) + str(s_index)) if s_index < 10 else str(s_index)
                        _id = str(food_id) + str(H_sort) + H_index_ + p_index_ + s_index_
                        # print(sentence)
                        # print(_id)
                        # print(H_sort)
                        # print(H_index)
                        # print(p_index)
                        # print(s_index)
                        id2sentence[int(_id)] = headline + "::" + sentence + "。"
                        s_index += 1
                p_index += 1
            # print(line)
        # exit()
        fout = open(dirout + _file, "w", encoding="utf-8")
        fout.write(lines[0])
        for key, value in sorted(id2sentence.items()):
            fout.write(str(key) + " " + value + "\n")

        food2id[_file.split('.')[0]] = food_id
        food_id += 1

file_food2id = open("/Users/tAku/Nextremer/data/wikidata_p_only_sameTopicANDsameSection2/food2id.txt", "w", encoding="utf-8")
for key, value in food2id.items():
    file_food2id.write(key + " " + str(value) + "\n")

# print(id2sentence)
