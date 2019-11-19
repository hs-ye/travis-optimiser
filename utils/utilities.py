import numpy as np
import yaml
from typing import List, Tuple

def get_cfg(file="config.yml"):
     ''' Loads the chosen config file '''
     with open(file, 'r') as ymlfile:
          cfg = yaml.load(ymlfile)
     
     return cfg


def haversineVectDist(s_lat, s_lng, e_lat, e_lng, scale=1000) -> np.ndarray:
   """Calculate haversine distances elementwise for two lists of long/lats
   input: 
        4 lists of equal length, containing the lat/long of start and end pt pairs
        NOTE: lat/longs should be in degrees
        scale: 1000 for m, 1 for km etc.
   returns: 1D ndarray of length n"""
   R = 6373.0  # approximate radius of earth in km

   s_lat = s_lat*np.pi/180.0                      
   s_lng = np.deg2rad(s_lng)     
   e_lat = np.deg2rad(e_lat)                       
   e_lng = np.deg2rad(e_lng)  

   d = np.sin((e_lat - s_lat)/2)**2 + np.cos(s_lat)*np.cos(e_lat) * np.sin((e_lng - s_lng)/2)**2

   return 2 * R * scale * np.arcsin(np.sqrt(d)).reshape(-1,)


def calc_midpoint_of_gpids(gmaps, input_gpids: List[str]) -> Tuple[float]:
    lat1, lon1 = get_latlong_from_gpid(gmaps, input_gpids[0])
    lat2, lon2 = get_latlong_from_gpid(gmaps, input_gpids[1])
    lat_mid = (lat1 + lat2) / 2
    lon_mid = (lon1 + lon2) / 2
    return lat_mid, lon_mid


def get_latlong_from_gpid(gmaps, gpid: str) -> Tuple[float]:
    '''
    Retrieves the lat-long position of a given google place id
    gmaps: Requires a google maps object with a valid API Key
    '''
    place_result = gmaps.place(place_id=gpid)

    lat = place_result['result']['geometry']['location']['lat']
    lng = place_result['result']['geometry']['location']['lng']
    
    return (lat, lng)

