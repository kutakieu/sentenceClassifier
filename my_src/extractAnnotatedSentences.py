fin_annotated = open("/Users/tAku/Nextremer/data/wikidata_p_only_sameTopicANDsameSection2/0131_annotated.tsv", encoding="utf-8")

fin_not_annotated = open("/Users/tAku/Nextremer/data/wikidata_p_only_sameTopicANDsameSection2/sentences_s00_H1orH2_Abst_meishi4annotation_tab.csv", encoding="utf-8")

fout = open("/Users/tAku/Nextremer/data/wikidata_p_only_sameTopicANDsameSection2/0203_annotation.csv", "w", encoding="utf-8")


annotated_list = []

"""construct annotated_list """

lines = fin_annotated.readlines()

for line in lines[1:]:
    line = line.split("\t")
    if line[0] == "":
        continue
    else:
        annotated_list.append(line[0])
        _id = line[0]
        headline = line[1]
        topic = line[2]
        label = line[3]
        text = "".join(line[4:])
        fout.write(_id + "\t" + headline + "\t" + topic + "\t" + label + "\t" + text)

lines = fin_not_annotated.readlines()

for line in lines:
    line = line.split("\t")
    if line[0] == "" or len(line) < 4:
        continue
    else:
        _id = line[0]
        print(_id)
        if _id in annotated_list:
            continue

        headline = line[1]
        topic = line[2]
        text = "".join(line[3:])
        fout.write(_id + "\t" + headline + "\t" + topic + "\t" + "\t" + text)
