from rnn_clean import load_data_for_model, generate_poem
from keras.models import load_model

def make_poem():
    ''' DOCSTRING
        produces a poem. Made all the functions into their own module.
        ---------
        INPUTS
        NONE
        ---------
        RETURNS
        poem: a poem that has been generated
    '''
    dataX, int_to_word, nvocab, X, y = load_data_for_model()

    model = load_model('weights/weights22---1000_words.hdf5')
    model.compile(loss='categorical_crossentropy', optimizer='adam')

    poem = generate_poem(model, dataX, int_to_word, nvocab)
    return poem
