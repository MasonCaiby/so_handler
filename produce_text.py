from rnn_clean_large import load_data_for_model, generate_text
from keras.models import load_model


def make_poem(weights_file):
    ''' DOCSTRING
        produces a poem. Made all the functions into their own module.
        ---------
        INPUTS
        NONE
        ---------
        RETURNS
        poem: a poem that has been generated
    '''
    dataX, int_to_word, nvocab, X, y = load_data_for_model('data/pratchett.txt')

    model = load_model(weights_file)
    model.compile(loss='categorical_crossentropy', optimizer='adam')

    poem = generate_text(model, dataX, int_to_word, nvocab, 1000)
    return poem
