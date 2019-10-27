from flask import Flask, jsonify, request
# from lib.gmaps_fetch import fetchGmapLocationData, getLocDataToDF
# from lib.router import solveRouting
from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp
import pandas as pd
import json
import googlemaps
import os
import pickle

app = Flask(__name__)

try:  # google cloud GAE debugger
  import googleclouddebugger
  googleclouddebugger.enable()
except ImportError:
  pass


@app.route("/")
@app.route("/home")
def home():
    return "<h1> Travis optimiser testing - use /api_route endpoint for testing</h1>"

@app.route("/about")
def about():
    return "About"

@app.route("/api_route")
def api_route():
    headers = json.loads(request.headers.get('nodes'))
    test = pd.DataFrame(columns=['name'])
    test['name'] = headers
    print(test)
    data = getLocDataToDF(test)
    ans = solveRouting(data)
    return jsonify(test.to_dict(orient='records'))

@app.route("/api_test")
def api_test():
    test = pd.DataFrame(columns=['name'])
    test['name'] = ['southern cross station', 'luna park', 'koko black', 
        'university of melbourne']
    data = getLocDataToDF(test)
    ans = solveRouting(data)
    return jsonify(ans.to_dict(orient='records'))

# pasted all functions here manually for GAE testing
# setup gmaps object  
# TODO should wrap all this data in a class and pass in params
gmaps = googlemaps.Client(key='AIzaSyBrY7HAvOgb8NHhW-mir7CQERHER8saC28')
mel_loc = (-37.8132, 144.965)  # centre of search radius
folder = 'test_data'
infile = 'locations.csv'
pickfile = 'gmaps_cache.pickle'
outfile = 'locations_add_data.csv'

def fetchGmapLocationData(dfLoc, useId=False):
    """ does a search based on the 'name' col of a passed in df
    TODO: Use the Gmaps ID to fetch locations based on useID param
    """
    locs = dfLoc.name  # col containing place names
    place_search_cache = []
    # for loc in locs[0:3]:  # testing limited search only
    for loc in locs:
        print('search:', loc)
        place = gmaps.places(loc, mel_loc, radius=10000)  # place search api
        print('found:', place['results'][0]['name'])
        place_search_cache.append(place)
    return place_search_cache


def getCachedGmapData(dfLoc, pickfile="gmaps_cache.pickle"):
    """ Try to get data from Pickle file, if it exists then ignores dfLoc
    if not, then fetch data from dfLoc and make pickle from gmaps API
    Doesn't check pickle file contents"""
    # if os.path.getsize(pickfile):  # check pickle file not empty
    if os.path.isfile(pickfile):  # check pickle file exists
        print('looks like gmaps data already exists. Try loading')
        try:
            infile = open(pickfile,'rb')
            gmap_data = pickle.load(infile)
            print('gmaps data loaded from pickle')
        except:
            print('could not load pickle data')
        else:
            infile.close()
    else:
        print('no data found - re-download data')
        try:
            outfile = open(pickfile,'wb')
            gmap_data = fetchGmapLocationData(dfLoc)
            pickle.dump(gmap_data, outfile)
            print('gmap data downloaded and saved')
        except:
            print('error saving gmaps data as pickle')
        else:
            outfile.close()
    return gmap_data


def extractLocDataFromGmapJSON(place_search_cache):
    """ Gets the required lat long location data from GMAP JSON response
    don't need the gmaps.place() api yet - see test filefor details
    """
    gpid_l, lat_l, lng_l, rating_l = [], [], [], []
    for place in place_search_cache:
        lng_l.extend([place['results'][0]['geometry']['location']['lng']])  # how to access lat
        lat_l.extend([place['results'][0]['geometry']['location']['lat']])  # and long
        gpid_l.extend([place['results'][0]['place_id']])
        try:
            rating_l.extend([place['results'][0]['rating']])
        except KeyError:  # possible some places don't have ratings
            rating_l.append(None)
            print('no rating found for {}'.format(place['results'][0]['name']))
    print(len(gpid_l), len(lat_l), len(lng_l), len(rating_l))
    return gpid_l, lat_l, lng_l, rating_l


def getLocDataToDF(dfLoc, saveCSV=False, use_cache=False):
    if use_cache:
        place_search_cache = getCachedGmapData(dfLoc)
    else:  # skip the caching logic
        place_search_cache = fetchGmapLocationData(dfLoc)
    gpid_l, lat_l, lng_l, rating_l = extractLocDataFromGmapJSON(place_search_cache)
    # add extensions to df
    dfLoc['gpid'] = gpid_l
    dfLoc['lat'] = lat_l
    dfLoc['lng'] = lng_l
    dfLoc['rating'] = rating_l
    # Save as csv to folder
    if saveCSV:
        dfLoc.to_csv(os.path.join(folder, outfile), index=False)
    return dfLoc


# Code for routing - here for GAE testing

def createDistMatrix(lats, lngs):
    """ Creates a matrix of haversine distances between all points inputs
    input: lists of lats and longs, must be same length
    output: np matrix of distances between all points, by default in m
    """
    npts = len(lats)
    if npts != len(lngs):
        raise ValueError('length of lats/longs not the same')
    elif npts == 0:
        raise ValueError('points list empty')

    mat = np.hstack((lats, lngs))
    output = np.zeros([npts, npts])
    # create triangle matrix of distances between all pts
    for i in range(npts):
        p1 = np.repeat(mat[i,:].reshape(1,2), repeats=npts-i, axis=0)
        p2 = mat[i:,:]
        p1_lat, p1_lng = np.hsplit(p1, 2)
        p2_lat, p2_lng = np.hsplit(p2, 2)
        output[i:,i] = haversineVectDist(p1_lat, p1_lng, p2_lat, p2_lng)
    # fill upper right triangle with lower left triangle
    ind_upper = np.triu_indices(npts, 1)
    output[ind_upper] = output.T[ind_upper]

    return output.astype(int)
    

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

def createTspSolverData(dfLoc, start_node=0):
    """ Placeholder: Testing data maker
    """
    data = {}
    lats = dfLoc.lat.to_numpy().reshape(-1,1)
    lngs = dfLoc.lng.to_numpy().reshape(-1,1)
    data['distance_matrix'] = createDistMatrix(lats, lngs)
    data['num_vehicles'] = 1
    data['depot'] = start_node
    return data


def distanceCallback(from_index, to_index):
    """ ortools tsp solver method, gets distances from the distance matrix
        notice we are using numpy array slicing, rather than python lists
        NOTE IMPORTANT: For some reason, this function definition must be defined AFTER the 'manager' 
        instance is created, for some reason.
        See https://stackoverflow.com/questions/55862927/python-or-tools-function-does-not-work-when-called-from-within-a-python-package
    """
    from_node = manager.IndexToNode(from_index)
    to_node = manager.IndexToNode(to_index)
    return data['distance_matrix'][from_node, to_node]


def printSolutionToConsole(manager, routing, assignment):
    """Prints route on console."""
    print('Objective: {} m'.format(assignment.ObjectiveValue()))
    index = routing.Start(0)
    plan_output = 'Route for vehicle 0:\n'
    route_distance = 0
    while not routing.IsEnd(index):
        plan_output += ' {} ->'.format(manager.IndexToNode(index))
        previous_index = index
        index = assignment.Value(routing.NextVar(index))
        route_distance += routing.GetArcCostForVehicle(previous_index, index, 0)
    plan_output += ' {}\n'.format(manager.IndexToNode(index))
    plan_output += 'Route distance: {}m\n'.format(route_distance)
    print(plan_output)

def getSolutionAsDF(manager, routing, assignment):
    """returns route solution as a dataframe"""
    print('Solution of minimal travel dist: {} m'.format(assignment.ObjectiveValue()))
    index = routing.Start(0)
    total_route_distance = 0
    result = pd.DataFrame(columns=['node', 'dist_to_next'])
    order = 0
    while not routing.IsEnd(index):  # loop through all nodes
        result.loc[order, 'node'] = int(manager.IndexToNode(index))
        # node = manager.IndexToNode(index)  # current node
        previous_index = index  # increment to next node
        index = assignment.Value(routing.NextVar(index))
        result.loc[order, 'dist_to_next'] = routing.GetArcCostForVehicle(previous_index, index, 0)
        total_route_distance += result.loc[order, 'dist_to_next']
        order += 1
    return result


def solveRouting(dfLoc, s_node=0):
    """ Solves the shortest route of locations given in the input df
    inputs:
        dfLoc: df of nodes, with 'lat' and 'lng' values as columns, in degrees
    returns:
        a df with nodes in order of shortest route
    """
    data = createTspSolverData(dfLoc, start_node=0)  # start node is the start point
    manager = pywrapcp.RoutingIndexManager(
        len(data['distance_matrix']), data['num_vehicles'], data['depot'])
    routing = pywrapcp.RoutingModel(manager)

    def distanceCallback(from_index, to_index):
        """ ortools tsp solver method, gets distances from the distance matrix
        using numpy array slicing, rather than python lists
        NOTE IMPORTANT: For some reason, this function definition must be defined AFTER the 'manager' 
        instance is created, for some reason. 
        See https://stackoverflow.com/questions/55862927/python-or-tools-function-does-not-work-when-called-from-within-a-python-package
        """
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return data['distance_matrix'][from_node, to_node]

    transit_callback_index = routing.RegisterTransitCallback(distanceCallback)
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)
    assignment = routing.SolveWithParameters(search_parameters)

    if assignment:
        printSolutionToConsole(manager, routing, assignment)
        dfAns = getSolutionAsDF(manager, routing, assignment)
        dfLoc.index.name = 'node'
        dfAns = dfAns.merge(dfLoc, on=['node','node'])
        return dfAns
    print('Error - no solution found, check input data')


if __name__ == '__main__':
    app.run(debug=True)