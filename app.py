from flask import Flask, jsonify, request
from travis_optimiser.gmaps_fetch import fetchGmapLocationData, getLocDataToDF
from travis_optimiser.router import solveRouting
import pandas as pd
import json

app = Flask(__name__)

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
    return jsonify(test.to_dict(orient='records'))

@app.route("/api_test")
def api_test():
    test = pd.DataFrame(columns=['name'])
    test['name'] = ['southern cross station', 'luna park', 'koko black', 
        'university of melbourne']
    data = getLocDataToDF(test)
    ans = solveRouting(data)
    return jsonify(ans.to_dict(orient='records'))



if __name__ == '__main__':
    app.run(debug=True)