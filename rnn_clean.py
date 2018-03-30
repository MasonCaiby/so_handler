import numpy
import sys
from keras.models import Sequential
from keras.layers import Dense, Dropout, LSTM
from keras.callbacks import ModelCheckpoint
from keras.utils import np_utils

def load_and_map():
    # load text file
    poems = [word+' ' for word in open('data/cleanedpoems.txt').read().split(' ')]

    # create mapping of unique chars to integers
    words = sorted(list(set(poems)))
    word_to_int = dict((c, i) for i, c in enumerate(words))
    int_to_word = dict((i, c) for i, c in enumerate(words))
    # summarize the dataset
    n_words = len(poems)
    n_vocab = len(words)
    return poems, words, word_to_int, int_to_word, n_words, n_vocab


def prep_data_set(n_words, poems, word_to_int, n_vocab):
    # prepare the dataset of input to output pairs encoded as integers
    seq_length = 10
    dataX = []
    dataY = []
    for i in range(0, n_words - seq_length, 1):
        seq_in = poems[i:i + seq_length]
        seq_out = poems[i + seq_length]
        dataX.append([word_to_int[word] for word in seq_in])
        dataY.append(word_to_int[seq_out])
    n_patterns = len(dataX)

    # reshape X to be [samples, time steps, features]
    X = numpy.reshape(dataX, (n_patterns, seq_length, 1))
    # normalize
    X = X / float(n_vocab)
    # one hot encode the output variable
    y = np_utils.to_categorical(dataY)

    return seq_length, dataX, dataY, n_patterns, X, y


def make_model(X, y):
    # define the LSTM model
    model = Sequential()
    model.add(LSTM(512, return_sequences=True,
                   input_shape=(X.shape[1], X.shape[2])))
    model.add(LSTM(512, return_sequences=False,
                   input_shape=(X.shape[1], X.shape[2])))
    model.add(Dropout(0.2))
    model.add(Dense(y.shape[1], activation='softmax'))
    model.compile(loss='categorical_crossentropy', optimizer='rmsprop')
    return model

def fit_model(model, weight_file, i):
    # define the checkpoint
    filepath = "weights/weights"+str(i)+"---all_words.hdf5"
    checkpoint = ModelCheckpoint(filepath, monitor='loss', verbose=1,
                                 save_best_only=False, mode='min')
    callbacks_list = [checkpoint]

    # use historical weights, if given
    if weight_file:
        model.load_weights(weight_file)

    # fit the model
    hista = model.fit(X, y, verbose=1, epochs=1, batch_size=1, callbacks=callbacks_list)
    return model, callbacks_list, filepath


def make_poem(weight_file, model, dataX, int_to_word, n_vocab):
    # load the network weights
    filename = weight_file
    model.load_weights(filename)
    model.compile(loss='categorical_crossentropy', optimizer='adam')
    # pick a random seed
    start = numpy.random.randint(0, len(dataX)-1)
    pattern = dataX[start]
    print("Seed:")
    print("\"", ''.join([int_to_word[value] for value in pattern]), "\"")
    # generate characters
    for i in range(100):
        x = numpy.reshape(pattern, (1, len(pattern), 1))
        x = x / float(n_vocab)
        prediction = model.predict(x, verbose=0)
        index = numpy.argmax(prediction)
        result = int_to_word[index]
        seq_in = [int_to_word[value] for value in pattern]
        sys.stdout.write(result)
        pattern.append(index)
        pattern = pattern[1:len(pattern)]
    print("\nDone.")


def load_data_for_model():
    poems, words, word_to_int, int_to_word, n_words, n_vocab = load_and_map()
#   Quick summary of loaded data
    print('Total Words: {}\nTotal Vocab: {}'.format(n_words, n_vocab))

#   prep the data so it can be used in the model
    seq_length, dataX, dataY, n_patterns, X, y = \
        prep_data_set(n_words, poems, word_to_int, n_vocab)

#   Summary of the number of patterns
    print("Total Patterns: {}".format(n_patterns))

    return dataX, int_to_word, n_vocab, X, y


if __name__ == "__main__":

    # make the data in one go:
    dataX, int_to_word, n_vocab, X, y = load_data_for_model()

    # make the model
    model = make_model(X, y)


    for i in range(170):
        # refit the model, return the callbacks, model, and latest file path
        # uses the most recent filepath to refit the model
        #filepath = 'weights/weights'+str(i)+'.hdf5' if i == 0 else 'weights/weights'+str(i - 1)+'---1000_words.hdf5'
        filepath = False
        model, callbacks_list, filepath = fit_model(model, filepath, i)
        print(filepath)
        # make a new poem
        make_poem(filepath, model=model, dataX=dataX, int_to_word=int_to_word, n_vocab=n_vocab)
        print("\a")
