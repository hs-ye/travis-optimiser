# recommender engine
'''
Content based recommender  v1
Sets up the recommender model to rank list of places, to be used by the predictor

This model doesn't require any of the ML libraries, pure content matrix approach
'''

import pandas as pd
import numpy as np
import googlemaps
import os
from google.cloud import storage
from utils import utilities
from typing import List, Tuple, Dict
from travis_optimiser.recommender_data import get_df_loc, update_poi_data 
# -- # pre-processing & pipelines
# from sklearn.decomposition import PCA, KernelPCA
# from sklearn.pipeline import Pipeline
# from sklearn.preprocessing import Imputer, LabelEncoder, StandardScaler
# # -- # model building
# from sklearn.linear_model import LinearRegression, LogisticRegression, Lasso
# # -- # scoring & validation
# from sklearn.metrics import mean_squared_log_error as msle

cfg = utilities.get_cfg()
json_keyfile = cfg['data_gcp']['json_key']
bucket_name = cfg['data_gcp']['bucket']
project = cfg['data_gcp']['project']
storage_client = storage.Client.from_service_account_json(json_keyfile)
bucket = storage_client.get_bucket(bucket_name)  # now it will create bucket obj

""" Model purpose
Using an input matrix of 2 chosen locations, rank all possible location vectors
1. Define input data matrix (assume clean data already)
2. Set up model params 

"""

def get_gmaps(key=cfg['google_key']):
    gmaps = googlemaps.Client(key=key)
    return gmaps

def get_best_recs(gmaps, input_gpids: List[str], rectype: str, cfg: Dict, reclimit=5,
        radius=500) -> pd.core.frame.DataFrame:
    ''' main recommender controller function, will try to return top recommendatoins
    Should handle various scenarios:
        - no items in location on the list
        - not enough items on the list (should be 5, or some other number)
        - expanding the search radius and seeing how far away it is
        - calling the google api to get a 'new' item
        - saving new items to the list 
    # TODO: Implement actual recommendation engine on top of results found
    '''
    # if isinstance(cfg, type(None)):
        # cfg = utilities.get_cfg()
    dfLoc = get_df_loc(cfg=cfg, method=cfg['backend'],)  # get the list of existing POIs known to the recommender
    num_locations = len(input_gpids)
    if num_locations == 1:    
        target_lat_lon = utilities.get_latlong_from_gpid(gmaps, input_gpids[0])
    
    elif num_locations == 2:
        target_lat_lon = utilities.calc_midpoint_of_gpids(gmaps, input_gpids)

    rec_results = rec_search_list_at_latlon(dfLoc, target_lat_lon, rectype='eat')  # NOTE: rectype for searching at list is different for searching at latlon

    num_new = 5 - len(rec_results)
    if num_new > 0:
        new_results = rec_search_gmaps_at_latlon(gmaps, target_lat_lon, rectype='restaurant')
        rec_results = append_and_update_new_poi_results(rec_results, new_results, num_new)
    
    return rec_results

def append_and_update_new_poi_results(rec_results, new_results, n_results: int) -> pd.core.frame.DataFrame:
    """ Performs cleaning then combines the results from existing and new
    adds any new search results to db as required
    inputs: 
        rec_result is a series
        new_results is a dataframe
    outputs: a pd series, for consistency
    # TODO: 
        # set operation to remove existing gpids
        # re-ranking of new options (i.e. based on 'real' recommender, in future)
        # add the new ones to the old ones, save to DF
        # return to the main list
    """
    new_results = new_results.head(n_results)
    cleaned_new_results = new_results.gpid
    update_poi_data(cleaned_new_results, method=cfg['backend'])
    results = pd.concat([rec_results, cleaned_new_results])
    return results

def rec_search_list_at_latlon(dfLoc, target_lat_lon: Tuple[float], rectype: str,
        reclimit=5, radius=500) -> pd.core.series.Series:
    """ Searches existing list for items
    returns: pd series of gpids only
    """
    dfLoc = dfLoc[dfLoc.Category.str.lower()==rectype]  # filter for lower only
    
    lat, lon = target_lat_lon
    # note we are relying on numpy broadcasting for the following vector calc to work
    dist = utilities.haversineVectDist(lat, lon, dfLoc.lat.to_numpy(), dfLoc.lng.to_numpy())
    
    dfRec = dfLoc[dist < radius]
    # gets the top 5 ids, sorts them by rating
    dfRec.head(reclimit).sort_values('rating', ascending=False, inplace=True)
    print(dfRec.name)
    return dfRec.gpid

def rec_search_gmaps_at_latlon(gmaps, target_lat_lon: Tuple[float], rectype: str, reclimit=5, 
        radius=500) -> pd.core.frame.DataFrame:
    """
    Searches google maps for avaliable places at the following
    Note rectype must be "restaurant" in googlemaps, see https://developers.google.com/places/supported_types
    """
    new_places = gmaps.places_nearby(location=target_lat_lon, radius=radius, type='restaurant',
            rank_by='prominence')  # note that 'prominence' is a google term for popularity
    dfNewplaces = convert_gmaps_search_result_string_to_df(new_places)
    dfNewplaces.sort_values('rating', ascending=False, inplace=True)
    return dfNewplaces

def convert_gmaps_search_result_string_to_df(result_string: str) -> pd.core.frame.DataFrame:
    results = []
    for _ in result_string['results']:
        name = _['name']
        lat = _['geometry']['location']['lat']
        lng = _['geometry']['location']['lng']
        place_id = _['place_id']
        try:  # not all places have a rating
            rating = _['rating']
            user_ratings_total = _['user_ratings_total']
        except KeyError:
            rating = None
            user_ratings_total = 0
        try:  # not all places have price-level info
            price_level = _['price_level']
        except KeyError:
            price_level = None
        address = _['vicinity']
        results.append([name, lat, lng, place_id, rating, user_ratings_total, price_level, address,])

    dfResults = pd.DataFrame(results,
        columns=["name", "lat", "lng", "gpid", "rating", "user_ratings_total", "price_level", "address",])
    return dfResults


if __name__ == "__main__":
    # test_get_best_recs()
    # test_search_at_latlon()
    pass