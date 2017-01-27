import MeCab

m = MeCab.Tagger("-Owakati")

dirin = "/Users/tAku/Nextremer/data/wikidata_pNdd_sameTopicANDsameSection2/"
fin = open(dirin + "2000_annotated.csv",encoding="utf-8")

dirout = "/Users/tAku/Nextremer/data/wikidata_pNdd_sameTopicANDsameSection2/"
fout = open(dirout + "2000_annotated_wakati.csv", "w", encoding="utf-8")

lines = fin.readlines()
true = 0
false = 0
remain = 0
for line in lines[1:]:
    # print(line)
    attributes = line.split(",")
    # for attribute in attributes:
    #     print(attribute)
    if attributes[0] == "":
        continue
    elif attributes[1] == "":
        remain+=1
        continue

    sentence_wakati = m.parse(attributes[3])
    fout.write(attributes[0] + "," + attributes[1] + "," + sentence_wakati)

    if attributes[1] == "t":
        true+=1
    elif attributes[1] == "f":
        false+=1

    # exit()
print("true : " + str(true))
print("false : " + str(false))
print("remain : " + str(remain))
