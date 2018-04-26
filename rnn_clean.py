import numpy
import sys
from keras.models import Sequential
from keras.layers import Dense, Dropout, LSTM
from keras.callbacks import ModelCheckpoint
from keras.utils import np_utils


def load_and_map(percentage_words=1):
    ''' DOCSTRING
        This loads the data and maps the words to numbers etc.
        I just hard coded everything, as the actual splits etc. are dependent
        on the file you are using.
        ----------
        INPUTS
        percentage_words: number of words you want to use to train your model
                          on defaults to 1
        ----------
        RETURNS
        poem_words: a list of every word, in the order they appear in
        words: a sorted set of the poem_words
        word_to_int: dictionary word: int
        int_to_word: dictionary int: word
        n_words: the total number of words in poem_words
        n_vocab: the number of unique words
    '''

    # load text file

    with open('data/cleanedpoems.txt') as f:
        poem_words = [word+' ' for word in f.read().split(' ')]

    num_words = int(len(poem_words)*percentage_words)
    poem_words = poem_words[:num_words]

    # create mapping of unique chars to integers
    words = sorted(list(set(poem_words)))
    word_to_int = dict((c, i) for i, c in enumerate(words))
    int_to_word = dict((i, c) for i, c in enumerate(words))
    # summarize the dataset
    n_words = len(poem_words)
    n_vocab = len(words)
    return poem_words, words, word_to_int, int_to_word, n_words, n_vocab


def prep_data_set(n_words, poems, word_to_int, n_vocab):
    ''' DOCSTRING
        This makes the patterns you train a model on. since it is an LSTM
        model, you split it into patterns of seq_length words and give it the
        word that should follow. Right now, I have it hard coded to 10, though
        you could change it if you wanted (I believe 10 is a good number for
        most things, so I leave it)
        ---------
        INPUTS
        n_words: the number of words you have to train on
        poems: the word list
        word_to_int: the dictionary that converts words to integers
        n_vocab: the number of unique words you have
        ---------
        RETURNS
        seq_length: the sequence length, currently at 10 words
        dataX: the different sequences made
        dataY: the word following each sequence
        n_patterns: the total number of
        X: reshaped dataX to patterns by seq length
        y: reshaped dataY to patterns by seq length
    '''
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
    ''' DOCSTRING
        This builds the model, you need X and Y to tell it the input shapes.
        It uses categorical crossentropy and a softmax activation. It seemed
        like people used variations of these from the time I looked online.
        -----------
        INPUT:
        X: the X data, this is just for to shape the model
        y: the y data, this is just for to shape the model
        -----------
        RETURNS:
        model: The model that has been built.
    '''
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


def fit_model(model, weight_file, filepath, X, y):
    ''' DOCSTRING
        This fits the model. It saves the weights to filepath and optionally
        loads the wieghts from weight_file.
        ---------
        INPUTS
        model: the model you are trying to train
        weight_file: the latest weight file for the model
        filepath: the filepath you want to save to
        X: the X data
        y: the y data
        ---------
        RETURNS
        model: the model, if you are loading pretrained weights, you dont need
               to remake the model
        callbacks_list: the callbacks returned from the keras model
        filepath: the saved filepath
    '''
    # define the checkpoint
    checkpoint = ModelCheckpoint(filepath, monitor='loss', verbose=1,
                                 save_best_only=False, mode='min')
    callbacks_list = [checkpoint]

    # use historical weights, if given
    if weight_file:
        model.load_weights(weight_file)

    # fit the model
    hista = model.fit(X, y, verbose=1, epochs=1, batch_size=1,
                      callbacks=callbacks_list)
    return model, callbacks_list, filepath


def make_poem(model, dataX, int_to_word, n_vocab):
    ''' DOCSTRING
        This makes a poem, from the model and a randomly selected pattern.
        I MIGHT eventually build this out so it can take a sequnce given to it
        so I can read in a comment on  photo and make a poem from that. But
        that would mean all words in the comment would have to be in my word
        bank. That seems improbable though (doggo, pupper, puns etc.) I'd have
        to decide on a filler word. But I'm not sure I want to do that right
        now.
        ---------
        INPUT
        model
        dataX
        int_to_word
        n_vocab
        ---------
        RETURNS
        NONE just a printed poem
    '''
    # load the network weights
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


def generate_poem(model, dataX, int_to_word, n_vocab):
    ''' DOCSTRING
        Same same as make poem, but returns the poem and doesnt print it.
        ---------
        INPUT
        model: model w/ loaded weights
        dataX: the x patterns
        int_to_word: the int to word dictionary
        n_vocab: the number of unique words you have
        ---------
        RETURNS
        poem: the generated poem
    '''
    start = numpy.random.randint(0, len(dataX)-1)
    pattern = dataX[start]
    # generate characters
    poem = ''
    for i in range(100):
        x = numpy.reshape(pattern, (1, len(pattern), 1))
        x = x / float(n_vocab)
        prediction = model.predict(x, verbose=0)
        index = numpy.argmax(prediction)
        result = int_to_word[index]
        seq_in = [int_to_word[value] for value in pattern]
        poem += result
        pattern.append(index)
        pattern = pattern[1:len(pattern)]
    print('generate_poem\'s poem:', poem)
    return poem


def load_data_for_model(percentage_words=1):
    ''' DOCSTRING
        Loads the data for the model. This essentially gets the numbers etc.
        you need. Call this when you are just trying to predict with the model,
        not train it from scratch. I guess I could just pickle everything in
        here.
        ---------
        INPUT
        NONE
        ---------
        RETURNS
        dataX: the X sequences
        int_to_word: the int to word dictionary
        n_vocab: the number of unique words
        X: the X sequences
        y: the ys the go with the Xs
    '''
    poems, words, word_to_int, int_to_word, n_words, n_vocab = \
                                                load_and_map(percentage_words)
#   Quick summary of loaded data
#   print('Total Words: {}\nTotal Vocab: {}'.format(n_words, n_vocab))

#   prep the data so it can be used in the model
    seq_length, dataX, dataY, n_patterns, X, y = \
        prep_data_set(n_words, poems, word_to_int, n_vocab)

#   Summary of the number of patterns
#   print("Total Patterns: {}".format(n_patterns))

    return dataX, int_to_word, n_vocab, X, y


def train_model(filename_start, filename_end, filepath=False):
    ''' DOCSTRING
        This, as the name suggests, trains the model. You can choose to start
        training a new model or not.
        ---------
        INPUTS
        filename_start: the first half of the filepath you will save weights to
                        use it will save the epoch number between the start
                        and end
        filename_end: the second half of the filepath you will save weights to
                      use it will save the epoch number between the start
                      and end
        filepath: if given, will load the old weights if False (default) it
                  will start training a new model
        ---------
        RETURNS
        NONE just saves weights to a file
    '''
    # make the data in one go:
    dataX, int_to_word, n_vocab, X, y = \
                                load_data_for_model(percentage_words=1)

    # make the model
    model = make_model(X, y)

    if not filepath:
        filepath_save = filename_start + '0' + filename_end
        model, callbacks_list, filepath = fit_model(model, False,
                                                    filepath_save, X, y)
        print('Made file: ', filepath)
    for i in range(1, 170):
        # refit the model, return the callbacks, model, and latest file path
        # uses the most recent filepath to refit the model
        print('loading weights from: ', filepath)
        filepath_save = filename_start + str(i) + filename_end
        model, callbacks_list, filepath = fit_model(model, filepath,
                                                    filepath_save, X, y)
        print('saving weights to: ', filepath)
        # make a new poem
        print(generate_poem(model, dataX, int_to_word, n_vocab))
        print("\a")


if __name__ == "__main__":
    train_model(filename_start='weights/weights_',
                filename_end='_10_perc_words.hdf5')
