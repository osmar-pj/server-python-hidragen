import pandas as pd
from flask import Flask, jsonify, Request
from flask_cors import CORS
from getUnit import getUnits
from datetime import datetime, timedelta
from getBasicData import getBasicData
from getLastTrips import getLastTrips
# from dotenv import load_dotenv

app = Flask(__name__)
cors = CORS(app)
units = getUnits()


@app.route("/api/v1/units", methods=["GET"])
def getTotalUnits():
    return jsonify(units)


@app.route('/api/v1/historical', methods=['GET'])
def getAllData():
    df = pd.read_csv('df_tag.csv')
    data = df.to_dict(orient='records')
    return jsonify({'data': data})


@app.route("/api/v1/weeks", methods=["GET"])
def getWeek():
    dfw = pd.read_csv('df_week.csv')
    dfw['ahorro_BBC929'][0] = dfw['ahorro_BBC929'][0] * 0.5
    dfw['ahorro_BBC929'][1] = dfw['ahorro_BBC929'][1] * 0.6
    dfw['ahorro_BBC929'][2] = dfw['ahorro_BBC929'][2] * 0.5
    dfw['ahorro_BBC929'][3] = dfw['ahorro_BBC929'][3] * 0.7
    dfw['ahorro_BBB850'][0] = dfw['ahorro_BBB850'][0] * 0.8
    dfw['ahorro_BBB850'][2] = dfw['ahorro_BBB850'][2] * 0.7
    dfw.rename(columns={'parkingHours': 'Horas de parqueo (h): ', 'engineHours': 'Horas de motor (h): ', 'mileage': 'Kilometraje (km): ', 'avgSpeed': 'Velocidad Inst. (km/h): ', 'maxSpeed': 'Velocidad Max (km/h): ',
                        'consumed': 'Consumo combustible (gal): ', 'avgConsumed': 'Rendimiento (km/gal): ', 'ahorro_BBB850': 'Ahorro BBB-850 (%): ', 'ahorro_BBC929': 'Ahorro BBC-929 (%): '}, inplace=True)
    dfw = dfw.tail(4).reset_index().T.reset_index()
    dfw = dfw[1:]
    dfw.rename(columns={'index': 'label', 0: 'w1',
                        1: 'w2', 2: 'w3', 3: 'w4'}, inplace=True)
    weeks = dfw.to_dict(orient='records')
    return jsonify({'weeks': weeks})


@app.route("/api/v1/lastweek", methods=["GET"])
def getLastWeek():
    arr = []
    start = datetime.now() - timedelta(days=7)
    end = datetime.now()
    for u in units['items']:
        unit = u['id']
        dfLastweek = getBasicData(start, end, unit)
        dfLastweek['nm'] = u['nm']
        arr.extend(dfLastweek.to_dict(orient='records'))
    df = pd.DataFrame(arr)
    df['week'] = pd.to_datetime(df['date']).dt.strftime('%U')
    week = datetime.now().strftime('%U')
    df_lastweek = df.query('week == @week')
    df_lastweek = df_lastweek.groupby(['date']).sum().reset_index()
    df_lastweek['week'] = pd.to_datetime(df_lastweek['date']).dt.strftime('%U')
    df_lastweek['ratio'] = df_lastweek['consumed'] / df_lastweek['engineHours']
    df_lastweek['avgConsumed'] = df_lastweek['mileage'] / \
        df_lastweek['consumed']
    df_lastweek.to_csv('df_lastweek.csv', index=False)
    lastweek = df_lastweek.to_dict(orient='records')
    return jsonify({'lastweek': lastweek})


@app.route("/api/v1/s_lastweek", methods=["GET"])
def getLastWeekSpeed():
    df_lastweek = pd.read_csv('df_lastweek.csv')
    lastweek = df_lastweek.to_dict(orient='records')
    return jsonify({'lastweek': lastweek})


@app.route("/api/v1/trips", methods=["GET"])
def getLasttrip():
    arr = []
    for u in units['items']:
        unit = u['id']
        dfLastTrips = getLastTrips(unit)
        dfLastTrips['nm'] = u['nm']
        arr.append(dfLastTrips.to_dict(orient='records'))
    df = pd.DataFrame(arr)
    df.rename(columns={0: 'rutaA', 1: 'rutaB'}, inplace=True)
    df.to_csv('df_lasttrips.csv', index=False)
    return jsonify({'trips': arr})


@app.route("/api/v1/s_trips", methods=["GET"])
def getLasttripSpeed():
    df1 = pd.read_csv('df_lasttrips.csv')
    df1['rutaA'] = df1['rutaA'].apply(lambda x: eval(x))
    df1['rutaB'] = df1['rutaB'].apply(lambda x: eval(x))
    arr1 = df1.to_dict('tight')['data']
    return jsonify({'trips': arr1})


@app.route('/api/v1/routes', methods=['GET'])
def getRoutes():
    dfA = pd.read_csv('df_rutaA.csv')
    dfB = pd.read_csv('df_rutaB.csv')
    timeFilter = datetime.now() - timedelta(days=7)
    dfA['date'] = dfA['timestampBegin'].apply(
        lambda x: datetime.fromtimestamp(x).date())
    idxa = dfA['timestampBegin'] >= timeFilter.timestamp()
    dfA = dfA[idxa]
    idxb = dfB['timestampBegin'] >= timeFilter.timestamp()
    dfB = dfB[idxb]
    rutaA = dfA.to_dict(orient='records')
    rutaB = dfB.to_dict(orient='records')
    return jsonify({'rutaA': rutaA, 'rutaB': rutaB})


if (__name__ == "__main__"):
    app.run(debug=True)

# if (__name__ == "__main__"):
#     app.run(host='IP', port='PORT')
