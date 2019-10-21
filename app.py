from flask import Flask, jsonify, request
from travis_optimiser.gmaps_fetch import fetchGmapLocationData, getLocDataToDF
from travis_optimiser.router import *
from travis_optimiser.recommender import recFromList, getGmaps
import logging
import pandas as pd
import json

app = Flask(__name__)

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('')

gmaps = getGmaps()

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
    ans = solveRouting(data)
    return jsonify(ans.to_dict(orient='records'))

@app.route("/api_test")
def api_test():
    """run test"""
    test = pd.DataFrame(columns=['name'])
    test['name'] = ["southern cross station", "luna park", "sydney airport", 
        "university of melbourne", "sydney opera house"]
    dfLoc = getLocDataToDF(test)
    ans = solveRouting(dfLoc)
    return jsonify(ans.to_dict(orient='records'))

@app.route("/api_test_from_csv")
def api_test_from_csv():
    """ read locations from csv files and solve, assumes already geocoded"""
    folder = 'travis_optimiser\\test_data'
    pickfile = 'gmaps_cache.pickle'
    outfile = 'locations_add_data.csv'
    dfLoc = pd.read_csv(os.path.join(folder, outfile), encoding='UTF-8')
    ans = solveRouting(dfLoc)
    return jsonify(ans.to_dict(orient='records'))


@app.route("/api_recommend_from_file")
def api_recommend_from_file():
    # use headers in get request: ids:["ChIJczgQh8lC1moR9r9gP44FRvY", "ChIJczgQh8lC1moR9r9gP44FRvY"]
    headers = json.loads(request.headers.get('ids'))
    print(headers)
    id1 = headers[0]
    id2 = headers[1]
    # dfIds = pd.DataFrame(columns=['ids'])
    # dfIds['ids'] = headers
    folder = 'travis_optimiser\\test_data'
    outfile = 'locations_recommender.csv'    
    dfLoc = pd.read_csv(os.path.join(folder, outfile), encoding='UTF-8')
    recs = recFromList(gmaps, id1, id2, dfLoc)  # default finds 'eat' places within 500m
    return jsonify(recs.to_dict())


if __name__ == '__main__':
    app.run(debug=True)
    api_test()