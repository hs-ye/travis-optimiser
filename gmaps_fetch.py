'''
Given a set of place names, queries the gmaps api and Appends:
    - gmaps place id (GPID)
    - Lat/long data
    - user review rating
To be passed to the cleaner for data cleaning
'''

import pandas as pd
import numpy as np
import requests
import googlemaps
import json
import os
import pickle

# setup gmaps object
gmaps = googlemaps.Client(key='AIzaSyBrY7HAvOgb8NHhW-mir7CQERHER8saC28')
mel_loc = (-37.8132, 144.965)  # centre of search radius
folder = 'test_data'
infile = 'locations.csv'
pickfile = 'gmaps_cache.pickle'
outfile = 'locations_add_data.csv'

# read in test locations TODO replace with
dfLoc = pd.read_csv(os.path.join(folder, infile), encoding='UTF-8')
locs = dfLoc.Name  # col containing place names

def fetchGmapLocationData(dfLoc):
    """ fetch results, should cache to avoid hitting the API
    """
    place_search_cache = []
    # for loc in locs[0:3]:  # testing limited search only
    for loc in locs:
        print('search:', loc)
        place = gmaps.places(loc, mel_loc, radius=10000)  # place search api
        print('found:', place['results'][0]['name'])
        place_search_cache.append(place)
    return place_search_cache


def getGmapLocationData(dfLoc, pickfile="gmaps_cache.pickle"):
    """ Try to get data from Pickle file, ignores dfLoc input
    if not, then fetch and make pickle from gmaps API"""
    # if os.path.getsize(pickfile):  # check pickle file not empty
    if os.path.isfile(pickfile):  # check pickle file exists
        print('looks like gmaps data already exists. Try loading')
        try:
            infile = open(pickfile,'rb')
            gmap_data = pickle.load(infile)
            print('gmaps data loaded from pickle')
        except:
            print('could not load pickle data')
        else:
            infile.close()
    else:
        print('no data found - re-download data')
        try:
            outfile = open(pickfile,'wb')
            gmap_data = fetchGmapLocationData(dfLoc)
            pickle.dump(gmap_data, outfile)
            print('gmap data downloaded and saved')
        except:
            print('error saving gmaps data as pickle')
        else:
            outfile.close()
    return gmap_data


def extractLocDataFromCache(place_search_cache):
    """ don't need the gmaps.place() api yet - see test filefor details
    """
    gpid_l, lat_l, lng_l, rating_l = [], [], [], []
    for place in place_search_cache:
        lng_l.extend([place['results'][0]['geometry']['location']['lng']])  # how to access lat
        lat_l.extend([place['results'][0]['geometry']['location']['lat']])  # and long
        gpid_l.extend([place['results'][0]['place_id']])
        try:
            rating_l.extend([place['results'][0]['rating']])
        except KeyError:  # possible some places don't have ratings
            rating_l.append(None)
            print('no rating found for {}'.format(place['results'][0]['name']))
    print(len(gpid_l), len(lat_l), len(lng_l), len(rating_l))
    return gpid_l, lat_l, lng_l, rating_l


place_search_cache = getGmapLocationData(dfLoc)
gpid_l, lat_l, lng_l, rating_l = extractLocDataFromCache(place_search_cache)
# add extensions to df
dfLoc['gpid'] = gpid_l
dfLoc['lat'] = lat_l
dfLoc['lng'] = lng_l
dfLoc['rating'] = rating_l

# Save as csv to folder
dfLoc.to_csv(os.path.join(folder, outfile), index=False)