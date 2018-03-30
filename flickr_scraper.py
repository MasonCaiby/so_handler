
#!/usr/bin/env python
"""
I save my flickr api keys in a txt file in the directory this repo
is saved to. I then read it in. You only need the first key, apparently.
To use this script out of box, save your key to flickr_key.txt as a csv with
a space between the two keys (not secret key second)

I used a lot of code from:
Script to scrape images from a flickr account.
Author: Ralph Bean <rbean@redhat.com>
https://gist.github.com/ralphbean/9966896
"""

# import ConfigParser
import urllib
import requests
import os
import errno
import time
from random import randint
from itertools import islice


# API urls
flickr_url = 'https://api.flickr.com/services/rest/'

# APIKey loader
with open('flickr_key.txt', 'r') as f:
    APIKey = f.readline().split(', ')[0]

def flickr_request(APIKey, **kwargs):
    '''DOCSTRING
       This just generates a Flickr API client
       It returns the client as a json
    '''
    response = requests.get(flickr_url, params=dict(
        api_key=APIKey,
        format='json',
        nojsoncallback=1,
        **kwargs))
    return response.json()


def get_flickr_page(tags, page=1, perpage=500):
    '''DOCSTRING
       This generates a request to flickr and returns it
       You can change the other kwargs, but I never needed to
       Since I'm shooting for as many photos as I can get I set
       the per_page to the max (500). I will pull a random photo from
       one of the tags I load, then check to make sure it hasn't sent before.
       Content type toggles what the request will return.
       tag_mode can be set to 'all' for an AND join
       ----------
       INPUTS:
       tags: comma seperated list of tags you want to search for
       page: the page # you want to return
       perpage: number of photos you want per page
       ----------
       RETURNS:
       the request
    '''
    return flickr_request(APIKey,
        method='flickr.photos.search',
        tags=tags,
        tag_mode='any',
        content_type=1,  # photos only
        page=page,
        per_page=perpage)


def get_photos_for_person(tags):
    '''DOCSTRING
       This bad boy right here pulls the photos from the
       pages the request returns. It steps through the
       pages froms last to first, from what I can tell
       the last page returned by get_flickr_page is
       actually the first page returned by a query.
       ------------
       INPUTS:
       tags: [comma, seperated, list] of search tags
       ------------
       RETURNS:
       None
    '''
    pages = get_flickr_page(tags)['photos']['pages']

    # Step backwards through the pictures
    d = get_flickr_page(tags, page=pages)
    for photo in d['photos']['photo']:
        yield photo

def main(tags):
    '''DOCSTRING
       This is pretty much straight from Ralph Bean's repo.
       This is what actually pulls the images and saves them to
       the 'flickr/$animal/_____.jpg' directory.

       FLOW:
       make photos variable by calling get_photos_for_person
       which actually just feeds its arguments to get_flickr_page
       and loops through the pages to pull out the phote and
       actually just feeds its arguments to get_flickr_request
       It then saves the images to the hard-coded folder location
       'flickr/$animal/_____.jpg'. I limited it 3601 photos.
       ---------
       INPUT:
       tags: the tags to query flickr for
       animal: the name of the animal you are querying for
       ---------
       RETURNS:
       None
    '''
    # First get all photos
    # https://secure.flickr.com/services/api/flickr.people.getPhotos.html

    photos = get_photos_for_person(tags)
    url, local = get_new_photo(photos, 0)

    output = '/'.join(local.split('/')[:-1])
    try:
        os.makedirs(output)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise

    urllib.request.urlretrieve(url, local)

    full_path = os.path.abspath(local)
    return full_path

def get_new_photo(photos, i):
    '''
        https://secure.flickr.com/services/api/misc.urls.html
        Each of these photo objects looks something like this
        {u'farm': 8,
         u'id': u'13606821584',
         u'isfamily': 0,
         u'isfriend': 0,
         u'ispublic': 1,
         u'owner': u'65490292@N04',
         u'secret': u'c5bfa5eb3e',
         u'server': u'7171',
         u'title': u''}
    '''
    photo  = next(islice(photos, i, None))
    prefix = "http://farm{farm}.staticflickr.com/{server}/"
    suffix = "{id}_{secret}_b.jpg"
    local = 'flickr/' + suffix.format(**photo)
    template = prefix + suffix
    url = template.format(**photo)
    if os.path.isfile(local):
        url, local = get_new_photo(photos, i + 1)
    return url, local

def query():
    '''DOCSRING
       could eventually build this out so that it queries a
       DB for a specific person to get the images they want to query.
       Currently, it's just dogs my girlfriend likes, because she's
       the most important
       ----------
       INPUTS:
       None
       __________
       Returns:
       tags: comma seperated list of dogs and things
    '''
    return ['puppy', 'pitbull', 'boxer', 'husky', 'malamute',
            'german shepherd', 'border collie']

if __name__ == '__main__':
    tags = query()
    toc = time.time()
    print(main(tags))















#
