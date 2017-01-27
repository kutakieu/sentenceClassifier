import urllib.request
import urllib.parse
from bs4 import BeautifulSoup
import time
import ssl
import MeCab
from os import listdir
from os.path import isfile, join
import re
# import regex
ssl._create_default_https_context = ssl._create_unverified_context

p_only = True

# ----main routine----


start = time.time()
remove_squareBracket = re.compile(r'\[.*?\]|（.*?）| \(.*?\)')
# remove_brackets = re.compile(r"(（.*?）| \(.*?\))")
# sub = re.sub(r"(（.*?。*.*?）)", "",sub)

# 読み込むファイル記述してください(空白行終わりで)
path2lists = "/Users/tAku/Nextremer/mecab_dictionary/foodLists/"
files = [f for f in listdir(path2lists) if isfile(join(path2lists, f))]

i = 0
count = 1
opener = urllib.request.build_opener()

for _file in files:
    if re.search(".txt",_file) != None:
        fin = open(path2lists + _file , encoding = "utf-8")
        lines = fin.readlines()
        numOfWords = len(lines)
        fin.close()
        count = 0
        for line in lines:
            line = line[:-1]    # 最後の文字(改行)を取る
            u = "https://ja.wikipedia.org/wiki/" + urllib.parse.quote(line.encode("utf-8"))
            #################test###################
            # line = "茶"
            # u = "https://ja.wikipedia.org/wiki/" + urllib.parse.quote(line.encode("utf-8"))
            ########################################
            try:
                opener.open(u)
            except Exception as e:
                # print (e)
                fnot.write(line + " is not found" + "\n") # Wikipediaに存在しなければnotFoundListへ
                # print(line + " is not found")
                count += 1
                continue

            # outputのパス記述してください
            if p_only:
                fou = open('/Users/tAku/Nextremer/data/wikidata_p_only_sameTopic/wikidata_raw/' + line + '.txt','w', encoding = 'utf-8')
                fnot = open("/Users/tAku/Nextremer/data/wikidata_p_only_sameTopic/notFoundList.txt" , "w" , encoding = "utf-8")
                html = opener.open(u).read()
                soup = BeautifulSoup(html, "lxml")
                text = soup.findAll(("p","h1","h2","h3","h4")) # 指定タグ内のテキスト全てをリスト格納
            else:
                fou = open('/Users/tAku/Nextremer/data/wikidata_pNdd_sameTopic/wikidata_raw/' + line + '.txt','w', encoding = 'utf-8')
                fnot = open("/Users/tAku/Nextremer/data/wikidata_pNdd_sameTopic/notFoundList.txt" , "w" , encoding = "utf-8")
                html = opener.open(u).read()
                soup = BeautifulSoup(html, "lxml")
                text = soup.findAll(("p","dd","h1","h2","h3","h4")) # 指定タグ内のテキスト全てをリスト格納

            count += 1
            # print(text)
            if line != (soup.title.string.split(" ")[0]): # ページのタイトルと検索語が一致するか確認
                 print(soup.title.string.split(" ")[0] + "|" + line + ": 抽出ページと検索語が異なります")
                 fnot.write(soup.title.string.split(" ")[0] + "|" + line + ": 抽出ページと検索語が異なります\n")
                 continue
            # fou.write(soup.title.string.split(" ")[0] + "|" + line + "\n")
            # text = remove_squareBracket("", text)
            fou.write(soup.title.string.split(" ")[0] + "::" + line + "\n")
            for part in text:
                if part.name in ["p", "dd"]:
                    lines = part.get_text()
                    lines = remove_squareBracket.sub("",lines)

                    fou.write(lines+"\n")
                else:
                    if part.get_text() != "目次":
                        headline = remove_squareBracket.sub("", part.get_text())
                        fou.write("!headline!##" + headline + "##" + part.name + "\n")
            fou.close()
            print(_file + " 残り : " + str(numOfWords-count) + " " + line)
fnot.close()

elapsed_time = time.time() - start
print("ElapsedTime:" + str(elapsed_time) + "[sec]")
