import numpy
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout
from keras.layers import LSTM
from keras.callbacks import ModelCheckpoint
from keras.utils import np_utils
from rnn_clean import make_poem, load_data_for_model
from keras.models import load_model

dataX, int_to_word, nvocab, X, y = load_data_for_model()

model = load_model('weights/7.5311.hdf5')

make_poem('weights/7.5311.hdf5', model, dataX, int_to_word, n_vocab = nvocab)
