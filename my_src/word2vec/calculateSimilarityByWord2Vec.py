from gensim.models import Word2Vec
import MeCab
import re
data_path = "/Users/tAku/Nextremer/data/"
punctuation = ["、","。","(",")","[","]","「","」","・","\n"," "]

wakati = MeCab.Tagger("-Owakati")
chasen = MeCab.Tagger("-Ochasen")

text_file = open(data_path + "candidate3.txt", encoding = "utf-8")

lines = text_file.readlines()

model = Word2Vec.load_word2vec_format(data_path + 'vectors_food.bin', binary=True)

t_score = 0
num_t = 0
f_score = 0
num_f = 0

for line in lines:
    count = 0
    score = 0
    label,text = line.split(',')
    topic,text = text.split(':')
    #print(text)
    morphemes = wakati.parse(text).split(' ')
    for morpheme in morphemes:
        if morpheme in punctuation:
            continue
        else:
            try:
                result = chasen.parse(morpheme).split('\t')[3].split('-')[0]    #MeCabの結果から品詞のみを抽出する
                if result == '名詞' and topic != morpheme:
                    count += 1
                    score += model.similarity(topic, morpheme)
                    print(morpheme + " " + str(model.similarity(topic, morpheme)))
            except:
                count -= 1
                print(morpheme + " is not in the vocabulary")
                continue

    print(count)
    print(label + " " + topic + " " + text)
    if count != 0:
        print("score = " + str(score / count))
        if label == 't':
            t_score += (score/count)
            num_t += 1
        else:
            f_score += (score/count)
            num_f += 1

print("t_score = " + str(t_score/num_t))
print("f_score = " + str(f_score/num_f))
    #print(text)
