from flask import Flask, jsonify
from travis_optimiser.gmaps_fetch import fetchGmapLocationData
import pandas as pd

app = Flask(__name__)

@app.route("/")
@app.route("/home")
def home():
    return "<h1> Home Page </h1>"

@app.route("/about")
def about():
    return "About"

@app.route("/api_test")
def api_test():
    test = pd.DataFrame(columns=['Name'])
    test['Name'] = ['southern cross station']
    print(test)
    data = fetchGmapLocationData(test)
    return jsonify(data)

@app.route("/api_router")
def api_router():


if __name__ == '__main__':
    app.run(debug=True)