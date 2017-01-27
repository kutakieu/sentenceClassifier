'''
入力するテキストファイルは，各行が「話題語::対話分（加工前）」
random_sampling.pyにて，この形式へ変更してランダムに指定した数の文を抽出可能

コード中の番号は以下のドキュメント中の番号と対応
各番号がどのような動作をしているかはドキュメント参照
https://docs.google.com/a/nextremer.com/document/d/1WlXtgBQUtaXrqbAQyL-d-2A_u03LoSoO0qYNYJaQkW4/edit?usp=sharing
'''
import re
from mecabobj import mecabtxt
from os import listdir
from os.path import isfile, join
# from filter_randomSample import filtering

fileNum = 50

dirin = "/Users/tAku/Nextremer/data/wikidata_p_only_sameTopicANDsameSection/wikidata_hierarchical_filtered/"
files = [f for f in listdir(dirin) if isfile(join(dirin, f))]

dirout = "/Users/tAku/Nextremer/data/wikidata_p_only_sameTopicANDsameSection/wikidata_hierarchical_modified/"

dirout_other = "/Users/tAku/Nextremer/data/wikidata_p_only_sameTopicANDsameSection/wikidata_hierarchical_other/"
# outname = dirname + filename.split('.')[0] + "_speak.txt"
# othername = dirname + filename.split('.')[0] + "_oth.txt"
# fin = open(dirname + filename, encoding='utf-8')
# fou = open(outname,'w', encoding='utf-8')
# fouo = open(othername,'w', encoding='utf-8')
# ftopic = open(dirname + filename.split('.')[0] + "_title.txt", 'w', encoding='utf-8')

file_synonyms = open("/Users/tAku/Nextremer/data/foodList_synonyms.txt", encoding="utf-8")
lines = file_synonyms.readlines()
synonyms = []
for line in lines:
    line = line[:-1]
    words = line.split(",")[1:]
    # print(words)
    synonyms.append(words)

for _file in files:
    if re.search(".txt",_file) != None:

        # fileNum -= 1

        fin = open(dirin + _file , encoding = "utf-8")
        lines = fin.readlines()
        fin.close()
        fout = open(dirout + _file, "w", encoding="utf-8")
        fouto = open(dirout_other + _file, "w", encoding="utf-8")

        page_topic = lines[0].split("::")[0]
        original_topic = lines[0].split("::")[1][:-1]
        if " " in original_topic and "(" in original_topic and ")" in original_topic:
            original_topic = original_topic.split(" ")[:-1][0]
        # topic = _file.split('.')[0]

        print(original_topic)
        # if _file == "おでん.txt":
        #     print("おでん！！！！！！")

        #料理名（ファイル名）の同義語をfoodList_synonyms.txtから探し、対応するリストを返す
        synonym = []
        for _synonym in synonyms:
            if original_topic in _synonym:
                synonym = _synonym
                break
        print(synonym)
        count = 0
        for line in lines:
            flag = False
            headflag = False
            shift = 0

            #___ 1.2.1 begin ___
            # tmp = line.split("::")
            line = line.split(' ')
            _id = line[0]
            sentence = ''.join(line[1:])
            # print(str(type(topic)) + " " + topic)
            # print(str(type(sentence)) + " " + sentence)
            # t = unicode(topic)
            # s = unicode(sentence)
            # print(str(type(t)) + " " + topic)
            # print(str(type(s)) + " " + sentence)
            sentence = re.sub(r'（.*?）|\(.*?\)|\[.*?\]|。|:|','',sentence.rstrip())
            line = sentence
            if len(synonym) == 0:
                if re.search(original_topic, sentence) != None:
                # if topic in sentence:
                    headflag = True
            else:
                for word in synonym:
                    if re.search(word, sentence) != None:
                    # if word in sentence:
                        headflag = True
                        break

            # if topic in sentence:
            #     line = sentence
            # else:
            #     line = sentence
            #     headflag = True

            #___ 1.2.1 continue ___

            #___ eliminate some marks ___
            # line = re.sub(r'（.*?）|\(.*?\)|\[.*?\]|。|:|','',line.rstrip())

            r = mecabtxt(line)

            #___ eliminate text consists of under 3 morphemes ___
            if len(r) < 3:
                count += 1
                continue

            #___ 1.1.1,2 begin ___
            if r[0].category in "接続詞":
                r.pop(0)
                if r[0].category in "記号":
                    r.pop(0)
                flag = False
                count += 1
                continue
            #___ 1.1.1,2 end ___



        	#___ 1.1.3 begin ___（added by sugimoto）文頭の指示代名詞
            if r[0].detail1 in "代名詞":
                r.pop(0)
                while r[0].category == "助詞":
                    r.pop(0)
                if r[0].category in "記号":
                    	r.pop(0)
                flag = False
                count += 1
                continue
            #___ 1.1.3 end ___

            #___ 1.1.4 begin ___（added by sugimoto）文頭の副詞可能
            if r[0].detail1 in "副詞可能":
                r.pop(0)
                while r[0].category== "助詞":
                    r.pop(0)
                if r[0].category in "記号":
                    	r.pop(0)
                flag = False
                count += 1
                continue
            #___ 1.1.4 end ___

            #___ 1.1.5 begin ___（added by sugimoto）文頭の特定の連体詞
            if r[0].surface in ["この", "その", "あの", "どの"]:
                try:
                    r.pop(0)
                    while r[0].category == "名詞":
                        r.pop(0)
                    while r[0].category == "助詞":
                        r.pop(0)
                    if r[0].category in "記号":
                            r.pop(0)
                    flag = False
                    count += 1
                    continue
                except Exception as e:
                    continue
            #___ 1.1.5 end ___


            #___ 1.1.6 begin ___（added by sugimoto）助詞から始まる文
            while r[0].category == "助詞":
                r.pop(0)
                flag = False
                count += 1
                continue
            #___ 1.1.6 end ___


            #1.1.7数フィルター
            for word in r:
                if word.category =="数":
                    flag == False
                    count += 1
                    continue



            #___ 3.1.1 begin ___
            if r[-1].category in  ["副詞","形容詞","名詞"]:
                r.extend("ですよね")
                flag = True
            #___ 3.1.1 end ___

            #___ 3.1.2 begin ___
            if r[-1].category in "動詞" or\
                r[-2].category in "動詞" and r[-1].category in ["助詞","助動詞"] or\
                r[-2].surface in "だっ" and r[-1].surface in "た":
                r.extend("んですよ")
                flag = True
            #___ 3.1.2 end ___

            #___ 3.1.3 begin ___
            if r[-2].surface in "で" and r[-1].surface in "ある":
                r.pop()
                r.pop()
                r.extend("なんですよ")
                flag = True
            #___ 3.1.3 end ___

            #___ 3.1.4 begin ___
            if r[-3].surface in "で" and r[-2].surface in "あっ" and r[-1].surface in "た":
                r.pop()
                r.pop()
                r.pop()
                r.extend("だったんですよ")
                flag = True
            #___ 3.1.4 end ___

            #___ 3.1.5 begin ___
            if r[-2].category in "助動詞" and r[-1].surface in ["という"]:
                r.pop()
                r.extend("そうですよ")
                flag = True
            #___ 3.1.5 end ___
            #___ 3.1.6 begin ___
            if r[-2].category in "名詞" and r[-1].surface in ["という"]:
                r.extend("んですよ")
                flag = True
            #___ 3.1.6 end ___
            #___ 3.1.7 begin ___
            if r[-2].detail1 in "形容動詞語幹" and r[-1].surface in "だ":
                r.pop()
                r.extend("ですよね")
                flag = True
            #___ 3.1.7 end ___


            #___ 2 begin ___
            shift = 0
            for i in r.indexes('、'):
                i += shift
                #___ 2.1 begin ___#
                if r[i-1].category in "動詞":
                    #___ 2.1.1 begin ___#
                    if r[i-1].surface in "おり":
                        r.pop(i-1)
                        r.insert(i-1,"いて")#2
                        shift += 1
                        flag = True
                    #___ 2.1.1 end ___

                    #___ 2.1.2 begin ___
                    elif r[i-1].surface in "し":
                        r.pop(i-1)
                        r.insert(i-1,"して")#2
                        shift += 1
                        flag = True
                    #___ 2.1.2 end ___

                    #___ 2.1.3 begin ___
                    elif  r[i-1].conjugate("連用タ接続"):
                        if r[i-1].conjugtype in ["五段・ガ行","五段・ナ行","五段・バ行","五段・マ行"]:
                            r.insert(i,"で")
                            shift += 1
                    #___ 2.1.3 end ___

                    #___ 2.1.4 begin ___
                        else:
                            r.insert(i,"て")
                            shift += 1
                        flag = True
                    #___ 2.1.4 end ___
                #___ 2.1 end ___

                #___ 2.2.1 begin ___
                elif r[i-1].category in "形容詞" and r[i-1].conjugtype in "連用形":
                    r.insert(i,"て")
                    shift += 1
                    flag = True
                #___ 2.2.1 end ___

                #___ 2.3 begin ___
                elif r[i-1].surface in "が" and r[i-1].detail1 in "接続助詞":
                    # print("")
                    #___ 2.3.1begin ___
                    if r[i-2].category in "形容詞":
                        r.pop(i-1)
                        r.insert(i-1,"ですけど")#2
                        shift += 1
                        flag = True
                    #___ 2.3.1 end ___
                    #___ 2.3.2 begin ___
                    elif r[i-2].category in "動詞":
                        r[i-2].conjugate("連用形")
                        r.pop(i-1)
                        r.insert(i-1,"ますけど")#2
                        shift += 1
                        flag = True
                        # print(r.text())
                    #___ 2.3.2 end ___
                    #___ 2.3.3 begin ___
                    elif r[i-3].category in "動詞" and r[i-2].surface in "た":
                        r.pop(i-1)
                        r.insert(i-1,"んですけど")#3
                        shift += 2
                        flag = True
                    #___ 2.3.3 end ___
                    #___ 2.3.4 begin ___
                    elif r[i-3].surface in "で" and r[i-2].surface in "ある":
                        r.pop(i-1)
                        r.pop(i-2)
                        r.pop(i-3)
                        r.insert(i-3,"ですけど")#2
                        shift -= 1
                        flag = True
                    #___ 2.3.4 end ___
                    #___ 2.3.5 begin ___
                    elif r[i-2].surface in "だ":
                        r.pop(i-1)
                        r.pop(i-2)
                        r.insert(i-2,"ですけど")#2
                        flag = True
                    #___ 2.3.5 end ___
                    #___ 2.3.6 begin ___
                    elif r[i-3].surface in "だ" and r[i-2].surface in "った":
                        r.pop(i-2)
                        r.pop(i-3)
                        r.insert(i-3,"でした")#2
                        flag = True
                    #___ 2.3.6 end ___
                    #___ 2.3.7 begin ___
                    elif r[i-2].surface in "た":
                        r.pop(i-1)
                        r.pop(i-2)
                        r.insert(i-2,"たんですけど")#3
                        shift += 1
                        flag = True
                    #___ 2.3.7 end ___
                    #___ 2.3.8 begin ___
                    elif r[i-2].surface in "ない":
                        r.pop(i-1)
                        r.pop(i-2)
                        r.insert(i-2,"ないんですけど")#4
                        shift += 2
                        flag = True
                    #___ 2.3.8 end ___

                #___ 2.3 end ___
                #___ 2.4.1 begin ___
                elif r[i-2].surface in "で" and r[i-1].surface in "あり":
                    r.pop(i-1)
                    shift -= 1
                    flag = True
                #___ 2.4.1 end ___
            #___ 2 end ___

            #___ 4.1.1 begin___
            r = mecabtxt(r.text().replace("であった","だった"))
            #___ 4.1.1 end ___

            #___ 1.2.1 continue ___
            if not headflag:
                r.insert(0,original_topic + "って、")
            #___ 1.2.1 end ___

            if not flag :
                # print("Inflection-failed")
                fouto.write(_id + " " + r.text() + "\n")
            else:
                # print(r.text())
                fout.write(_id + " " + original_topic + "::" + r.text() + "\n")
                # ftopic.write(tmp[0] + "\n")
        print(_file + " Exclusion-sentence :",count)
        # if(fileNum == 0):
        #     break
        fout.close()
        fouto.close()
        # fouo.close()
        # ftopic.close()
