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
id1 = 'ChIJ9RT5wLRC1moRpIkhaxraJMc'  # ??
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