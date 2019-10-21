# recommender engine
'''
Content based recommender  v1
Sets up the recommender model to rank list of places, to be used by the predictor

This model doesn't require any of the ML libraries, pure content matrix content
'''

import pandas as pd
import numpy as np
import googlemaps
from utils import utilities
# -- # pre-processing & pipelines
# from sklearn.decomposition import PCA, KernelPCA
# from sklearn.pipeline import Pipeline
# from sklearn.preprocessing import Imputer, LabelEncoder, StandardScaler
# # -- # model building
# from sklearn.linear_model import LinearRegression, LogisticRegression, Lasso
# # -- # scoring & validation
# from sklearn.metrics import mean_squared_log_error as msle


""" Model purpose
Using an input matrix of 3 chosen locations, rank all possible location vectors

1. Define input data matrix (assume clean data already)
2. Set up model params 

"""

# -- # Testing data input
# pd.read_csv()

def getGmaps(key='AIzaSyBrY7HAvOgb8NHhW-mir7CQERHER8saC28'):
    gmaps = googlemaps.Client(key=key)
    return gmaps

def getBestRec():
    ''' generic recommender controller function to handle various scenarios
    e.g.:
        - no items in location on the list
        - not enough items on the list (should be 5, or some other number)
        - expanding the search radius and seeing how far away it is
        - calling the google api to get a 'new' item
        - saving new items to the list 
    '''
    pass


def recFromList(gmaps, id1, id2, dfLoc, rectype='eat', reclimit=5,radius=500):
    """ Given 2 google ids, works out where to perform a search, and does so in a radius
    Searches a pre-defined list of places

    TODO: see getBestRec function
    """

    dfLoc = dfLoc[dfLoc.Category.str.lower()==rectype]  # filter for lower only

    place1 = gmaps.place(place_id=id1)
    place2 = gmaps.place(place_id=id2)

    lat = place1['result']['geometry']['location']['lat']
    lng = place1['result']['geometry']['location']['lng']

    lat2 = place2['result']['geometry']['location']['lat']
    lng2 = place2['result']['geometry']['location']['lng']

    lat_mid = (lat + lat2) / 2
    lng_mid = (lng + lng2) / 2

    dist = utilities.haversineVectDist(lat_mid, lng_mid, 
        dfLoc.lat.to_numpy(), dfLoc.lng.to_numpy())
    dfRec = dfLoc[dist < radius]  # 300m walking distance

    dfRec.head(reclimit).sort_values('rating', ascending=False, inplace=True)

    return dfRec.gpid  # gets the top 5 ids


def recFromLoc(id1, id2, radius):
    """ Given 2 google ids, works out where to perform a search, and does so in a radius
    """
    pass


def getGooglePlaceID(gmaps, search_string):
    '''
    '''
    pass

