from sklearn.linear_model import LogisticRegression
from sklearn.decomposition import PCA
from sklearn.externals import joblib
from sklearn.model_selection import cross_val_score
import numpy as np
import sys, getopt
from random import shuffle
import random
from gensim.models import Word2Vec
import re
import time
import MeCab
from os import listdir
from os.path import isfile, join

wakati = MeCab.Tagger("-Owakati")
chasen = MeCab.Tagger("-Ochasen")

fin = open("/Users/tAku/Nextremer/data/wikidata_p_only_sameTopicANDsameSection2/0208_annotation_shuffled.tsv", encoding="utf-8")
data_path = "/Users/tAku/Nextremer/data/"

remove_squareBracket = re.compile(r'\[.*?\]|（.*?）| \(.*?\)')
original_sentences = []
with_h_id = True

def prepare():

    dirin = "/Users/tAku/Nextremer/data/data4paper/"

    files = [f for f in listdir(dirin) if isfile(join(dirin, f))]

    shuffle(files)
    files4training = files[:int(len(files) * 1)]
    files4test = files[int(len(files) * 1):]

    data4training = []
    labels4training = []
    num_f = 0
    num_t = 0
    for _file in files4training:
        if re.search(".tsv",_file) == None:
            continue

        fin = open(dirin + _file, encoding="utf-8")

        lines = fin.readlines()
        # lines = lines[1:]
        num_data = 0

        training_lines = []
        for line in lines:
            if  line.split("\t")[3] == "f" or line.split("\t")[3] == "ff":
                num_f += 1
            if  line.split("\t")[3] == "t" or line.split("\t")[3] == "f" or line.split("\t")[3] == "ff":
                num_data += 1
                training_lines.append(line)
        print("total : " + str(num_data) + " sentences")
        # shuffle(training_lines)

        # data = np.zeros((num_data,n_steps * n_input + 5))

        # random.seed(0)
        j = 0   #indenx of sentences (= 0~num_of_labeled_sentences)
        # print(id2food[10])

        _id = training_lines[-1].split("\t")[0]
        print(_id)
        max_h_id = int(_id[len(_id)-6:len(_id)-4])



        for line in training_lines:
            line = line.split("\t")
            _id = line[0]
            if _id == "":
                continue
            food_id = int(_id[0:len(_id)-7])
            h_sort = int(_id[-7])
            h_id = int(_id[len(_id)-6:len(_id)-4]) / max_h_id
            p_id = int(_id[len(_id)-4:len(_id)-2])
            s_id = int(_id[len(_id)-2:len(_id)])

            topic = remove_squareBracket.sub("",line[2])
            label = line[3]
            label = 1 if label == "t" else -1


            # text = "".join(line[4:])
            # original_sentences.append(text)

            wordVec = []
            wordVec.append(h_sort)
            if with_h_id:
                wordVec.append(h_id)
            wordVec.append(p_id)
            wordVec.append(s_id)

            # num_f = 500
            if label == 1:
                if num_t < num_f:
                    labels4training.append(label)
                    data4training.append(wordVec)
                    num_t += 1
                # else:
                #     labels4test.append(label)
                #     data4test.append(wordVec)
            else:
                labels4training.append(label)
                data4training.append(wordVec)

            j += 1
            # print(str(j) + " files complete vectorizing")
            if j % 100 == 0:
                print(str(j) + " files complete vectorizing")
    print("num data_f = " + str(num_f))
    print("num data = " + str(len(data4training)))
    #
    # data_f = []
    # labels_f = []
    # data_t = []
    # labels_t = []
    # for i in range(len(data4training)):
    #     if labels4training[i] == -1:
    #         data_f.append(data4training[i])
    #         labels_f.append(-1)
    #         # labels.append(labels4training[i])
    #     else:
    #         data_t.append(data4training[i])
    #         labels_t.append(1)
    # print("num data_f = " + str(len(data_f)))
    # print("num data_t = " + str(len(data_t)))


    # exit()


    data4test = []
    labels4test = []
    if with_h_id == True:
        for i in range(1,4):
            for j in range(10):
                for k in range(5):
                    for l in range(5):
                        param = []
                        param.append(i)
                        param.append(j/10)
                        param.append(k)
                        param.append(l)
                        data4test.append(param)
                        labels4test.append(0)
    else:
        for i in range(1,5):
            for k in range(5):
                for l in range(5):
                    param = []
                    param.append(i)
                    # param.append(j/10)
                    param.append(k)
                    param.append(l)
                    data4test.append(param)
                    labels4test.append(0)
    #
    # for _file in files4training:
    #     if re.search(".tsv",_file) == None:
    #         continue
    #
    #     fin = open(dirin + _file, encoding="utf-8")
    #
    #     lines = fin.readlines()
    #     # lines = lines[1:]
    #     num_data = 0
    #     training_lines = []
    #     for line in lines:
    #         if line.split("\t")[3] == "t" or line.split("\t")[3] == "f" or line.split("\t")[3] == "ff":
    #             num_data += 1
    #             training_lines.append(line)
    #     print("total : " + str(num_data) + " sentences")
    #     # shuffle(training_lines)
    #
    #     # data = np.zeros((num_data,n_steps * n_input + 5))
    #
    #     # random.seed(0)
    #     j = 0   #indenx of sentences (= 0~num_of_labeled_sentences)
    #     # print(id2food[10])
    #
    #     _id = training_lines[-1].split("\t")[0]
    #     max_h_id = int(_id[len(_id)-6:len(_id)-4])
    #
    #     for line in training_lines:
    #         line = line.split("\t")
    #         _id = line[0]
    #         if _id == "":
    #             continue
    #         food_id = int(_id[0:len(_id)-7])
    #         h_sort = int(_id[-7])
    #         h_id = int(_id[len(_id)-6:len(_id)-4]) / max_h_id
    #         p_id = int(_id[len(_id)-4:len(_id)-2])
    #         s_id = int(_id[len(_id)-2:len(_id)])
    #
    #         topic = remove_squareBracket.sub("",line[2])
    #         label = line[3]
    #         label = 1 if label == "t" else -1
    #         labels4test.append(label)
    #
    #         text = "".join(line[4:])
    #         original_sentences.append(text)
    #
    #         wordVec = []
    #
    #         wordVec.append(h_sort)
    #         wordVec.append(h_id)
    #         wordVec.append(p_id)
    #         wordVec.append(s_id)
    #
    #         data4test.append(wordVec)
    #         j += 1
    #         # print(str(j) + " files complete vectorizing")
    #         if j % 100 == 0:
    #             print(str(j) + " files complete vectorizing")

    print("complete vectorize data set")
    num_dataset = j
    print("dataset size = " + str(num_dataset))

    # return np.asarray(data), np.asarray(labels)
    return data4training, labels4training, data4test, labels4test, original_sentences


def main():

    X, y, X_test, y_test, test_sentences = prepare()

    total_true = 0
    total = 0
    for i in y:
        total += 1
        if i==1:
            total_true += 1
    print("trueの割合")
    print(total_true / total)


    start = time.time()

    try:
        clf = joblib.load('LogisticRegression.pkl_')
        print("load the pickle file...")
    except:
        print("start training the model...")

        clf = LogisticRegression()

        clf = clf.fit(X, y)
        scores = cross_val_score(clf, X, y)

        print(scores.mean())

        joblib.dump(clf, 'LogisticRegression.pkl')

    prediction = clf.predict(X_test)
    probability = clf.predict_proba(X_test)
    correct = 0
    if with_h_id:
        fout = open("/Users/tAku/Nextremer/data/data4paper/data.txt", "w", encoding="utf-8")
    else:
        fout = open("/Users/tAku/Nextremer/data/data4paper/data_without_h_index.txt", "w", encoding="utf-8")
    if len(prediction) == len(y_test):
        for i in range(len(prediction)):
            if y_test[i] == prediction[i]:
                print("True  " + "y : " + str(y_test[i]) + " p : " + str(prediction[i]))

                print(probability[i])
                correct += 1
            else:
                print("False  " + "y : " + str(y_test[i]) + " p : " + str(prediction[i]))

                if with_h_id:
                    fout.write(str(X_test[i][0]) + "\t" + str(X_test[i][1]) + "\t" + str(X_test[i][2]) + "\t" + str(X_test[i][3]) + "\t" + str(probability[i][1]) + "\n")
                else:
                    fout.write(str(X_test[i][0]) + "\t" + str(X_test[i][1]) + "\t" + str(X_test[i][2]) + "\t" + str(probability[i][1]) + "\n")

                print(probability[i])

        print("num correct = " + str(correct) + " out of " + str(len(y_test)) + " = " + str(correct/len(y_test)))
    else:
        print(len(prediction))
        print(len(y_test))

    # probability = clf.predict_proba(X_test)
    # for i in range(len(probability)):
    #     print(str(probability[i]) + "  " + test_sentences[i])

    elapsed_time = time.time() - start
    print("ElapsedTime:" + str(elapsed_time) + "[sec]")


if __name__ == "__main__":
   main()
