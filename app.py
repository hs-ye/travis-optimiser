from flask import Flask, jsonify, request
from travis_optimiser.gmaps_fetch import fetchGmapLocationData, getLocDataToDF
from travis_optimiser.router import solve_routing
from travis_optimiser.recommender import rec_from_list, get_gmaps, get_best_recs
import logging
import pandas as pd
import json
import os

app = Flask(__name__)

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('')

# gmaps client loaded at start of the app
gmaps = get_gmaps()

@app.route("/")
@app.route("/home")
def home():
    return "<h1> Home Page </h1>"

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
    ans = solve_routing(data)
    return jsonify(ans.to_dict(orient='records'))

@app.route("/api_test")
def api_test():
    """run test"""
    test = pd.DataFrame(columns=['name'])
    test['name'] = ["southern cross station", "luna park", "sydney airport", 
        "university of melbourne", "sydney opera house"]
    dfLoc = getLocDataToDF(test)
    ans = solve_routing(dfLoc)
    return jsonify(ans.to_dict(orient='records'))

@app.route("/api_solve_route_from_csv")
def api_solve_route_from_csv():
    """ read locations from csv files and solve, assumes already geocoded"""
    folder = 'travis_optimiser\\test_data'
    # pickfile = 'gmaps_cache.pickle'
    outfile = 'locations_add_data.csv'
    dfLoc = pd.read_csv(os.path.join(folder, outfile), encoding='UTF-8')
    ans = solve_routing(dfLoc)
    return jsonify(ans.to_dict(orient='records'))


@app.route("/api_recommend_from_file")
def api_recommend_from_file():
    """ NOTE: Deprecated - do not use"""
    # use headers in get request: ids:["ChIJdedaLk5d1moRQOX0CXZWBB0", "ChIJczgQh8lC1moR9r9gP44FRvY"]
    headers = json.loads(request.headers.get('ids'))
    print(headers)
    id1 = headers[0]
    id2 = headers[1]
    # dfIds = pd.DataFrame(columns=['ids'])
    # dfIds['ids'] = headers
    folder = 'travis_optimiser\\test_data'  #  PC
    # folder = 'travis_optimiser/test_data'  # MAC
    outfile = 'locations_recommender.csv'
    dfLoc = pd.read_csv(os.path.join(folder, outfile), encoding='UTF-8')
    recs = rec_from_list(gmaps, id1, id2, dfLoc)  # default finds 'eat' places within 500m
    return jsonify(recs.to_dict())

@app.route("/api_get_recs_eats"):
def api_get_recs_eats():
    headers = json.loads(request.headers.get('ids'))
    print(headers)
    recs = get_best_recs(gmaps, headers, rectype='restaurant')
    return jsonify(recs.to_dict())



if __name__ == '__main__':
    app.run(debug=True)
    api_test()