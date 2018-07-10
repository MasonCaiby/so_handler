#You know, this should have been one class...

import numpy
import sys
import os, errno, time
from keras.models import Sequential
from keras.layers import Dense, Dropout, LSTM
from keras.callbacks import ModelCheckpoint
from keras.utils import np_utils
from emailer import build_message
from helpers import safe_folder, newest_file, remote_verbose_emailer


def load_and_map(filepath, percentage_words=1):
    ''' DOCSTRING
        This loads the data and maps the words to numbers etc.
        I just hard coded everything, as the actual splits etc. are dependent
        on the file you are using.
        ----------
        INPUTS
        filepath: the file with the text you want to train your poems on
        percentage_words: number of words you want to use to train your model
                          on defaults to 1
        ----------
        RETURNS
        corpus: a list of every word or character, in the order they appear in
        character_to_int: dictionary {character: int}
        int_to_character: dictionary {int: character}
        corpus_length: the total number of characters in poem_words
        n_vocab: the number of unique characters
    '''

    # load text file
    with open(filepath) as f:
        text = f.read().lower()

    corpus = text[:int(len(text)*percentage_words)]

    characters = sorted(list(set(corpus)))
    character_to_int = dict((c, i) for i, c in enumerate(characters))
    int_to_character = dict((i, c) for c, i in character_to_int.items())

    # summarize the dataset
    corpus_length = len(corpus)
    n_vocab = len(characters)
    return corpus, character_to_int, int_to_character, corpus_length, n_vocab


def prep_data_set(corpus_length, corpus, character_to_int, n_vocab,
                  seq_length=100):
    ''' DOCSTRING
        This makes the patterns you train a model on. since it is an LSTM
        model, you split it into patterns of seq_length words and give it the
        word that should follow. Right now, I have it hard coded to 100, though
        you could change it if you wanted (I believe 100 is a good number for
        most things, so I leave it)
        ---------
        INPUTS
        corpus_length: the number of chars you have to train on
        corpus: the list of characters you are training your model on
        character_to_int: the dictionary that converts words to integers
        n_vocab: the number of unique words you have
        seq_length: the length of characters/words you want to train your model
        ---------
        RETURNS
        seq_length: the sequence length, currently at 100 characters
        dataX: the different sequences made
        dataY: the word following each sequence
        n_patterns: the total number of
        X: reshaped dataX to patterns by seq length
        y: reshaped dataY to patterns by seq length
    '''
    # prepare the dataset of input to output pairs encoded as integers
    dataX = []
    dataY = []
    for i in range(0, corpus_length - seq_length, 1):
        seq_in = corpus[i:i + seq_length]
        seq_out = corpus[i + seq_length]
        dataX.append([character_to_int[character] for character in seq_in])
        dataY.append(character_to_int[seq_out])
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
    model.add(Dropout(0.5))
    model.add(LSTM(512, return_sequences=True,
                   input_shape=(X.shape[1], X.shape[2])))
    model.add(Dropout(0.5))
    model.add(LSTM(512, return_sequences=True,
                   input_shape=(X.shape[1], X.shape[2])))
    model.add(Dropout(0.5))
    model.add(LSTM(512, return_sequences=False,
                   input_shape=(X.shape[1], X.shape[2])))
    model.add(Dropout(0.5))
    model.add(Dense(y.shape[1], activation='softmax'))
    model.compile(loss='categorical_crossentropy', optimizer='adam')
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
    '''
    # define the checkpoint
    checkpoint = ModelCheckpoint(filepath, monitor='loss', verbose=1,
                                 save_best_only=False, mode='min')
    callbacks_list = [checkpoint]

    # use historical weights, if given
    if weight_file:
        model.load_weights(weight_file)
        model.compile(loss='categorical_crossentropy', optimizer='adam')

    # fit the model
    hista = model.fit(X, y, verbose=1, epochs=1, batch_size=128,
                      callbacks=callbacks_list)
    return model


def make_text(model, dataX, int_to_character, n_vocab):
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
        model: the trained model
        dataX: the X data
        int_to_character: your int_to_word dict
        n_vocab: the number of words you've used
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
        seq_in = [int_to_character[value] for value in pattern]
        sys.stdout.write(result)
        pattern.append(index)
        pattern = pattern[1:len(pattern)]
    print("\nDone.")


def generate_text(model, dataX, int_to_character, n_vocab):
    ''' DOCSTRING
        Same same as make poem, but returns the poem and doesnt print it.
        ---------
        INPUT
        model: model w/ loaded weights
        dataX: the x patterns
        int_to_character: the int to word dictionary
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
        result = int_to_character[index]
        seq_in = [int_to_character[value] for value in pattern]
        poem += result
        pattern.append(index)
        pattern = pattern[1:len(pattern)]
    return poem


def load_data_for_model(text_path, percentage_words=1):
    ''' DOCSTRING
        Loads the data for the model. This essentially gets the numbers etc.
        you need. Call this when you are just trying to predict with the model,
        not train it from scratch. I guess I could just pickle everything in
        here.
        ---------
        INPUT
        text_path: filepath to the training text you have
        percentage_words: the percentage of words from your training set you
                          want to train your model on, useful for test running
                          your model
        ---------
        RETURNS
        dataX: the X sequences
        int_to_character: the int to word dictionary
        n_vocab: the number of unique words
        X: the X sequences
        y: the ys the go with the Xs
    '''

    corpus, character_to_int, int_to_character, corpus_length, n_vocab = \
        load_and_map(text_path, percentage_words)
#   Quick summary of loaded data
#   print('Total Words: {}\nTotal Vocab: {}'.format(n_chars, n_vocab))

#   prep the data so it can be used in the model
    seq_length, dataX, dataY, n_patterns, X, y = \
        prep_data_set(corpus_length, corpus, character_to_int, n_vocab)

#   Summary of the number of patterns
#   print("Total Patterns: {}".format(n_patterns))

    return dataX, int_to_character, n_vocab, X, y


def train_model(text_path, filename_start, filename_end, filepath=False,
                percentage_words=1, start=1, iterations=170,
                remote_verbose_email=False):
    ''' DOCSTRING
        This, as the name suggests, trains the model. You can choose to start
        training a new model or not.
        ---------
        INPUTS
        text_path: the filepath to your training data
        filename_start: the first half of the filepath you will save weights to
                        use it will save the epoch number between the start
                        and end
        filename_end: the second half of the filepath you will save weights to
                      use it will save the epoch number between the start
                      and end
        filepath: if given, will load the old weights if False (default) it
                  will start training a new model
        percentage_words: the number of words you want to train on
        start: the number you want to start on, for file names. useful if
               you're using this function to train the same model on the same
               data multiple times.
        iterations: number of iterations you want to go through
        remote_verbose_email: the email address you want to send the poem to,
                              if you want to monitor progress remotely
        ---------
        RETURNS
        NONE just saves weights to a file
    '''
    # make the data in one go:
    dataX, int_to_character, n_vocab, X, y = \
        load_data_for_model(text_path, percentage_words)

    # make the model
    model = make_model(X, y)

    # safely make the folder if it doesn't exist
    folder_name = filename_start.split('/')[0]
    safe_folder(folder_name)

    if not filepath:
        filepath_save = filename_start + '0' + filename_end
        model = fit_model(model, False, filepath_save, X, y)
        filepath = newest_file(folder_name)
        print('Made file: ', filepath)
        print(generate_text(model, dataX, int_to_character, n_vocab))
        print("\a\n")

    top_range = start + iterations
    for epoch_number in range(start, top_range):
        # refit the model, return the callbacks, model, and latest file path
        # uses the most recent filepath to refit the model
        print('loading weights from: ', filepath)
        filepath_save = filename_start + str(epoch_number) + filename_end
        model = fit_model(model, filepath,
                                          filepath_save, X, y)
        # since we include the loss in the filename we have to check which file
        # we just saved. I can't find a way to get that from keras's callbacks
        filepath = newest_file(folder_name)
        print('saving weights to: ', filepath)

        # make a new poem
        predicted_text = generate_text(model, dataX, int_to_character, n_vocab)
        print(predicted_text)
        print("\a\n")

        # send an email with the message, useful for remote monitoring of model
        # e.g. training on AWS for long periods of time
        if remote_verbose_email:
            remote_verbose_emailer(epoch_number, remote_verbose_email,
                                   predicted_text)


if __name__ == "__main__":
    train_model(text_path='data/pratchett.txt',
                filepath='weights_large/50--loss_1.2281.hdf5',
                filename_start='weights_large/',
                filename_end='--loss_{loss:.4f}.hdf5',
                start=51)
