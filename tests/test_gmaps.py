'''
Given a set of inputs, e.g. place names
Gets required data from the google maps API
To be passed to the cleaner for data cleaning
'''

import pandas as pd
import requests
import googlemaps
import json
from datetime import datetime

import pympler  # for testing size of objects in memory
from pympler import asizeof

dfLoc = pd.read_csv('travis_optimiser/test_data/locations.csv', encoding='UTF-8')
locs = dfLoc.name
# setup gmaps object
gmaps = googlemaps.Client(key='AIzaSyBrY7HAvOgb8NHhW-mir7CQERHER8saC28')

""" EXAMPLES - check package details for full methods
It is just a wrapper around making requests to the http api endpoint
# Geocoding an address
geocode_result = gmaps.geocode('1600 Amphitheatre Parkway, Mountain View, CA')
geocode_result  # gives a lot more data than what we need
"""
mel_loc = (-37.8132, 144.9)
gtest = gmaps.places('chinatown melbourne', mel_loc, radius=10000)

gtest.keys()
len(gtest['results'])
gtest['results'][0]
gtest['results'][0].keys()
# dict_keys(['formatted_address', 'geometry', 'icon', 'name', 'opening_hours', 
# 'photos', 'place_id', 'plus_code', 'rating', 'reference', 'types', 
# 'user_ratings_total'])
gtest['results'][0]['rating'] 
gtest['results'][0]['geometry']['location']
gtest['results'][0]['geometry']['location']['lat']  # how to access lat
gtest['results'][0]['geometry']['location']['lng']  # and long

gtest['results'][0]['id']  # not sure what this is
gtest['results'][0]['place_id']  # this is the correct one
loc_pid = gtest['results'][0]['place_id']  # this is the correct one

# use pid to get place details
locDetail = gmaps.place(loc_pid)
locDetail.keys()
locDetail['result']
locDetail['result'].keys()
# dict_keys(['address_components', 'adr_address', 'formatted_address', 
#   'geometry', 'icon', 'id', 'name', 'opening_hours', 'photos', 
#   'place_id', 'plus_code', 'rating', 'reference', 'reviews', 'scope', 
#   'types', 'url', 'user_ratings_total', 'utc_offset', 'vicinity', 'website'])

# probably don't actually need any of these for the slotter


for loc in locs:
    print(loc)

pympler.asizeof.asizeof(place_search_cache)

# Save as csv

# dfLoc.to_csv('test_data/locations_encoded.csv', index=False)
