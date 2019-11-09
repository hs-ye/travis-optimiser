import pandas as pd
import numpy as np
import os


"""
Module for Management of the backend data needed for the recommender
"""

def get_df_loc(method='local'):
    """
    obtains the recommender data as a dataframe, used for getting the current
    copy of the data
    TODO Alternate options, e.g. getting from S3 or GCP cloud store
    returns: DataFrame of location data avaliable
    """
    if method == 'local':
        dfLoc = load_data_from_local()
    # TODO Implement alternative options
    return dfLoc


def update_poi_data(update_data, method='local'):
    """
    Updates the existing data of POIs used by recommender, depending on the option used
    """
    if method == 'local':
        dfLoc = update_data_to_local()
    
    print('POI data in {} updated'.format(method))

def load_data_from_local():
    # read data
    # 
    folder = 'travis_optimiser\\test_data'  #  PC
    # folder = 'travis_optimiser/test_data'  # MAC
    outfile = 'locations_recommender.csv'
    dfLoc = pd.read_csv(os.path.join(folder, outfile), encoding='UTF-8')
    return dfLoc

def load_data_from_gcp_cloud():
    # To be implemented, when moving data to the cloud
    pass

def update_data_to_local():
    pass
