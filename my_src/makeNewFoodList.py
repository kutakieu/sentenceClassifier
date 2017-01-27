fin_not = open("/Users/tAku/Nextremer/data/notFoundList.txt", encoding="utf-8")
notFounds = fin_not.readlines()
notFoundList = []
for att in notFounds:
    foodName = "".join(att.split(" ")[0:-3])
    notFoundList.append(foodName)
print(len(notFoundList))
print(notFoundList[0])
# print(notFounds[0][-1])
# print("パスタパスタ" not in notFounds)
notFood = ["Qoo",
"アイス",
"アミューズ",
"ウインナー",
"オマール",
"カール",
"コロナ",
"サイドカー",
"シャンパーニュ",
"シンハー",
"ストロベリーパフェ",
"スプレッド",
"ダージリン",
"デラウェア",
"バーボン",
"パニーニ",
"フランクフルト",
"ブルックス・イングランド",
"ホルモン",
"ホワイト",
"マスカット",
"ムーンライト",
"モンブラン",
"肉",
"緑川"]

fout = open("/Users/tAku/Nextremer/data/foodList.txt", "w", encoding="utf-8")
for _file in ["/Users/tAku/Nextremer/data/food.txt", "/Users/tAku/Nextremer/data/food2.txt"]:

    fin = open(_file, encoding="utf-8")
    lines = fin.readlines()

    for line in lines:
        if line[:-1] not in notFoundList and line[:-1] not in notFood:
            fout.write(line)
