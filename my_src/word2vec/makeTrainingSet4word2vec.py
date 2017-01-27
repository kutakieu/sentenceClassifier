import re
from os import listdir
from os.path import isfile, join
mypath = "/Users/tAku/Nextremer/data/wikidata/"
mypath_out = "/Users/tAku/Nextremer/data/"

# onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]

fout = open(mypath_out + "word2vec_training.txt", "w", encoding = "utf-8")

for filename in ["/Users/tAku/Nextremer/data/foodList.txt"]:
     if re.search(".txt",filename) != None:
         print(filename)
         fin = open(mypath + filename, encoding = "utf-8")
         lines = fin.readlines()
         fin.close()
         for line in lines:
             line = line.replace('\n','')
             fout.write(line)
