import pandas as pd
import numpy as np

def load_and_clean():
    # open the file containing all poems. from a kaggle download
    poems = pd.read_csv('data/all_poems.csv')

    # filter it to just poems that are of type 'Love'
    love_poems = poems[poems['type'] == 'Love']
    love_poems = love_poems[love_poems['age'] == 'Modern']['content']
    # also lowercases the string.
    # there's a lot of old timey words in here, I might end up trying to stem the
    # words in the string, we'll see how everything turns out

    lp = '\n'.join(love_poems.values.tolist()).lower()

    # save string to txt file
    with open("data/cleanedpoems.txt", "w") as text_file:
        text_file.write(lp)

if __name__ == "__main__":
    load_and_clean()
