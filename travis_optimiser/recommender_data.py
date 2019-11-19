import pandas as pd
import numpy as np
import os
import gcsfs

from google.cloud import storage
from utils.utilities import get_cfg


"""
Module for Management of the backend data needed for the recommender
"""

class RecData:

    def __init__(self, cfg_file="config.yml"):
        self.cfg = get_cfg(cfg_file)
        self.method = self.cfg['backend']
        # setup cloud drive if needed
        if self.method == 'gcp':
            gs_token = self.cfg['data_gcp']['json_key'] if self.cfg['gcp_local_auth'] == 1 else None
            self.gcs_fs = gcsfs.GCSFileSystem(project='my-project', token=gs_token)
        self.dfLoc = None  # placeholder for existing data, but doesn't add it yet
        self.dfNew = None  # placeholder for new data coming in


        # not needed - manual way of connecting to gcs
        # json_keyfile = self.cfg['data_gcp']['json_key']
        # bucket_name = self.cfg['data_gcp']['bucket']
        # project = self.cfg['data_gcp']['project']
        # self.storage_client = storage.Client.from_service_account_json(json_keyfile)
        # self.bucket = self.storage_client.get_bucket(bucket_name)  # now it will create bucket obj

    def get_df_loc(self) -> pd.core.frame.DataFrame:
        """
        obtains the recommender data as a dataframe, used for getting the current
        copy of the data
        method: local or gcp
        returns: DataFrame of location data avaliable
        """
        if self.method == 'local':
            dfLoc = self.load_data_from_local()
        elif self.method == 'gcp':
            dfLoc = self.load_data_from_gcp_cloud()
        else:
            raise KeyError(f'error - non supported method: {self.method}')
        
        print(f'loaded existing data from {self.method} into rec_data')
        self.dfLoc = dfLoc
        
        return dfLoc

    def load_data_from_local(self):
        # read data
        # 
        module = self.cfg['data_local']['module']
        folder = self.cfg['data_local']['folder']
        folder = os.path.join(module, folder)  #  universal
        # folder = 'travis_optimiser\\test_data'  #  PC
        # folder = 'travis_optimiser/test_data'  # MAC
        outfile = 'locations_recommender.csv'
        dfLoc = pd.read_csv(os.path.join(folder, outfile), encoding='UTF-8')
        return dfLoc

    def load_data_from_gcp_cloud(self):
        bucket = self.cfg['data_gcp']['bucket']
        folder = self.cfg['data_gcp']['folder']
        file = self.cfg['data_gcp']['data_file']

        # path = os.path.join(bucket, folder, file)  # folderpaths are in unix, this won't work if running on windows machine
        path = bucket + '/' + folder + '/' + file  # folderpaths are in unix
        # blob = bucket.blob(bucket_folder + file)
        # filename = blob.name.split('/')[-1]
        # local_folder = "scripts"
        # dl_path = os.path.join(local_folder, filename)
        # blob.download_to_filename(dl_path)
        
        with self.gcs_fs.open(path) as f:
            dfLoc = pd.read_csv(f)
            print(f'{file} downloaded from ' + f'{bucket}.')
        return dfLoc

    def remove_duplicates_from_new(self, new_results: pd.core.frame.DataFrame) -> pd.core.frame.DataFrame:
        """What the function name says"""
        df_deduped = pd.DataFrame(columns=new_results.columns)
        for index, row in new_results.iterrows():
            # gpid_exists = self.dfLoc.gpid.str.contains('ChIJT').any():
            gpid_exists = self.dfLoc.gpid.str.contains(row.gpid).any()
            if not gpid_exists:
                df_deduped = df_deduped.append(row)
        return df_deduped

    def write_new_poi_data(self, update_data: pd.core.frame.DataFrame) -> None:
        """
        inputs:
            update_data: pd Dataframe
        Updates the existing data of POIs used by recommender, depending on the option used
        """
        self.dfNew = pd.concat([self.dfLoc, update_data], sort=False)
        # self.dfLoc = None
        # missing_cols = list(set(self.dfLoc.columns.to_list()) - set(update_data.columns.to_list()))

        method = self.cfg['backend']
        if method == 'local':
            self.update_data_to_local()
        elif method == 'gcp':
            self.update_data_to_gcp()
        
        self.dfLoc = self.dfNew  # updates the dfLoc
        print('POI data in {} updated'.format(method))

    def update_data_to_local(self):
        module = self.cfg['data_local']['module']
        folder = self.cfg['data_local']['folder']
        file = self.cfg['data_local']['data_file']
        out_path = os.path.join(module, folder, file)
        self.dfNew.to_csv(out_path, index=False)
        print('updated file saved to ' + f'{out_path}.')

    def update_data_to_gcp(self):
        # write updates to file
        bucket = self.cfg['data_gcp']['bucket']
        folder = self.cfg['data_gcp']['folder']
        file = self.cfg['data_gcp']['data_file']
        out_path = bucket + '/' + folder + '/' + file  # folderpaths are in unix
        with self.gcs_fs.open(out_path, 'w') as f:
            self.dfNew.to_csv(f, index=False)
            print('updated file uploaded to ' + f'{bucket}.')
        