from os import listdir
from os.path import isfile, join
import re
import random
import MeCab
import math

dirin = "/Users/tAku/Nextremer/data/wikidata_p_only_sameTopicANDsameSection2/wikidata_hierarchical/"
files = [f for f in listdir(dirin) if isfile(join(dirin, f))]

word2tf_df = {}
wakati = MeCab.Tagger("-Owakati")
punctuation = [" ","、","。","　","\n",".",",","「","」","(",")"]

num_files = len(files)

for _file in files:
	if re.search(".txt",_file) != None:
		print(_file)
		bagOfWords_eachDoc = []
		fin = open(dirin + _file , encoding = "utf-8")
		lines = fin.readlines()
		fin.close()
		lines = lines[1:]
		for line in lines:
			line = line.split(" ")
			line = "".join(line[1:])
			line = line.split("::")
			sentence = line[1]
			# print(sentence)

			morphemes = wakati.parse(sentence).split(" ")
			for morpheme in morphemes:
				if morpheme not in punctuation:
					try:	#dictionaryにすでにこの単語があるかをトライ
						word2tf_df[morpheme][0] += 1
						if morpheme not in bagOfWords_eachDoc:
							word2tf_df[morpheme][1] += 1
							bagOfWords_eachDoc.append(morpheme)
					except:	#dictionaryにない場合
						word2tf_df[morpheme] = [1,1]
						bagOfWords_eachDoc.append(morpheme)


            # file_food2id.write(key + " " + str(value) + "\n")
		# if i == 10:
		# 	for key, value in word2tf_df.items():
		# 		print(key + " tf:" + str(value[0]) + " idf:" + str(value[1]))
		# 	exit()
file_tf_idf = open("/Users/tAku/Nextremer/data/wikidata_p_only_sameTopicANDsameSection2/tf_idf.txt", "w", encoding="utf-8")
for key, value in word2tf_df.items():
	idf = math.log10(num_files/value[1]) + 1
	file_tf_idf.write(key + "\t" + str(value[0]) + "\t" + str(value[1]) + "\t" + str(idf) + "\t" + str((math.log10(value[0])+1) * idf) +  "\n")
