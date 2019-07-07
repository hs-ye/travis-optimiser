'''
given a list of ranked locations to visit, tries to put the locations
in sequence on the shortest path
Current implementation users google ortools solver
'''

from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp
import numpy as np
import pandas as pd
import os
import json


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

    # load test data
    folders = ['travis_optimiser','test_data']
    locfile = 'locations_add_data.csv'

    dfLoc = pd.read_csv(os.path.join(*folders, locfile))
    ans = solveRouting(dfLoc)
    print(ans.head())
