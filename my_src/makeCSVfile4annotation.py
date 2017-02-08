fin = open("/Users/tAku/Nextremer/data/wikidata_pNdd_sameTopicANDsameSection2/2000ish.csv",encoding="utf-8")
fout = open("/Users/tAku/Nextremer/data/wikidata_pNdd_sameTopicANDsameSection2/2000_final.csv","w",encoding="utf-8")
lines = fin.readlines()
from random import shuffle
import random
# random.seed(10)
#
# shuffle(lines)
# fout.write("id,answer,topic,sentence\n")
for line in lines[1:]:
    line = line.split(",")
    _id = line[0]
    line = "".join(line[1:])


    line = line.split("::")
    topic = line[0]
    headline = line[1]
    text = line[2]
    # text = text.replace(",","")
    fout.write(_id + "\t")
    fout.write(headline + "\t")
    fout.write(topic + "\t")
    fout.write(text + "\n")

    # fout.write(sentence + "\n")
