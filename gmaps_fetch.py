'''
Given a set of place names, queries the gmaps api and Appends:
    - gmaps place id (GPID)
    - Lat/long data
    - user review rating
To be passed to the cleaner for data cleaning
'''

import pandas as pd
import requests
import googlemaps
import json
import os

# setup gmaps object
gmaps = googlemaps.Client(key='AIzaSyBrY7HAvOgb8NHhW-mir7CQERHER8saC28')
mel_loc = (-37.8132, 144.965)  # centre of search radius
folder = 'test_data'
infile = 'locations.csv'
outfile = 'locations_add_data.csv'

# read in test locations TODO replace with
dfLoc = pd.read_csv(os.path.join(folder, infile), encoding='UTF-8')
locs = dfLoc.Name  # col containing place names

def cacheGmapLocationData(dfLoc):
    """ Cache results so don't need to keep hitting the gmaps API
    """
    place_search_cache = []
    # for loc in locs[0:3]:  # testing limited search only
    for loc in locs:
        print('search:', loc)
        place = gmaps.places(loc, mel_loc, radius=10000)  # place search api
        print('found:', place['results'][0]['name'])
        place_search_cache.append(place)
    return place_search_cache

def extractLocDataFromCache(place_search_cache):
    """ don't need the gmaps.place() api yet - see test filefor details
    """
    gpid_l, lat_l, lng_l, rating_l = [], [], [], []
    for place in place_search_cache:
        lng_l.extend([place['results'][0]['geometry']['location']['lat']])  # how to access lat
        lat_l.extend([place['results'][0]['geometry']['location']['lng']])  # and long
        gpid_l.extend([place['results'][0]['place_id']])
        try:
            rating_l.extend([place['results'][0]['rating']])
        except KeyError:  # possible some places don't have ratings
            rating_l.append(None)
            print('no rating found for {}'.format(place['results'][0]['name']))
    print(len(gpid_l), len(lat_l), len(lng_l), len(rating_l))
    return gpid_l, lat_l, lng_l, rating_l


place_search_cache = cacheGmapLocationData(dfLoc)
gpid_l, lat_l, lng_l, rating_l = extractLocDataFromCache(place_search_cache)
# add extensions to df
dfLoc['gpid'] = gpid_l
dfLoc['lat'] = lat_l
dfLoc['lng'] = lng_l
dfLoc['rating'] = rating_l

# Save as csv
dfLoc.to_csv(os.path.join(folder, outfile), index=False)