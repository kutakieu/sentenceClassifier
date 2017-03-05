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

wakati = MeCab.Tagger("-Owakati")
chasen = MeCab.Tagger("-Ochasen")

fin = open("/Users/tAku/Nextremer/data/wikidata_p_only_sameTopicANDsameSection2/0208_annotation_shuffled.tsv", encoding="utf-8")
data_path = "/Users/tAku/Nextremer/data/"

#日本語のページ全体のワードベクトル
# w2v_model = Word2Vec.load_word2vec_format(data_path + 'jawiki_all.bin', binary=True, unicode_errors='ignore')

#フードドメインのみで作ったワードベクトル
w2v_model = Word2Vec.load_word2vec_format(data_path + 'foodVector.bin', binary=True)

# file_id2food = open("/Users/tAku/Nextremer/data/wikidata_p_only_sameTopicANDsameSection2/id2food.txt", encoding="utf-8")
# id2food = {}
file_tfidf = open("/Users/tAku/Nextremer/data/wikidata_p_only_sameTopicANDsameSection2/tfidf.txt", encoding="utf-8")
tfidf = {}
remove_squareBracket = re.compile(r'\[.*?\]|（.*?）| \(.*?\)')
original_sentences = []

n_input = 4 # number of features of each step(word)
n_steps = 10 # timesteps

def prepare():
    # """construct the id2food dictionary"""
    # lines = file_id2food.readlines()
    # for line in lines:
    #     line = line[:-1]
    #     line = line.split(" ")
    #     _id = line[0]
    #     food = "".join(line[1:])
    #     id2food[int(_id)] = food
    # file_id2food.close()
    # print("complete making id2food dictionary")

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
    # lines = lines[1:]
    num_data = 0
    training_lines = []
    for line in lines:
        if line.split("\t")[3] == "t" or line.split("\t")[3] == "f":
            num_data += 1
            training_lines.append(line)
    print("total : " + str(num_data) + " sentences")
    shuffle(training_lines)
    max_length = n_steps
    unknown = np.zeros(n_input)

    data = np.zeros((num_data,n_steps * n_input + 5))

    labels = []
    # random.seed(0)
    j = 0   #indenx of sentences (= 0~num_of_labeled_sentences)
    # print(id2food[10])
    for line in training_lines:
        line = line.split("\t")
        _id = line[0]
        if _id == "":
            continue
        food_id = int(_id[0:len(_id)-7])
        h_sort = int(_id[-7])
        h_id = int(_id[len(_id)-6:len(_id)-4])
        p_id = int(_id[len(_id)-4:len(_id)-2])
        s_id = int(_id[len(_id)-2:len(_id)])
        # try:
        #     id2food[food_id]
        # except:
        #     print(_id)
        #     continue

        topic = remove_squareBracket.sub("",line[2])
        label = line[3]
        label = 1 if label == "t" else 0
        labels.append(label)

        text = "".join(line[4:])
        original_sentences.append(text)

        morphemes = wakati.parse(text).split(" ")
        morphemes = morphemes[:-1]
        sentence_length = len(morphemes)

        nouns = []
        for morpheme in morphemes:
            if "名詞" == chasen.parse(morpheme).split("\t")[0].split("-")[0]:
                nouns.append(morpheme)

        if len(nouns) < max_length:
            while len(nouns) < max_length:
                nouns.insert(0, "<unknown>")
        elif len(nouns) > max_length:
            nouns = nouns[0:max_length]

        # fout.write(line[1] + ";")
        wordVecs = np.zeros((n_steps,n_input))
        # wordVecs = np.zeros(n_steps*n_input)
        i = 0   #index of term/word of each sentence. range is (0~59)

        for morpheme in nouns:
            try:
                # score = w2v_model[morpheme]
                # wordVecs[i] = score

                """ここから各単語とトピックの類似度をパラメーターの201番目として渡す"""
                # if "名詞" == chasen.parse(morpheme).split("\t")[0].split("-")[0]:
                wordVecs[i][0] = w2v_model.similarity(topic,morpheme)
            except:
                wordVecs[i][0] = 0
                # wordVecs[i][200] = 0
            # wordVecs[i][1] = h_sort
            # wordVecs[i][2] = h_id
            # wordVecs[i][3] = p_id
            # wordVecs[i][4] = s_id
            # wordVecs[i][5] = sentence_length
            try:
                temp_tfidf = tfidf[morpheme]
                wordVecs[i][1] = temp_tfidf[0]
                wordVecs[i][2] = temp_tfidf[1]
                wordVecs[i][3] = temp_tfidf[2]
            except:
                wordVecs[i][1] = 0
                wordVecs[i][2] = 0
                wordVecs[i][3] = 0

            i += 1
        wordVecs = np.reshape(wordVecs,(n_steps * n_input))
        wordVecs = np.append(wordVecs, h_sort)
        wordVecs = np.append(wordVecs, h_id)
        wordVecs = np.append(wordVecs, p_id)
        wordVecs = np.append(wordVecs, s_id)
        wordVecs = np.append(wordVecs, sentence_length)
        data[j] = wordVecs
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
    print(X.shape)
    print(y.shape)
    print(X_test.shape)
    print(y_test.shape)

    # X, y = prepare()

    print("X.shape = " + str(X.shape) + "  y.shape = " + str(y.shape))

    start = time.time()

    try:
        clf = joblib.load('LogisticRegression.pkl_')
        print("load the pickle file...")
    except:
        print("start training the model...")
        flag4pca = False

        clf = LogisticRegression()

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

        joblib.dump(clf, 'LogisticRegression.pkl')

    prediction = clf.predict(X_test)
    probability = clf.predict_proba(X_test)
    correct = 0
    if len(prediction) == len(y_test):
        for i in range(len(prediction)):
            if y_test[i] == prediction[i]:
                print("True  " + "y : " + str(y_test[i]) + " p : " + str(prediction[i]) +  "  " + test_sentences[i])
                print(probability[i])
                correct += 1
            else:
                print("False  " + "y : " + str(y_test[i]) + " p : " + str(prediction[i]) + "  " + test_sentences[i])
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
