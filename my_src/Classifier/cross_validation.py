from sklearn.linear_model import LogisticRegression
from sklearn.decomposition import PCA
from sklearn.externals import joblib
from sklearn.model_selection import cross_val_score
import numpy as np
import sys, getopt
from random import shuffle
import random
import re
import time
from os import listdir
from os.path import isfile, join
from sklearn.metrics import roc_curve
import matplotlib.pyplot as plt
from math import sqrt
from scipy import interp

def cross_validation(dirin, files, k):

    for _file in files:
        if re.search(".tsv",_file) == None:
            files.remove(_file)

    # print(len(files))

    shuffle(files)
    num_files_each_group = int(len(files)/k)
    # print(num_files_each_group)
    plots = []

    for i in range(k):

        training_files = files[0:num_files_each_group*i] + files[num_files_each_group*(i+1):]
        test_files = files[num_files_each_group*i:num_files_each_group*(i+1)]

        data4training, labels4training = make_data_set(training_files, dirin)

        data4test, labels4test = make_data_set(test_files, dirin)

        clf = LogisticRegression()
        clf = clf.fit(data4training, labels4training)

        prediction = clf.predict(data4test)
        probability = clf.predict_proba(data4test)


        TP_total = 0
        FP_total = 0
        for j in range(len(data4test)):
            if probability[j][1] > 0 and labels4test[j] == 1:
                TP_total += 1
            elif probability[j][1] > 0 and labels4test[j] == -1:
                FP_total += 1
        # print(TP_total)
        # print(FP_total)
        plot = []
        for i in range(100):
            TP = 0
            FP = 0
            threshold = (100 - i)/100
            for j in range(len(data4test)):
                if probability[j][1] > threshold and labels4test[j] == 1:
                    TP += 1
                elif probability[j][1] > threshold and labels4test[j] == -1:
                    FP += 1
            plot.append([TP/TP_total,FP/FP_total])
            # print(TP)
            # print(FP)
        # exit()
        plots.append(plot)

    return plots



def make_data_set(files, dirin, with_h_id=True):
    data = []
    labels = []
    num_data = 0
    num_f = 0
    num_t = 0
    training_lines = []
    for _file in files:
        fin = open(dirin + _file, encoding="utf-8")

        lines = fin.readlines()
        # lines = lines[1:]


        for line in lines:
            if  line.split("\t")[3] == "f" or line.split("\t")[3] == "ff":
                num_f += 1
            if  line.split("\t")[3] == "t" or line.split("\t")[3] == "f" or line.split("\t")[3] == "ff":
                num_data += 1
                training_lines.append(line)

    shuffle(training_lines)

    # _id = training_lines[-1].split("\t")[0]
    # print(_id)
    # max_h_id = int(_id[len(_id)-6:len(_id)-4])

    for line in training_lines:
        line = line.split("\t")
        _id = line[0]
        if _id == "":
            continue
        food_id = int(_id[0:len(_id)-7])
        h_sort = int(_id[-7])
        # h_id = int(_id[len(_id)-6:len(_id)-4]) / max_h_id
        h_id = int(_id[len(_id)-6:len(_id)-4])
        p_id = int(_id[len(_id)-4:len(_id)-2])
        s_id = int(_id[len(_id)-2:len(_id)])

        # topic = remove_squareBracket.sub("",line[2])
        label = line[3]
        label = 1 if label == "t" else -1

        wordVec = []
        wordVec.append(h_sort)
        if with_h_id:
            wordVec.append(h_id)
        wordVec.append(p_id)
        wordVec.append(s_id)

        # num_f = 500
        if label == 1:
            if num_t < num_f:
                labels.append(label)
                data.append(wordVec)
                num_t += 1
        else:
            labels.append(label)
            data.append(wordVec)

    return data, labels

def main():
    dirin = "/Users/tAku/Nextremer/data/data4paper/"
    files = [f for f in listdir(dirin) if isfile(join(dirin, f))]

    MEAN = np.zeros((100))
    STDS_UPPER = np.zeros((100))
    STDS_LOWER = np.zeros((100))
    repeat = 50
    plt.figure(figsize=(5, 5))
    for k in range(repeat):
        print(str(k+1) + "th time")
        plots = cross_validation(dirin, files, 5)

        base_fpr = np.linspace(0, 1, 100)

        for plot in plots:
            plot = np.asarray(plot)
            plt.plot(plot[:,1], plot[:,0], 'b', alpha=0.05)

        stds_upper = []
        stds_lower = []
        means = []
        yinterps = []
        for plot in plots:
            plot = np.asarray(plot)
            yinterps.append(interp(base_fpr, plot[:,1], plot[:,0]))

        for i in range(100):
            std = 0
            mean = 0
            for yinterp in yinterps:
                # print(plot[i][1])
                mean += yinterp[i]
            # exit()
            mean /= len(plots)
            for yinterp in yinterps:
                std += (yinterp[i] - mean)**2
            std = sqrt(std/6)
            # stds.append(std)
            means.append(mean)
            stds_upper.append(mean+std)
            stds_lower.append(mean-std)
        MEAN = MEAN + np.asarray(means)
        STDS_UPPER = STDS_UPPER + np.asarray(stds_upper)
        STDS_LOWER = STDS_LOWER + np.asarray(stds_lower)

    MEAN /= repeat
    STDS_UPPER /= repeat
    STDS_LOWER /= repeat
    plt.fill_between(base_fpr, STDS_LOWER, STDS_UPPER, color='grey', alpha=0.3)
    plt.plot(base_fpr, MEAN, "b")
    # plt.plot([1,0],"go")
    plt.plot([0, 1], [0, 1],'r--')
    plt.xlim([-0.01, 1.01])
    plt.ylim([-0.01, 1.01])
    plt.ylabel('True Positive Rate')
    plt.xlabel('False Positive Rate')
    plt.axes().set_aspect('equal', 'datalim')
    plt.show()


if __name__ == "__main__":
   main()
