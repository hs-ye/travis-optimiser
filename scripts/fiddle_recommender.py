'''Testing the recommender
# Get ids from gmaps, for two places

# App: Check midpoint between two points
# Search around radius for options against known list of places (can think about KD Tree to speed up later)
# sort by rating criteria weights
    # Dist
    Rating
    Similar to profile, which needs to be manually loaded

'''

import pandas as pd
import requests
import googlemaps
import json
from datetime import datetime
from utils.utilities import haversineVectDist

# test google place ids
id1 = 'ChIJczgQh8lC1moR9r9gP44FRvY'  # Chinatown Melbourne 墨尔本唐人街
id1 = 'ChIJ9RT5wLRC1moRpIkhaxraJMc'  # mckillops lane
id2 = 'ChIJdedaLk5d1moRQOX0CXZWBB0'  # Spencer Street Station

dfLoc = pd.read_csv('travis_optimiser/test_data/locations_add_data.csv', encoding='UTF-8')
gmaps = googlemaps.Client(key='AIzaSyBrY7HAvOgb8NHhW-mir7CQERHER8saC28')

dfLoc = dfLoc[dfLoc.Category.str.lower()=='eat']

place1 = gmaps.place(place_id=id1)
place2 = gmaps.place(place_id=id2)

place1.keys()
place1['result']['geometry']['location']
lat = place1['result']['geometry']['location']['lat']
lng = place1['result']['geometry']['location']['lng']

lat2 = place2['result']['geometry']['location']['lat']
lng2 = place2['result']['geometry']['location']['lng']

lat_mid = (lat + lat2) / 2
lng_mid = (lng + lng2) / 2

dist = haversineVectDist(lat_mid, lng_mid, dfLoc.lat.to_numpy(), dfLoc.lng.to_numpy())
dfRecommend = dfLoc[dist < 300]  # 300m walking distance

dfRecommend.head(5).sort_values('rating', ascending=False, inplace=True)
dfRecommend.gpid
lat_mid, lng_mid

# Testing for the places_nearby search
target_lat_lon = (-37.82347, 144.970761)  # south melb near NGV
new_places = gmaps.places_nearby(location=target_lat_lon, radius=500, type='restaurant')
new_places = gmaps.places_nearby(location=target_lat_lon, radius=500, type='restaurant', rank_by='prominence')
new_places['results']
new_places['results'][0]
len(new_places['results'])  # 13 results
[(_['name'], _['geometry']['location']) for _ in new_places['results']]

test = [(
        _['name'], 
        _['geometry']['location']['lat'],
        _['geometry']['location']['lng'],
        _['place_id'],
        _['rating'],  # this will throw keyerror as not all places have a rating
        # _['user_ratings_total'],
        # _['price_level'],
        _['vicinity']
    ) for _ in new_places['results']]

pd.DataFrame(test)

test = []
for _ in new_places['results']:
    name = _['name']
    lat = _['geometry']['location']['lat']
    lng = _['geometry']['location']['lng']
    place_id = _['place_id']
    try:
        rating = _['rating']
        user_ratings_total = _['user_ratings_total']
    except KeyError:
        rating = None
        user_ratings_total = 0
    
    try:
        price_level = _['price_level']
    except KeyError:
        price_level = None
    address = _['vicinity']
    test.append([name, lat, lng, place_id, rating, user_ratings_total, price_level, address,])

pd.DataFrame(test,
    columns=["name", "lat", "lng", "place_id", "rating", "user_ratings_total", "price_level", "address",])


