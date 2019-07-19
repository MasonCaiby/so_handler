from keras.models import Sequential
from keras.layers import Dense, Dropout, LSTM
from keras.callbacks import ModelCheckpoint
from keras.utils import np_utils


class TextGenChar:
    def __init__(self, text_file, model_dir, num_chars=40, email_on=False):
        self.text_file = text_file
        self.model_dir = model_dir
        self.num_chars = num_chars
        self.email_on = email_on

    def load_text(self):
        with open(self.text_file, 'r') as text_file:
            raw_text = text_file.read()


    def make_model(self):
        pass

    def train_model(self):
        pass