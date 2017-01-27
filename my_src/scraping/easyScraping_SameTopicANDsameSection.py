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
#このスクレイピングでは基本的に <p>と <dd> の両方をとる。
p_only = True

# ----main routine----


start = time.time()
remove_squareBracket = re.compile(r'\[.*?\]|（.*?）| \(.*?\)')
# remove_brackets = re.compile(r"(（.*?）| \(.*?\))")
# sub = re.sub(r"(（.*?。*.*?）)", "",sub)

# 読み込むファイル記述してください(空白行終わりで)
# path2lists = "/Users/tAku/Nextremer/mecab_dictionary/foodLists/"
# files = [f for f in listdir(path2lists) if isfile(join(path2lists, f))]

head = {"h1":1, "h2":2, "h3":3, "h4":4, "h5":5, "dt":6}

i = 0
count = 1
opener = urllib.request.build_opener()

for _file in ["/Users/tAku/Nextremer/data/foodList.txt"]:
    if re.search(".txt",_file) != None:
        fin = open(_file , encoding = "utf-8")
        lines = fin.readlines()
        numOfWords = len(lines)
        fin.close()
        count = 0
        for line in lines:
            flag = False
            line = line[:-1]    # 最後の文字(改行)を取る
            # line = "広島風お好み焼き"
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
                fou = open('/Users/tAku/Nextremer/data/wikidata_p_only_sameTopicANDsameSection/wikidata_raw/' + line + '.txt','w', encoding = 'utf-8')
                fnot = open("/Users/tAku/Nextremer/data/wikidata_p_only_sameTopicANDsameSection/notFoundList.txt" , "w" , encoding = "utf-8")
                html = opener.open(u).read()
                soup = BeautifulSoup(html, "lxml")
                text = soup.findAll(("p","h1","h2","h3","h4")) # 指定タグ内のテキスト全てをリスト格納
            else:
                fou = open('/Users/tAku/Nextremer/data/wikidata_pNdd_sameTopicANDsameSection/wikidata_raw/' + line + '.txt','w', encoding = 'utf-8')
                fnot = open("/Users/tAku/Nextremer/data/wikidata_pNdd_sameTopicANDsameSection/notFoundList.txt" , "w" , encoding = "utf-8")
                html = opener.open(u).read()
                soup = BeautifulSoup(html, "lxml")
                text = soup.findAll(("p","dd","dt","h1","h2","h3","h4")) # 指定タグ内のテキスト全てをリスト格納

            count += 1
            # print(text)
            if line != (soup.title.string.split(" ")[0]): # ページのタイトルと検索語が一致するか確認
                 print(soup.title.string.split(" ")[0] + "|" + line + ": 抽出ページと検索語が異なります")
                #  fnot.write(soup.title.string.split(" ")[0] + "|" + line + ": 抽出ページと検索語が異なります\n")
                 flag = True

            # fou.write(soup.title.string.split(" ")[0] + "|" + line + "\n")
            # text = remove_squareBracket("", text)
            fou.write(soup.title.string.split(" ")[0] + "::" + line + "\n")

            #トピック名とページ名が一致していない場合 True
            if flag:
                flag2write = False
                pre_H = 1
                topic_H = 0
                for part in text:
                    if part.name in "h1":
                        fou.write("!headline!##" + remove_squareBracket.sub("", part.get_text()) + "##" + part.name + "\n")

                    elif part.name in ["h2","h3","h4","dt"]:

                        headline = part.get_text()
                        #現在のヘッダーが、トピック名が含まれているヘッダーのサブクラスの場合、ヘッダーにトピック名が入っていなくてもファイルに書き込む
                        if flag2write and head[part.name] > topic_H and topic_H != 0:
                            print("here")
                            flag2write = True
                            fou.write("!headline!##" + remove_squareBracket.sub("", part.get_text()) + "##" + part.name + "\n")
                            continue
                        else:
                            False

                        if line in headline:
                            flag2write = True
                            topic_H = head[part.name]
                            fou.write("!headline!##" + remove_squareBracket.sub("", part.get_text()) + "##" + part.name + "\n")
                        elif head[part.name] <= topic_H:
                            flag2write = False
                            topic_H = 0

                    elif part.name in ["p","dd"]:
                        sentences = part.get_text()
                        if "。" not in sentences:
                            continue
                        sentences = remove_squareBracket.sub("",sentences)
                        #ヘッダーにトピック名が入っていれば、直下のパラグラフはまるごとファイルに書き込む
                        if flag2write:
                            fou.write(sentences+"\n")
                        #各パラグラフを句点で分けて、トピック名が文章に入っていれば、ファイルに書き込む
                        else:
                            sentences = sentences.split("。")
                            flag2addNewLine = False
                            for sentence in sentences:
                                if line in sentence:
                                    flag2addNewLine = True
                                    fou.write(sentence+"。")
                            if flag2addNewLine:
                                fou.write("\n")

            else:
                for part in text:
                    if part.name in ["p", "dd"]:
                        lines = part.get_text()
                        if "複数の問題があります。" in lines or "。" not in lines:
                            continue
                        lines = remove_squareBracket.sub("",lines)
                        fou.write(lines+"\n")
                    else:
                        if part.get_text() != "目次":
                            headline = remove_squareBracket.sub("", part.get_text())
                            fou.write("!headline!##" + headline + "##" + part.name + "\n")
            fou.close()
            print(_file + " 残り : " + str(numOfWords-count) + " " + line)
            # exit()
fnot.close()

elapsed_time = time.time() - start
print("ElapsedTime:" + str(elapsed_time) + "[sec]")
