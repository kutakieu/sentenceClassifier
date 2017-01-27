file_food2id = open("/Users/tAku/Nextremer/data/wikidata_pNdd_sameTopicANDsameSection2/food2id.txt", encoding="utf-8")

lines = file_food2id.readlines()

id2food = {}
for line in lines:
    line = line[:-1]
    line = line.split(" ")
    food = "".join(line[:-1])
    _id = line[-1]
    id2food[_id] = food

file_id2food = open("/Users/tAku/Nextremer/data/wikidata_pNdd_sameTopicANDsameSection2/id2food.txt", "w", encoding="utf-8")

for key, value in id2food.items():
    file_id2food.write(key + " " + str(value) + "\n")
