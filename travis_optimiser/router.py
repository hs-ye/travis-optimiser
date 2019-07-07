'''
given a list of ranked locations to visit, tries to put the locations
in sequence on the shortest path
'''

import numpy as np
import pandas as pd
from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp
import os

# General process:
# 1. generate a weighted distance or time matrix (i.e the cost)
# 2. choose some way of solving it
#   a. Brute force: compare path costs from all combinations
    # b. Some heuristic: e.g. just take nearest neighbour
    # c. NOTE what this currently uses: pre-written solver in google ortools
# 3. select


def create_dist_matrix(lats, lngs):
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
        output[i:,i] = haversine_vect_dist(p1_lat, p1_lng, p2_lat, p2_lng)
    # fill upper right triangle with lower left triangle
    ind_upper = np.triu_indices(npts, 1)
    output[ind_upper] = output.T[ind_upper]

    return output.astype(int)
    

def haversine_vect_dist(s_lat, s_lng, e_lat, e_lng, scale=1000):
   """Calculate haversine distances elementwise for two lists of long/lats
   input: 
        4 lists of equal length, containing the lat/long of start and end pt pairs
        scale: 1000 for m, 1 for km etc.
   returns: 1D matrix of length n"""
   R = 6373.0  # approximate radius of earth in km

   s_lat = s_lat*np.pi/180.0                      
   s_lng = np.deg2rad(s_lng)     
   e_lat = np.deg2rad(e_lat)                       
   e_lng = np.deg2rad(e_lng)  

   d = np.sin((e_lat - s_lat)/2)**2 + np.cos(s_lat)*np.cos(e_lat) * np.sin((e_lng - s_lng)/2)**2

   return 2 * R * scale * np.arcsin(np.sqrt(d)).reshape(-1,)

def create_tsp_solver_data(dfLoc):
    """ Placeholder: Testing data maker
    """
    data = {}
    lats = dfLoc.lat.to_numpy().reshape(-1,1)
    lngs = dfLoc.lng.to_numpy().reshape(-1,1)
    data['distance_matrix'] = create_dist_matrix(lats, lngs)
    data['num_vehicles'] = 1
    data['depot'] = 0
    return data


def distance_callback(from_index, to_index):
    """ required part of the ortools tsp solver
    basically get distances from the distance matrix
    notice we are using numpy array slicing"""
    from_node = manager.IndexToNode(from_index)
    to_node = manager.IndexToNode(to_index)
    return data['distance_matrix'][from_node, to_node]


def print_solution(manager, routing, assignment):
    # TODO: return the route and us df to get the list of locations to travel
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
    print(plan_output)
    plan_output += 'Route distance: {}m\n'.format(route_distance)


if __name__ == '__main__':

    # load data
    folder = 'test_data'
    locfile = 'locations_add_data.csv'

    dfLoc = pd.read_csv(os.path.join(folder, locfile))
    data = create_tsp_solver_data(dfLoc)

    manager = pywrapcp.RoutingIndexManager(
        len(data['distance_matrix']), data['num_vehicles'], data['depot'])
    routing = pywrapcp.RoutingModel(manager)

    transit_callback_index = routing.RegisterTransitCallback(distance_callback)
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)

    assignment = routing.SolveWithParameters(search_parameters)
    if assignment:
        print_solution(manager, routing, assignment)