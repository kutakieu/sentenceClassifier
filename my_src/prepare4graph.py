from os import listdir
from os.path import isfile, join
import re

dirin = "/Users/tAku/Nextremer/data/data4paper/"

files = [f for f in listdir(dirin) if isfile(join(dirin, f))]

fouts = []
fout1 = open(dirin + "abst-firstSentence.txt", "w")
fout2 = open(dirin + "abst-allSentence.txt", "w")
fout3 = open(dirin + "h2-firstSentence.txt", "w")
fout4 = open(dirin + "h2-p-firstSentence.txt", "w")
fout5 = open(dirin + "h2-allSentence.txt", "w")
fout6 = open(dirin + "h3-firstSentence.txt", "w")
fout7 = open(dirin + "h3-p-firstSentence.txt", "w")
fout8 = open(dirin + "h3-allSentence.txt", "w")

fouts.append(fout1)
fouts.append(fout2)
fouts.append(fout3)
fouts.append(fout4)
fouts.append(fout5)
fouts.append(fout6)
fouts.append(fout7)
fouts.append(fout8)
num_h3 = 0
num_h2 = 0
num_h1 = 0
num_total = 0

num_sentences = [0,0,0,0,0,0,0,0]
num_true = [0,0,0,0,0,0,0,0]

for _file in files:
    if re.search(".tsv",_file) == None:
        continue

    fin = open(dirin + _file, "r")

    lines = fin.readlines()

    for line in lines[1:]:
        original_line = line
        line = line.split("\t")
        _id = line[0]
        label = line[3]
        if _id == "" or label == "":
            continue
        # food_id = int(_id[0:len(_id)-7])
        print(_id)
        h_sort = int(_id[-7])
        h_id = int(_id[len(_id)-6:len(_id)-4])
        p_id = int(_id[len(_id)-4:len(_id)-2])
        s_id = int(_id[len(_id)-2:len(_id)])


        if h_sort == 1 and h_id == 0 and s_id == 0:
            i = 0
            for fout in fouts:
                fout.write(original_line)
                num_sentences[i] += 1
                if label == "t":
                    num_true[i] += 1
                i += 1

        elif h_sort == 1 and h_id == 0 :
            i = 1
            for fout in fouts[1:]:
                fout.write(original_line)
                num_sentences[i] += 1
                if label == "t":
                    num_true[i] += 1
                i += 1

        elif h_sort == 2 and p_id == 0 and s_id == 0:
            i = 2
            for fout in fouts[2:]:
                fout.write(original_line)
                num_sentences[i] += 1
                if label == "t":
                    num_true[i] += 1
                i += 1

        elif h_sort == 2 and s_id == 0:
            i = 3
            for fout in fouts[3:]:
                fout.write(original_line)
                num_sentences[i] += 1
                if label == "t":
                    num_true[i] += 1
                i += 1

        elif h_sort == 2:
            i = 4
            for fout in fouts[4:]:
                fout.write(original_line)
                num_sentences[i] += 1
                if label == "t":
                    num_true[i] += 1
                i += 1

        elif h_sort == 3 and p_id == 0 and s_id == 0:
            i = 5
            for fout in fouts[5:]:
                fout.write(original_line)
                num_sentences[i] += 1
                if label == "t":
                    num_true[i] += 1
                i += 1

        elif h_sort == 3 and s_id == 0:
            i = 6
            for fout in fouts[6:]:
                fout.write(original_line)
                num_sentences[i] += 1
                if label == "t":
                    num_true[i] += 1
                i += 1

        elif h_sort == 3:
            i = 7
            for fout in fouts[7:]:
                fout.write(original_line)
                num_sentences[i] += 1
                if label == "t":
                    num_true[i] += 1
                i += 1

        if h_sort == 3:
            num_h3 += 1
        if h_sort == 2:
            num_h2 += 1
        if h_sort == 1:
            num_h1 += 1

for fout in fouts:
    fout.close()
print(num_h1)
print(num_h2)
print(num_h3)
print(num_h1 + num_h2 + num_h3)

print("\n\n")
for i in range(8):
    print("total=" + str(num_sentences[i]) + "\t true_poistive=" + str(num_true[i]) + "\t true_negative=" + str(num_sentences[i]-num_true[i]))
    print("total=" + str(num_sentences[7]) + "\t true_poistive=" + str(num_true[i]/num_true[7]) + "\t true_negative=" + str((num_sentences[i]-num_true[i])/(num_sentences[7]-num_true[7])))
