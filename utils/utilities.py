import numpy as np


def haversineVectDist(s_lat, s_lng, e_lat, e_lng, scale=1000):
   """Calculate haversine distances elementwise for two lists of long/lats
   input: 
        4 lists of equal length, containing the lat/long of start and end pt pairs
        NOTE: lat/longs should be in degrees
        scale: 1000 for m, 1 for km etc.
   returns: 1D matrix of length n"""
   R = 6373.0  # approximate radius of earth in km

   s_lat = s_lat*np.pi/180.0                      
   s_lng = np.deg2rad(s_lng)     
   e_lat = np.deg2rad(e_lat)                       
   e_lng = np.deg2rad(e_lng)  

   d = np.sin((e_lat - s_lat)/2)**2 + np.cos(s_lat)*np.cos(e_lat) * np.sin((e_lng - s_lng)/2)**2

   return 2 * R * scale * np.arcsin(np.sqrt(d)).reshape(-1,)
