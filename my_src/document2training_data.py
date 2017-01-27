import MeCab

m = MeCab.Tagger("-Owakati")
fileName = "hanashi_kotoba_dataset.txt"
dirpath = "/Users/tAku/Nextremer/data/"

fin = open(dirpath + fileName,encoding="utf-8")
fout = open(dirpath + "out_" + fileName, 'w', encoding="utf-8")
punctuation = ["、","。","(",")","[","]","「","」","・"]
lines = fin.readlines()

for line in lines:
    if line is not None:
        #print(line + "!!!!!!!!!!!!")
        morphemes = m.parse(line).split(' ')
        print(morphemes)
    # morphemes = m.parse(line)

        for morpheme in morphemes:
            fout.write(morpheme + " ")
            print(morpheme + " ")

            # if morpheme in punctuation:
            #     continue;
            # else:
            #     fout.write(morpheme + " ")
            #     print(morpheme + " ")

fout.close()
