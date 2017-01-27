# -*-coding:utf-8 -*-


# import module
from os import listdir
from os.path import isfile, join
import re
import random
import time
# from editdistance import eval

#---main routine---

start = time.time()

# PAtH(in,out共通)
dirin = "/Users/tAku/Nextremer/data/wikidata_p_only_sameTopicANDsameSection/wikidata_hierarchical/"
files = [f for f in listdir(dirin) if isfile(join(dirin, f))]

dirout = "/Users/tAku/Nextremer/data/wikidata_p_only_sameTopicANDsameSection/wikidata_hierarchical_filtered/"
# 読み込むファイルの数
fileNum = 10

# ランダムに取得したい文の数（）
sentenceNum = 25000

s = []

for _file in files:
	if re.search(".txt",_file) != None:
		# fileNum -= 1
		fin = open(dirin + _file , encoding = "utf-8")
		fout = open(dirout + _file, "w", encoding="utf-8")
		lines = fin.readlines()
		fout.write(lines[0])
		if len(lines) <= 1: #タイトルしか存在しないページ
			continue
		"""
		topic = text[0].split("|")[0]
		query = text[0].split("|")[1][:-1]
		#if topic != query: #ページ遷移してたらcotinue
		if eval(topic,query) > (min(len(topic),len(query))-1): #編集距離が遠い
			print(topic,"|",query)
		"""
		for line in lines[1:]:
			line = line.split(' ')
			_id = line[0]
			sentence = ''.join(line[1:])
			# フィルタリング項目（10文字以下、70文字以上、句点で終わる）
			if (sentence == "\n"):
				continue
			# elif (len(sentence) > 70) or (len(sentence) < 10)
			#	continue
			elif sentence[-2] != "。":
				continue
			elif sentence.find("現在") != -1:
				continue
			elif sentence.find("上述") != -1:
				continue
			elif sentence.find("後述") != -1:
				continue
			elif sentence.find("上記") != -1:
				continue
			elif sentence.find("下記") != -1:
				continue
			elif sentence.find("当時") != -1:
				continue
			elif sentence.find("以下の") != -1:
				continue
			elif sentence.find("次の") != -1:
				continue
			elif sentence.find("参照") != -1:
				continue
			elif sentence.find("その後") != -1:
				continue
			elif sentence.find("このほか") != -1:
				continue
			elif sentence.find("この他") != -1:
				continue
			elif sentence.find("こういった") != -1:
				continue
			elif sentence.find("このため") != -1:
				continue
			elif sentence.find("かつて") != -1:
				continue
			elif sentence.find("現代") != -1:
				continue
			elif sentence.find("このような") != -1:
				continue
			elif sentence.find("再度") != -1:
				continue
			# elif sentence.find("同様") != -1:
			# 	continue
			elif sentence.find("年には") != -1:
				continue
			elif sentence.find("本項") != -1:
				continue
			elif sentence.find("諸説") != -1:
				continue
			elif sentence.find("さらに") != -1:
				continue
			else:
				# sentence = re.sub(r'（.*?）|\(.*?\)|\[.*?\]|。|:|','',sentence.rstrip())
				fout.write(_id + " " + sentence)
		# if fileNum == 0:
		# 	break

# リストからランダムに文(sentenceNum個を選択し、ランダムな順序でリストに格納)
# print('sentenceNum :',len(s))
# randomSentence = random.sample(s, sentenceNum)
#
# with open(PATH + "Filtered-sentence/filterd-sentences2.txt", "w", encoding = "utf-8") as fou:
# 	for sub in randomSentence:
# 		fou.write(sub)

elapsed_time = time.time() - start
print("ElapsedTime:" + str(elapsed_time) + "[sec]")


def filtering(lines):
	result = []
	for line in lines:
		line = line.split(' ')
		_id = line[0]
		sentence = ''.join(line[1:])
		# フィルタリング項目（10文字以下、70文字以上、句点で終わる）
		if (sentence == "\n"):
			continue
		# elif (len(sentence) > 70) or (len(sentence) < 10) or sentence[-2] != "。":
		# 	continue
		elif sentence.find("現在") != -1:
			continue
		elif sentence.find("上述") != -1:
			continue
		elif sentence.find("後述") != -1:
			continue
		elif sentence.find("上記") != -1:
			continue
		elif sentence.find("下記") != -1:
			continue
		elif sentence.find("当時") != -1:
			continue
		elif sentence.find("以下の") != -1:
			continue
		elif sentence.find("次の") != -1:
			continue
		elif sentence.find("参照") != -1:
			continue
		elif sentence.find("その後") != -1:
			continue
		elif sentence.find("このほか") != -1:
			continue
		elif sentence.find("この他") != -1:
			continue
		elif sentence.find("こういった") != -1:
			continue
		elif sentence.find("このため") != -1:
			continue
		elif sentence.find("かつて") != -1:
			continue
		elif sentence.find("現代") != -1:
			continue
		elif sentence.find("このような") != -1:
			continue
		elif sentence.find("再度") != -1:
			continue
		elif sentence.find("同様") != -1:
			continue
		elif sentence.find("年には") != -1:
			continue
		elif sentence.find("本項") != -1:
			continue
		elif sentence.find("諸説") != -1:
			continue
		elif sentence.find("さらに") != -1:
			continue
		else:
			result.append(_id + " " + sentence)
