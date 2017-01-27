import random

dirin = "/Users/tAku/Nextremer/data/wikidata_pNdd_sameTopicANDsameSection/wikidata_hierarchical_modified/"

while True:
    text_name = input("type food name : ")

    try:
        fin = open(dirin + text_name + ".txt", encoding="utf-8")
    except:
        continue

    lines = fin.readlines()
    num_sentences = len(lines)
    # for line in lines:

    sentence = lines[random.randint(0,num_sentences-1)]
    print(sentence)
