import argparse
from time import time
from flickr_scraper import main, query
from emailer import build_message
from produce_text import make_poem

parser = argparse.ArgumentParser()

parser.add_argument("-to", "--to_name", help="Person to send email to")
parser.add_argument("-from", "--from_name", help="Your name")
parser.add_argument("-to_email", "--to_email",
                    help="Email you want to send it to")
args = parser.parse_args()

poem = make_poem('weights/weights_9_10_perc_words.hdf5')
tags = query()
img = main(tags)


with open('gmail.csv') as gmail:
    creds = gmail.read().split(', ')
    from_email = creds[0]
    from_password = creds[1]

build_message(args.to_name, args.from_name,
              from_email, from_password,
              args.to_email, poem,
              img)
