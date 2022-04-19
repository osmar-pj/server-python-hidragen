import pandas as pd
from flask import Flask, jsonify, Request
from flask_cors import CORS
from getTripByTruck import trip
from getTripTrucks import tripProduction

app = Flask(__name__)
cors = CORS(app)


@app.route("/api/v1/trips", methods=["GET"])
def getTotalTrips():
    df = pd.DataFrame(tripProduction)
    df.sort_values(by='timeStart', ascending=False, inplace=True)
    df1 = df.head(6)
    trips = df1.to_dict(orient='records')
    return jsonify({'trips': trips})


@app.route("/api/v1/trip/<tag>", methods=["GET"])
def getTripByTag(tag):
    tagId = tag
    print(tagId)
    return jsonify({'trip': trip})


if (__name__ == "__main__"):
    app.run(debug=True)
