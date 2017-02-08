from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.decomposition import PCA
from sklearn.externals import joblib
from sklearn.model_selection import cross_val_score
from sklearn import svm
import numpy as np
import sys, getopt
from random import shuffle
import random
from gensim.models import Word2Vec
import re
import time
import MeCab

wakati = MeCab.Tagger("-Owakati")

fin = open("/Users/tAku/Nextremer/data/wikidata_pNdd_sameTopicANDsameSection2/2000ish.csv", encoding="utf-8")
data_path = "/Users/tAku/Nextremer/data/"
model = Word2Vec.load_word2vec_format(data_path + 'foodVector.bin', binary=True)

file_id2food = open("/Users/tAku/Nextremer/data/wikidata_pNdd_sameTopicANDsameSection2/id2food.txt", encoding="utf-8")
id2food = {}
file_tfidf = open("/Users/tAku/Nextremer/data/wikidata_p_only_sameTopicANDsameSection2/tfidf.txt", encoding="utf-8")
tfidf = {}
remove_squareBracket = re.compile(r'\[.*?\]|（.*?）| \(.*?\)')
original_sentences = []

n_input = 209 # number of features of each step(word)
n_steps = 60 # timesteps

def prepare():
    """construct the id2food dictionary"""
    lines = file_id2food.readlines()
    for line in lines:
        line = line[:-1]
        line = line.split(" ")
        _id = line[0]
        food = "".join(line[1:])
        id2food[int(_id)] = food
    file_id2food.close()
    print("complete making id2food dictionary")

    """construct the tfidf dictionary here"""
    lines = file_tfidf.readlines()
    for line in lines:
        line = line[:-1]
        line = line.split("\t")
        word = line[0]
        tf = int(line[1])
        df = int(line[2])
        _tfidf = float(line[4])
        tfidf[word] = [tf, df, _tfidf]
    file_tfidf.close()
    print("complete making tfidf dictionary")

    lines = fin.readlines()
    lines = lines[1:]
    num_data = 0
    for line in lines[1:]:
        if line.split(",")[0] != "":
            num_data += 1
    print("total : " + str(num_data) + " sentences")
    shuffle(lines)
    max_length = n_steps
    unknown = np.zeros(n_input)

    data = np.zeros((num_data,n_steps * n_input))
    labels = []
    # random.seed(0)
    j = 0   #indenx of sentences (= 0~num_of_labeled_sentences)
    # print(id2food[10])
    for line in lines[1:]:
        line = line.split(",")
        _id = line[0]
        if _id == "":
            continue
        food_id = int(_id[0:len(_id)-7])
        h_sort = int(_id[-7])
        h_id = int(_id[len(_id)-6:len(_id)-4])
        p_id = int(_id[len(_id)-4:len(_id)-2])
        s_id = int(_id[len(_id)-2:len(_id)])
        try:
            id2food[food_id]
        except:
            print(_id)
            continue

        topic = remove_squareBracket.sub("",id2food[food_id])
        label = line[1]
        label = 1 if label == "t" else 0
        labels.append(label)

        text = "".join(line[2:])
        original_sentences.append(text)

        morphemes = wakati.parse(text).split(" ")
        morphemes = morphemes[:-1]
        sentence_length = len(morphemes)

        if len(morphemes) < max_length:
            while len(morphemes) < max_length:
                morphemes.insert(0, "<unknown>")
        elif len(morphemes) > max_length:
            morphemes = morphemes[0:max_length]

        # fout.write(line[1] + ";")
        wordVecs = np.zeros((n_steps,n_input))
        # wordVecs = np.zeros(n_steps*n_input)
        i = 0   #index of term/word of each sentence. range is (0~59)
        for morpheme in morphemes:
            try:
                score = model[morpheme]
                wordVecs[i] = score

                """ここから各単語とトピックの類似度をパラメーターの201番目として渡す"""
                wordVecs[i][200] = model.similarity(topic,morpheme)
            except:
                wordVecs[i] = unknown
                # wordVecs[i][200] = 0
            wordVecs[i][201] = h_sort
            wordVecs[i][202] = h_id
            wordVecs[i][203] = p_id
            wordVecs[i][204] = s_id
            wordVecs[i][205] = sentence_length

            try:
                current_tfidf = tfidf[morpheme]
                wordVecs[i][206] = current_tfidf[0]
                wordVecs[i][207] = current_tfidf[1]
                wordVecs[i][208] = current_tfidf[2]
            except:
                wordVecs[i][206] = 0
                wordVecs[i][207] = 0
                wordVecs[i][208] = 0

            i += 1
        data[j] = np.reshape(wordVecs,(n_steps * n_input))
        j += 1
        # print(str(j) + " files complete vectorizing")
        if j % 100 == 0:
            print(str(j) + " files complete vectorizing")
    print("complete vectorize data set")
    num_dataset = j
    print("dataset size = " + str(num_dataset))
    data = data[:num_dataset]

    rate_of_training_data = 0.8
    num_training_data = int(num_dataset * rate_of_training_data)
    # return np.asarray(data), np.asarray(labels)
    return np.asarray(data[:num_training_data]), np.asarray(labels[:num_training_data]), np.asarray(data[num_training_data:]), np.asarray(labels[num_training_data:]), original_sentences[num_training_data:]


def main():

    X, y, X_test, y_test, test_sentences = prepare()
    print(X_test.shape)
    print(y_test.shape)

    # X, y = prepare()

    print("X.shape = " + str(X.shape) + "  y.shape = " + str(y.shape))

    start = time.time()

    try:
        clf = joblib.load('svmModel.pkl_')
        print("load the pickle file...")
    except:
        print("start training the model...")
        flag4pca = True

        # clf = RandomForestClassifier(n_estimators=1000, max_depth=None, min_samples_split=2, random_state=0, max_features = "auto")
        # clf = ExtraTreesClassifier(n_estimators=1000, max_depth=None, min_samples_split=2, random_state=0, max_features = "auto")
        clf = svm.SVC()

        if flag4pca:
            print("PCA is ON")
            pca = PCA(n_components=100)
            pca.fit(X)
            print(X.shape)
            X_transformed = pca.transform(X)
            print(X_transformed.shape)

            X_test = pca.transform(X_test)
            print(X_test.shape)
            # X_ = pca.inverse_transform(X_transformed)
            # print(X_.shape)
            clf = clf.fit(X_transformed, y)
            scores = cross_val_score(clf, X_transformed, y)

        else:
            print("PCA is OFF")
            clf = clf.fit(X, y)
            scores = cross_val_score(clf, X, y)

        print(scores.mean())

        joblib.dump(clf, 'svmModel.pkl')

    prediction = clf.predict(X_test)
    correct = 0
    if len(prediction) == len(y_test):
        for i in range(len(prediction)):
            if y_test[i] == prediction[i]:
                print("True  " + "y : " + str(y_test[i]) + "p : " + str(prediction[i]) + test_sentences[i])
                correct += 1
            else:
                print("False  " + "y : " + str(y_test[i]) + "p : " + str(prediction[i]) + test_sentences[i])
        print("num correct = " + str(correct) + " out of " + str(len(y_test)) + " = " + str(correct/len(y_test)))
    else:
        print(len(prediction))
        print(len(y_test))
    elapsed_time = time.time() - start
    print("ElapsedTime:" + str(elapsed_time) + "[sec]")


if __name__ == "__main__":
   main()
