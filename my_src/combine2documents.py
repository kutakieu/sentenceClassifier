path_fileName1 = "/Users/tAku/Nextremer/data/word2vec_training.txt"
path_fileName2 = "/Users/tAku/Nextremer/data/hanashi_kotoba_dataset.txt"
path_out = "/Users/tAku/Nextremer/data/wiki_AND_hanashi_kotoba"

fin1 = open(path_fileName1, encoding="utf-8")
fin2 = open(path_fileName2, encoding="utf-8")

fout = open(path_out,  "w", encoding="utf-8")

lines1 = fin1.readlines()
lines2 = fin2.readlines()

for line in lines1:
    fout.write(line)
for line in lines2:
    fout.write(line)

fin1.close()
fin2.close()
fout.close()
