from flickr_scraper import main, query
from emailer import build_message
from produce_text import make_poem

tags = query()
img = main(tags)
poem = make_poem()

with open('gmail.csv') as gmail:
    creds = gmail.read().split(', ')
    from_email = creds[0]
    from_password = creds[1]
build_message('Marissa', 'Max', from_email, from_password,
                  'maxwell.caudle@gmail.com', poem, img)
