'''
given a list of ranked locations to visit, tries to put the locations
in sequence on the shortest path
'''


import pandas as pd
import requests
import googlemaps
import json
import os

# load data
folder = 'test_data'
locfile = 'locations_add_data.csv'

dfLoc = pd.read_csv(os.path.join(folder, locfile))