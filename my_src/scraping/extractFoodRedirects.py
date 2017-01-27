


dirin = "/Users/tAku/Nextremer/data/"

synonyms = []
file_synonym = open(dirin + "wikipedia_synonym.txt", encoding="utf-8")
lines = file_synonym.readlines()
for line in lines:
    line = line[:-1]
    words = line.split(",")
    synonyms.append(words)

tempFoods = []
fout = open(dirin + "foodList_synonyms.txt", "w", encoding="utf-8")
# file_notFound = open(dirin + "foodList_notFound.txt", "w", encoding="utf-8")

for foods in ("food.txt", "food2.txt"):
    fin = open(dirin + foods, encoding="utf-8")
    lines = fin.readlines()
    for line in lines:
        flag = False
        line = line[:-1]
        if " " in line and "(" in line and ")" in line:
            line = line.split(" ")[:-1][0]

        print(line)
        #新しい入力文がtempFoodsのsynonymリストにすでに入っているかを検索（重複を避けるため)
        for synonym in tempFoods:
            if line in synonym:
                flag = True
                break
        #リストにまだなかった場合はoutput fileに書き込み、同時にtempFoodsに追加する
        if flag == False:
            for synonym in synonyms:
                if line in synonym:
                    fout.write(line)
                    for word in synonym:
                        fout.write("," + word)
                    fout.write("\n")

                    tempFoods.append(synonym)
                    break
