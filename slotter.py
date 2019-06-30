'''
given a list of ranked locations to visit, tries to put the locations
in sequence on the shortest path
'''

import numpy as np
import pandas as pd
import ortools
# import json
import os

# load data
folder = 'test_data'
locfile = 'locations_add_data.csv'

dfLoc = pd.read_csv(os.path.join(folder, locfile))

# General process:
# 1. generate a weighted distance or time matrix (i.e the cost)
# 2. choose some way of solving it
#   a. Brute force: compare path costs from all combinations
    # b. Some heuristic: e.g. just take nearest neighbour
    # c. use a pre-written solver, e.g. google OR tools
# 3. select

def create_dist_matrix(lats, lngs):
    """ Creates a matrix of haversine distances between all points inputs
    input: lists of lats and longs, must be same length
    output: np matrix of distances between all points
    """
    npts = len(lats)
    if npts != len(lngs):
        raise ValueError('length of lats/longs not the same')
    elif npts == 0:
        raise ValueError('points list empty')

    # TODO: TESTING please remove
    # lats = dfLoc.lat.to_numpy().reshape(-1,1)
    # lngs = dfLoc.lng.to_numpy().reshape(-1,1)
    mat = np.hstack((lats, lngs))
    output = np.zeros([npts, npts])
    # create triangle matrix of distances between all pts
    for i in range(npts):
        p1 = np.repeat(mat[i,:].reshape(1,2), repeats=npts-i, axis=0)
        p2 = mat[i:,:]
        p1_lat, p1_lng = np.hsplit(p1, 2)
        p2_lat, p2_lng = np.hsplit(p2, 2)
        output[i:,i] = haversine_vect_dist(p1_lat, p1_lng, p2_lat, p2_lng)
    # fill upper right triangle with lower left triangle
    ind_upper = np.triu_indices(npts, 1)
    output[ind_upper] = output.T[ind_upper]
    
    return output
    


def haversine_vect_dist(s_lat, s_lng, e_lat, e_lng, scale=1000):
   """Calculate haversine distances elementwise for two lists of long/lats
   input: 4 lists of equal length, containing the lat/long of start and end pt pairs
   returns: 1D matrix of length n"""
   # approximate radius of earth in km
   R = 6373.0

   s_lat = s_lat*np.pi/180.0                      
   s_lng = np.deg2rad(s_lng)     
   e_lat = np.deg2rad(e_lat)                       
   e_lng = np.deg2rad(e_lng)  

   d = np.sin((e_lat - s_lat)/2)**2 + np.cos(s_lat)*np.cos(e_lat) * np.sin((e_lng - s_lng)/2)**2

   return 2 * R * scale * np.arcsin(np.sqrt(d)).reshape(-1,)
