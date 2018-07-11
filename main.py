import argparse, os
import flickr_scraper
from time import time
from emailer import build_message
from produce_text import make_poem
from notifier import notify

def main(to_name, from_name, to_email):
    #sends an os notification to the user
    notify("Creating and sending email", "I will notify you when I am done")

    poem = make_poem('weights_large/51--loss_1.2245.hdf5')
    tags = flickr_scraper.query()
    img = flickr_scraper.main(tags)


    with open('gmail.csv') as gmail:
        creds = gmail.read().split(', ')
        from_email = creds[0]
        from_password = creds[1]

    build_message(to_name, from_name,
                  from_email, from_password,
                  to_email, poem,
                  img)

    os.remove(img)

    #sends an os notification to the user
    notify("Email Sent", "recipient = {}".format(to_email))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument("-to_name", "--to_name", help="Person to send email to")
    parser.add_argument("-from", "--from_name", help="Your name")
    parser.add_argument("-to_email", "--to_email",
                        help="Email you want to send it to")
    args = parser.parse_args()

    main(args.to_name, args.from_name, args.to_email)
