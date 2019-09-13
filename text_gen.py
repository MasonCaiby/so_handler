import numpy as np
import re
import os

from keras.models import Sequential
from keras.layers import Dense, Dropout, LSTM, BatchNormalization
from keras.callbacks import ModelCheckpoint
from keras.utils import np_utils

os.environ['KMP_DUPLICATE_LIB_OK']='True'


class TextGenChar:
    def __init__(self, text_file, num_chars=40, seq_length=50, email_on=False, percent_text=1.0):
        self.text_file = text_file

        self.num_chars = num_chars
        self.email_on = email_on
        self.seq_length = seq_length
        self.percent_text = percent_text

        # load text
        self.text = None
        self.corpus = None
        self.length = 0
        self.char_len = 0
        self.n_char = {}
        self.char_n = {}
        self.f_to_char = {}

        # pre_process
        self.X = []
        self.Y = []
        self.X_m = None
        self.Y_m = None

    def load_text(self):
        with open(self.text_file, 'r', encoding="utf8") as text_file:
            raw_text = text_file.read()
        self.text = re.sub(r'\n+', '\n', raw_text).strip()
        self.text = raw_text.lower()
        self.text = self.text[:int(len(self.text)*self.percent_text)]
        self.corpus = self.text
        self.length = len(self.text)

        characters = sorted(list(set(self.text)))
        self.char_len = len(characters)
        for n, char in enumerate(characters):
            self.n_char[n] = char
            self.char_n[char] = n

        self.corpus = list(map(lambda x: self.char_n[x], [a for a in self.text]))

    def pre_processsing(self):
        for i in range(self.length - self.seq_length):
            sequence = self.corpus[i:i+self.seq_length]
            label = self.corpus[i+self.seq_length]
            self.X.append(sequence)
            self.Y.append(label)

        self.X_m = np.reshape(self.X, (len(self.X), self.seq_length, 1))
        self.X_m = self.X_m / float(len(self.n_char))
        self.Y_m = np_utils.to_categorical(self.Y)


class TextGenModel:
    def __init__(self, text_obj, model_dir, temp):
        self.text_obj = text_obj
        self.model_dir = model_dir
        self.temp = temp

        self.model = Sequential()

    def build_model(self):
        self.model.add(LSTM(512,
                            input_shape=(self.text_obj.X_m.shape[1],
                                         self.text_obj.X_m.shape[2]),
                            return_sequences=True))
        self.model.add(Dropout(0.2))
        self.model.add(LSTM(256, return_sequences=True))
        self.model.add(Dropout(0.2))
        self.model.add(LSTM(128))
        self.model.add(BatchNormalization())
        self.model.add(Dense(self.text_obj.Y_m.shape[1], activation='softmax'))
        self.model.compile(loss='categorical_crossentropy', optimizer='adam')

    def train_model(self):
        for _ in range(200):
            filepath = self.model_dir+"model_.hdf5"

            checkpoint = ModelCheckpoint(filepath, monitor='loss', verbose=1,
                                         save_best_only=False, mode='min')
            callbacks_list = [checkpoint]

            self.model.fit(self.text_obj.X_m, self.text_obj.Y_m,
                           verbose=1, epochs=1, batch_size=128,
                           callbacks=callbacks_list)

            self.produce_text(num_chars=500)

    def produce_text(self, num_chars):
        rand_index = np.random.randint(0, len(self.text_obj.X))
        pattern = self.text_obj.X[rand_index]
        full_string = [self.text_obj.n_char[i] for i in pattern]

        for _ in range(num_chars):
            x = pattern[-self.text_obj.seq_length:]  # grab the last seq_length chars as input
            x = np.reshape(x, (1, self.text_obj.seq_length, 1))  # reshape for model
            x = x / float(len(self.text_obj.n_char))  # use the normalization function
            char_probs = self.model.predict(x, verbose=0).astype('float64')[0]  # get the probs from the model
            result = self.get_next_char(char_probs)  # get the most likely char from results
            pattern = np.append(pattern, result)  # add it to the string
            full_string.append(self.text_obj.n_char[result])
        print("\"", ''.join(full_string), "\"")

    def get_next_char(self, char_probs):
        # char_probs = np.log(char_probs) / self.temp
        # exp_preds = np.exp(char_probs)
        # preds = exp_preds / np.sum(exp_preds)
        # probs = np.random.multinomial(1, preds, 1)
        result = np.argmax(char_probs)
        return result


if __name__ == "__main__":
    text = TextGenChar("data/gutenberg.txt", percent_text=1)
    text.load_text()
    text.pre_processsing()
    model = TextGenModel(text_obj=text, model_dir="three_musk_model/", temp=0.2)
    model.build_model()
    model.train_model()
