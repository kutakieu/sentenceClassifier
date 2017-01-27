import csv   #csvモジュールをインポートする

datadir = "/Users/tAku/Nextremer/data/"

fin = open(datadir + "teacher_data2_utf8.csv", 'r', encoding="utf-8")
fout = open(datadir + "teacher_data2.csv", "w", encoding = "cp932")
# fout2 = open(datadir + "teacher_data2_utf8.csv", "w", encoding = "utf-8")
# fout2 = open(datadir + "teacher_data_utf8.csv", "w", encoding="utf-8")

writer = csv.writer(fout)
# writer2 = csv.writer(fout2)


# writer2 = csv.writer(fout2)
dataReader = csv.reader(fin)
count = 0
for row in dataReader:
    count += 1
    writer.writerow(row)

print(count)

#
# dataReader = csv.reader(fin)
#
# count = 0
# new_row = []
# for row in dataReader:
#     #print "line Num = %02d" % count
#     if row[0] != "":
#         new_row = []
#         new_row.append("knowledge")
#         new_row.append("food#" + row[0])
#         new_row.append(row[1])
#         # writer.writerow(new_row)
#         writer2.writerow(new_row)
#         count += 1
#
# print(count)
