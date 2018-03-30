
#!/usr/bin/env python
""" Script to scrape images from a flickr account.
Author: Ralph Bean <rbean@redhat.com>
"""

# import ConfigParser
import urllib
import requests
import os, errno
import time

# Get config secrets from a file
# config = ConfigParser.ConfigParser()
# config.read(['flickr.ini', '/etc/flickr.ini'])
# flickr_api_key = config.get('general', 'flickr_api_key')

# API urls
flickr_url = 'https://api.flickr.com/services/rest/'


def flickr_request(**kwargs):
    response = requests.get(flickr_url, params=dict(
        api_key=api_key,
        format='json',
        nojsoncallback=1,
        **kwargs))
    return response.json()


def get_flickr_page(tags, page=1):
    return flickr_request(
        method='flickr.photos.search',
        tags=tags,
        tag_mode='any',
        content_type=1,  # photos only
        page=page,
        per_page=500)


def get_photos_for_person(tags):

    pages = get_flickr_page(tags)['photos']['pages']

    seen = {}
    # Step backwards through the pictures

    for page in range(pages, 1, -1):
        d = get_flickr_page(tags, page=page)
        for photo in d['photos']['photo']:
            yield photo

def main(tags, animal):

    #nsid = raw_input("NSID of the flickr user you want to scrape: ")

    # First get all photos
    # https://secure.flickr.com/services/api/flickr.people.getPhotos.html

    photos = get_photos_for_person(tags)


    # Then, with photo objects, get the images
    # https://secure.flickr.com/services/api/misc.urls.html
    # Each of these photo objects looks something like this
    # {u'farm': 8,
    #  u'id': u'13606821584',
    #  u'isfamily': 0,
    #  u'isfriend': 0,
    #  u'ispublic': 1,
    #  u'owner': u'65490292@N04',
    #  u'secret': u'c5bfa5eb3e',
    #  u'server': u'7171',
    #  u'title': u''}
    output = 'flickr/' + str(animal+'/')

    try:
        os.makedirs(output)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise

    prefix = "http://farm{farm}.staticflickr.com/{server}/"
    suffix = "{id}_{secret}_b.jpg"
    template = prefix + suffix

    for i, photo in enumerate(photos):
        if i == 3601:
            break
        url = template.format(**photo)
        index = "%0.6i" % i
        local = output + index + "-" + suffix.format(**photo)
        # print("* saving", url)
        urllib.request.urlretrieve(url, local)
        # print("      as", local)

def make_animals():
    #dictionary of different animal names and associated tags
    animals = {'mule_deer': ['mule deer'],
               'bobcat': ['bobcat'],
               'mountain_lion': ['mountain lion', 'cougar'],
               'coyote': ['coyote'],
               'elk': ['elk'],
               'ermine': ['ermine'],
               'human': ['human'],
               'lynx': ['lynx'],
               'marten': ['marten'],
               'moose': ['moose'],
               'porcupine': ['porcupine'],
               'ptargmigan': ['ptarmigan', 'Lagopus muta'],
               'red_fox': ['red fox'],
               'red_squirrel': ['red squirrel'],
               'snowshoe_hare': ['snowshoe hare', 'Lepus americanus'],
               'bear': ['bear','black bear','grizzly bear','grizzly'],
               'bird': ['bird'],
               'mountain_goat': ['mountain goat'],
               'marmot': ['marmot'],
               'bighorn_sheep': ['bighorn sheep'],
               'racoon': ['racoon', 'trash panda'],
               'dog': ['dog', 'puppy'],
               'chipmunk': ['chipmunk'],
               'cow': ['cow'],
               'horse': ['horse'],
               'domestic_sheep': ['sheep', 'domestic sheep'],
               'turkey': ['turkey'],
               'gray_jay': ['gray jay', 'grey jay', 'Canada jay',
                            'whisky jack', 'Perisoreus canadensis'],
               'dusky_grouse': ['dusky grouse', 'sooty grouse',
                                 'blue grouse', 'Dendragapus obscurus'],
               'mouse': ['mouse'],
               'bat': ['bat'],
               'striped_skunk': ['striped_skunk', 'skunk'],
               'house_wren': ['house wren', 'Troglodytes aedon', 'wren'],
               'stellars_jay': ['stellars jay', 'blue jay', 'long-crested jay', 'mountain jay',
                                 'pine jay'],
               'junco': ['junco', 'dark eyed junco', 'dark-eyed junco', 'Junco hyemalis'],
               'badger': ['badger'],
               'butterfly': ['butterfly'],
               'hawk': ['hawk', 'red tail hawk', 'red tailed hawk'],
               'magpie': ['magpie'],
               'mule': ['mule'],
               'prarie_dog': ['prarie dog'],
               'pronghorn': ['pronghorn', 'Antilocapra americana', 'antelope'],
               'rabbit': ['rabbit', 'bunny'],
               'raven': ['raven'],
               'sage_grouse': [' Centrocercus urophasianus', 'sage grouse', 'greater sage grouse']}
    return animals

if __name__ == '__main__':
    animals = make_animals()

    for animal, tags in animals.items():
        if animal not in ['badger', 'bat', 'bear', 'bighorn_sheep',
                          'bird', 'bobcat', 'butterfly','chipmunk',
                          'cow','coyote','dog', 'elk',
                          'ermine', 'gray_jay','hawk','horse',
                          'house_wren','human','junco', 'lynx','magpie',
                          'marmot','marten',
                          'moose','mountain_goat','mountain_lion','mouse','mule',
                          'mule_deer','porcupine','ptarmigan','racoon','red_fox',
                          'red_squirrel','snowshoe_hare','stellars_jay','striped_skunk',
                          'turkey'
                          ]:
            print(animal)
            toc = time.time()
            main(tags, animal)
            print(time.time() - toc)
            print()














#
