import pandas as pd
import numpy as np
import os


"""
Module for Management of the backend data needed for the recommender
"""


def get_df_loc(cfg, method='local'):
    """
    obtains the recommender data as a dataframe, used for getting the current
    copy of the data
    method: local or gcp
    returns: DataFrame of location data avaliable
    """
    if method == 'local':
        dfLoc = load_data_from_local()
    elif method == 'gcp':
        dfLoc = load_data_from_gcp_cloud(cfg)
    else:
        print(f'error - non supported method: {method}')
    return dfLoc

def update_poi_data(update_data, method='local'):
    """
    TODO WIP function
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

def load_data_from_gcp_cloud(cfg):
    # TODO Remove hardcoding of data being read and paths
    bucket_folder = 'travis_recommender/csv_data/'  # folderpaths are in unix
    file = "locations_recommender.csv"
    # blob = bucket.blob(bucket_folder + file)
    # filename = blob.name.split('/')[-1]
    # local_folder = "scripts"
    # dl_path = os.path.join(local_folder, filename)
    # blob.download_to_filename(dl_path)
    # print(f'{filename} downloaded from bucket.')

    dl_path = 'gs://'+ bucket_folder + file
    dfLoc = pd.read_csv(dl_path, encoding='UTF-8')
    return dfLoc

def update_data_to_local():
    pass

