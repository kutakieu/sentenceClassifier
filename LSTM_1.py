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
training_iters = 20000
batch_size = 50
display_step = 10
num_data = 0
# Network Parameters
n_input = 206 # MNIST data input (img shape: 28*28)
n_steps = 60 # timesteps
n_hidden = 200 # hidden layer num of features
n_classes = 2 # MNIST total classes (0-9 digits)

# tf Graph input
x = tf.placeholder("float", [None, n_steps, n_input])
y = tf.placeholder("float", [None, n_classes])

# Define weights
weights = {
    # Hidden layer weights => 2*n_hidden because of forward + backward cells
    'out': tf.Variable(tf.random_normal([2*n_hidden, n_classes]))
}
biases = {
    'out': tf.Variable(tf.random_normal([n_classes]))
}

fin = open("/Users/tAku/Nextremer/data/wikidata_pNdd_sameTopicANDsameSection2/2000_annotated_wakati.csv", encoding="utf-8")
data_path = "/Users/tAku/Nextremer/data/"
model = Word2Vec.load_word2vec_format(data_path + 'foodVector.bin', binary=True)

file_id2food = open("/Users/tAku/Nextremer/data/wikidata_pNdd_sameTopicANDsameSection2/id2food.txt", encoding="utf-8")
id2food = {}
remove_squareBracket = re.compile(r'\[.*?\]|（.*?）| \(.*?\)')
def prepare():
    """
    construct the id2food dictionary
    """
    lines = file_id2food.readlines()
    for line in lines:
        line = line[:-1]
        line = line.split(" ")
        _id = line[0]
        food = "".join(line[1:])
        id2food[int(_id)] = food
    print("complete making id2food dictionary")

    lines = fin.readlines()
    shuffle(lines)
    max_length = n_steps
    unknown = np.zeros(n_input)
    num_data = len(lines)
    data = np.zeros((len(lines),n_steps,n_input))
    labels = []
    # random.seed(0)
    j = 0   #indenx of sentences (= 0~num_of_labeled_sentences)
    # print(id2food[10])
    for line in lines:
        line = line.split(",")
        _id = line[0]
        food_id = int(_id[0:len(_id)-7])
        h_sort = int(_id[-7])
        h_id = int(_id[len(_id)-6:len(_id)-4])
        p_id = int(_id[len(_id)-4:len(_id)-2])
        s_id = int(_id[len(_id)-2:len(_id)])
        topic = remove_squareBracket.sub("",id2food[food_id])
        label = line[1]
        onehot = [1,0] if label == "t" else [0,1]
        labels.append(onehot)

        morphemes = line[2].split(" ")
        morphemes = morphemes[:-1]
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
                """
                ここから各単語とトピックの類似度をパラメーターの201番目として渡す
                """
                wordVecs[i][200] = model.similarity(topic,morpheme)
            except:
                wordVecs[i] = unknown
                # wordVecs[i][200] = unknown
            wordVecs[i][201] = h_sort
            wordVecs[i][202] = h_id
            wordVecs[i][203] = p_id
            wordVecs[i][204] = s_id
            wordVecs[i][205] = sentence_length
            i += 1
        data[j] = wordVecs
        j += 1
        # print(str(j) + " files complete vectorizing")
        if j % 100 == 0:
            print(str(j) + " files complete vectorizing")
    print("complete vectorize data set")

    return np.asarray(data[:1000]), np.asarray(data[1000:]), np.asarray(labels[:1000]), np.asarray(labels[1000:])

def get_next_batch(x, y, index):
    shuffle(index)
    batch_x = []
    batch_y = []
    for i in range(batch_size):
        batch_x.append(x[index[i]])
        batch_y.append(y[index[i]])
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

    index4shuffle = [i for i in range(1000)]

    pred = BiRNN(x, weights, biases)

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
        step = 1
        # Keep training until reach max iterations
        while step * batch_size < training_iters:
            # batch_x, batch_y = mnist.train.next_batch(batch_size)
            batch_x, batch_y = get_next_batch(x_train, y_train, index4shuffle)
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

if __name__ == "__main__":
   main(sys.argv[1:])
