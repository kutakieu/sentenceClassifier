from os import listdir
from os.path import isfile, join
import re
import random
import MeCab
import math

# dirin = "/Users/tAku/Nextremer/data/wikidata_p_only_sameTopicANDsameSection2/wikidata_hierarchical/"
# files = [f for f in listdir(dirin) if isfile(join(dirin, f))]
fin = open("/Users/tAku/Desktop/wiki.txt",encoding="utf-8")
lines = fin.readlines()
fin.close()

word2tf_df = {}
wakati = MeCab.Tagger("-Owakati")
punctuation = [" ","、","。","　","\n",".",",","「","」","(",")"]
# BOF = 0
# EOF = 0
bagOfWords_eachDoc = []
num_of_doc = 1
for i in range(len(lines)):

	if lines[i] == "\n":
		if re.search(r'\[\[.+\]\]',lines[i+1]) != None and lines[i+2] == "\n":
			# EOF = i
			# BOF = i+1
			num_of_doc += 1
			# for w in bagOfWords_eachDoc:
			# 	print(w)
			bagOfWords_eachDoc = []
	else:
		morphemes = wakati.parse(lines[i]).split(" ")
		for morpheme in morphemes:
			# print(morpheme)
			if morpheme not in punctuation:
				try:	#dictionaryにすでにこの単語があるかをトライ
					word2tf_df[morpheme][0] += 1	#tf += 1
					if morpheme not in bagOfWords_eachDoc:
						word2tf_df[morpheme][1] += 1	#df += 1
						bagOfWords_eachDoc.append(morpheme)
				except:	#dictionaryにない場合
					word2tf_df[morpheme] = [1,1]
					bagOfWords_eachDoc.append(morpheme)


	if num_of_doc == 3:
		file_tf_idf = open("/Users/tAku/Desktop/tf_idf.txt", "w", encoding="utf-8")
		# file_tf_idf = open("/Users/tAku/Nextremer/data/wikidata_p_only_sameTopicANDsameSection2/tf_idf.txt", "w", encoding="utf-8")
		for key, value in word2tf_df.items():
			idf = math.log10(num_of_doc/value[1]) + 1
			file_tf_idf.write(key + "\t" + str(value[0]) + "\t" + str(value[1]) + "\t" + str(idf) + "\t" + str((math.log10(value[0])+1) * idf) +  "\n")
		exit()


            # file_food2id.write(key + " " + str(value) + "\n")
		# if i == 10:
		# 	for key, value in word2tf_df.items():
		# 		print(key + " tf:" + str(value[0]) + " idf:" + str(value[1]))
		# 	exit()
file_tf_idf = open("/Users/tAku/Nextremer/data/wikidata_p_only_sameTopicANDsameSection2/tf_idf.txt", "w", encoding="utf-8")
for key, value in word2tf_df.items():
	idf = math.log10(num_of_doc/value[1]) + 1
	file_tf_idf.write(key + "\t" + str(value[0]) + "\t" + str(value[1]) + "\t" + str(idf) + "\t" + str((math.log10(value[0])+1) * idf) +  "\n")
