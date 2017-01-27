fin = open("/Users/tAku/Nextremer/data/wikidata_pNdd_sameTopicANDsameSection2/wikidata_extracted4annotation/2000ish.txt",encoding="utf-8")
fout = open("/Users/tAku/Nextremer/data/wikidata_pNdd_sameTopicANDsameSection2/wikidata_extracted4annotation/2000ish.csv","w",encoding="utf-8")
lines = fin.readlines()

fout.write("id,answer,topic,sentence\n")
for line in lines:
    line = line.split(" ")
    # print(line[0])
    # print(line[1])
    fout.write(line[0] + ",,")
    line = "".join(line[1:])
    sentence = line.split("::")
    fout.write(sentence[0] + ",")

    sentence = "".join(sentence[1:])
    fout.write(sentence + "\n")
