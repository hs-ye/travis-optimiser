import pandas as pd
import numpy as np
import os
from utils.utilities import get_cfg


"""
Module for Management of the backend data needed for the recommender
"""

class RecData:
    def __init__(self):
        self.cfg = get_cfg()

    def get_df_loc(self, cfg, method='local'):
        """
        obtains the recommender data as a dataframe, used for getting the current
        copy of the data
        method: local or gcp
        returns: DataFrame of location data avaliable
        """
        if method == 'local':
            dfLoc = load_data_from_local(cfg)
        elif method == 'gcp':
            dfLoc = load_data_from_gcp_cloud(cfg)
        else:
            print(f'error - non supported method: {method}')
        return dfLoc

    def update_poi_data(self, update_data, method='local'):
        """
        inputs:
            update_data: pd Dataframe
        Updates the existing data of POIs used by recommender, depending on the option used
        """
        if method == 'local':
            dfLoc = update_data_to_local()
        elif method == 'gcp':
            dfLoc = update_data_to_gcp()
        
        print('POI data in {} updated'.format(method))

    def load_data_from_local(self, cfg):
        # read data
        # 
        module = cfg['data_local']['module']
        folder = cfg['data_local']['folder']
        folder = os.path.join(module, folder)  #  universal
        # folder = 'travis_optimiser\\test_data'  #  PC
        # folder = 'travis_optimiser/test_data'  # MAC
        outfile = 'locations_recommender.csv'
        dfLoc = pd.read_csv(os.path.join(folder, outfile), encoding='UTF-8')
        return dfLoc

    def load_data_from_gcp_cloud(self, cfg):
        bucket = cfg['data_gcp']['bucket']
        folder = cfg['data_gcp']['folder']
        file = cfg['data_gcp']['data_file']
        path = os.path.join(bucket, folder, file)  # folderpaths are in unix
        # blob = bucket.blob(bucket_folder + file)
        # filename = blob.name.split('/')[-1]
        # local_folder = "scripts"
        # dl_path = os.path.join(local_folder, filename)
        # blob.download_to_filename(dl_path)

        dl_path = 'gs://'+ path
        dfLoc = pd.read_csv(dl_path, encoding='UTF-8')
        print(f'{file} downloaded from ' + f'{bucket}.')
        return dfLoc

    def update_data_to_local(self, ):
        pass

    def update_data_to_gcp(self, ):
        pass
