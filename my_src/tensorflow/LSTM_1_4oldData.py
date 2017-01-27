'''
A Bidirectional Recurrent Neural Network (LSTM) implementation example using TensorFlow library.
This example is using the MNIST database of handwritten digits (http://yann.lecun.com/exdb/mnist/)
Long Short Term Memory paper: http://deeplearning.cs.cmu.edu/pdfs/Hochreiter97_lstm.pdf
Author: Aymeric Damien
Project: https://github.com/aymericdamien/TensorFlow-Examples/
'''

from __future__ import print_function

import tensorflow as tf
from tensorflow.contrib import rnn
import numpy as np
import sys, getopt
from random import shuffle
import random
from gensim.models import Word2Vec
import re
import MeCab
# Import MNIST data
# from tensorflow.examples.tutorials.mnist import input_data
# mnist = input_data.read_data_sets("/tmp/data/", one_hot=True)

'''
To classify images using a bidirectional recurrent neural network, we consider
every image row as a sequence of pixels. Because MNIST image shape is 28*28px,
we will then handle 28 sequences of 28 steps for every sample.
'''

# Parameters
learning_rate = 0.001
training_iters = 30000
batch_size = 50
display_step = 10
num_data = 0
# Network Parameters
n_input = 202 # MNIST data input (img shape: 28*28)
n_steps = 60 # timesteps
n_hidden = 200 # hidden layer num of features
n_classes = 2 # MNIST total classes (0-9 digits)
num_training = 2500 # the number of training data

# tf Graph input
x = tf.placeholder("float", [None, n_steps, n_input])
y = tf.placeholder("float", [None, n_classes])
wakati = MeCab.Tagger("-Owakati")
chasen = MeCab.Tagger('-Ochasen')
# Define weights
weights = {
    # Hidden layer weights => 2*n_hidden because of forward + backward cells
    'out': tf.Variable(tf.random_normal([2*n_hidden, n_classes]))
}
biases = {
    'out': tf.Variable(tf.random_normal([n_classes]))
}

fin = open("/Users/tAku/Nextremer/data/wikidata_pNdd_sameTopicANDsameSection2/candidate.txt", encoding="utf-8")
data_path = "/Users/tAku/Nextremer/data/"
model = Word2Vec.load_word2vec_format(data_path + 'foodVector.bin', binary=True)

# file_id2food = open("/Users/tAku/Nextremer/data/wikidata_pNdd_sameTopicANDsameSection2/id2food.txt", encoding="utf-8")
# id2food = {}
remove_squareBracket = re.compile(r'\[.*?\]|（.*?）| \(.*?\)')
original_sentences = []
def prepare():
    lines = fin.readlines()
    shuffle(lines)
    max_length = n_steps
    unknown = np.zeros(n_input)
    num_data = len(lines)
    data = np.zeros((len(lines),n_steps,n_input))
    labels = []
    # random.seed(0)
    j = 0   #indenx of sentences (= 0~num_of_labeled_sentences)

    for line in lines:
        line = line[:-1]
        line = line.split(",")
        label = line[0]
        line = line[1].split(":")
        topic = line[0]
        sentence = line[1]
        onehot = [1,0] if label == "t" else [0,1]
        labels.append(onehot)

        original_sentences.append(sentence)
        morphemes = wakati.parse(sentence).split(' ')
        sentence_length = len(morphemes)

        if len(morphemes) < max_length:
            while len(morphemes) < max_length:
                morphemes.insert(0, "<unknown>")
        elif len(morphemes) > max_length:
            morphemes = morphemes[0:max_length]

        # fout.write(line[1] + ";")
        wordVecs = np.zeros((n_steps,n_input))
        i = 0   #index of term/word of each sentence. range is (0~59)
        for morpheme in morphemes:
            try:
                score = model[morpheme]
                wordVecs[i] = score
                wordVecs[i][200] = model.similarity(topic,morpheme)
            except:
                wordVecs[i] = unknown
                # wordVecs[i][200] = 0
            wordVecs[i][201] = sentence_length

            i += 1
        data[j] = wordVecs
        j += 1
        # print(str(j) + " files complete vectorizing")
        if j % 100 == 0:
            print(str(j) + " files complete vectorizing")
    print("complete vectorize data set")

    return np.asarray(data[:num_training]), np.asarray(data[num_training:]), np.asarray(labels[:num_training]), np.asarray(labels[num_training:])

def get_next_batch(x, y, step):
    # shuffle(index)
    batch_x = x[step*batch_size:(step+1)*batch_size]
    batch_y = y[step*batch_size:(step+1)*batch_size]
    # for i in range(batch_size):
    #     batch_x.append(x[index[i]])
    #     batch_y.append(y[index[i]])
    return np.asarray(batch_x), np.asarray(batch_y)


def BiRNN(x, weights, biases):

    # Prepare data shape to match `bidirectional_rnn` function requirements
    # Current data input shape: (batch_size, n_steps, n_input)
    # Required shape: 'n_steps' tensors list of shape (batch_size, n_input)

    # Permuting batch_size and n_steps
    x = tf.transpose(x, [1, 0, 2])
    # Reshape to (n_steps*batch_size, n_input)
    x = tf.reshape(x, [-1, n_input])
    # Split to get a list of 'n_steps' tensors of shape (batch_size, n_input)
    x = tf.split(0, n_steps, x)

    # Define lstm cells with tensorflow
    # Forward direction cell
    lstm_fw_cell = tf.nn.rnn_cell.BasicLSTMCell(n_hidden, forget_bias=1.0)
    # Backward direction cell
    lstm_bw_cell = tf.nn.rnn_cell.BasicLSTMCell(n_hidden, forget_bias=1.0)

    # Get lstm cell output
    try:
        outputs, _, _ = tf.nn.bidirectional_rnn(lstm_fw_cell, lstm_bw_cell, x, dtype=tf.float32)
    except Exception: # Old TensorFlow version only returns outputs not states
        outputs, states = tf.nn.bidirectional_rnn(lstm_fw_cell, lstm_bw_cell, x, dtype=tf.float32)

    # Linear activation, using rnn inner loop last output
    return tf.matmul(outputs[-1], weights['out']) + biases['out']

def main(argv):

    x_train, x_test, y_train, y_test = prepare()

    index4shuffle = [i for i in range(num_training)]

    pred = BiRNN(x, weights, biases)

    # prediction = tf.nn.softmax_cross_entropy_with_logits(logits=pred, labels=y)
    prediction = tf.nn.softmax(logits=pred)
    prediction = tf.cast(tf.argmax(prediction, 1), tf.int32)

    # Define loss and optimizer
    cost = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=pred, labels=y))
    optimizer = tf.train.AdamOptimizer(learning_rate=learning_rate).minimize(cost)

    # Evaluate model
    correct_pred = tf.equal(tf.argmax(pred,1), tf.argmax(y,1))
    accuracy = tf.reduce_mean(tf.cast(correct_pred, tf.float32))

    # Initializing the variables
    init = tf.initialize_all_variables()

    # Launch the graph
    with tf.Session() as sess:
        sess.run(init)
        step = 0
        flag2shuffle = False
        cycle = num_training/batch_size
        # Keep training until reach max iterations
        while step * batch_size < training_iters:
            if (step%cycle) * batch_size <= num_training and ((step+1) % cycle) * batch_size > num_training:
                shuffle(index4shuffle)
            # batch_x, batch_y = mnist.train.next_batch(batch_size)
            batch_x, batch_y = get_next_batch(x_train, y_train, step%cycle)
            # print(batch_x.shape)
            # print(batch_y.shape)
            # Reshape data to get 28 seq of 28 elements
            batch_x = batch_x.reshape((batch_size, n_steps, n_input))
            # Run optimization op (backprop)
            sess.run(optimizer, feed_dict={x: batch_x, y: batch_y})
            if step % display_step == 0:
                # Calculate batch accuracy
                acc = sess.run(accuracy, feed_dict={x: batch_x, y: batch_y})
                # Calculate batch loss
                loss = sess.run(cost, feed_dict={x: batch_x, y: batch_y})
                print("Iter " + str(step*batch_size) + ", Minibatch Loss= " + \
                      "{:.6f}".format(loss) + ", Training Accuracy= " + \
                      "{:.5f}".format(acc))
            step += 1
        print("Optimization Finished!")

        # Calculate accuracy for 128 mnist test images
        # test_len = num_data - 1000
        # test_data = mnist.test.images[:test_len].reshape((-1, n_steps, n_input))
        # test_label = mnist.test.labels[:test_len]
        print("Testing Accuracy:", \
            sess.run(accuracy, feed_dict={x: x_test, y: y_test}))

        """
        make prediction
        """
        fout = open("/Users/tAku/Nextremer/data/wikidata_pNdd_sameTopicANDsameSection2/prediction.csv", "w", encoding="utf-8")
        classification = prediction.eval(feed_dict = {x: x_test})
        test_sentences = original_sentences[num_training:]
        fout.write("prediction,label,sentence\n")
        if len(classification) == len(y_test):
            for i in range(len(classification)):
                # label = 0
                fout.write(str(classification[i]) + "," + ("0" if y_test[i][0]==1 else "1") + "," + test_sentences[i] + "\n")

if __name__ == "__main__":
   main(sys.argv[1:])
