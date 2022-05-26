import pandas as pd
from main import login
from getResource import getResources
from datetime import datetime, timedelta
import locale
locale.setlocale(locale.LC_ALL, 'es_ES.UTF-8')

"""
GEOFENCES OBJECTS
  1: Cementos Inka
  2: Cerro Azul
  3: Impala Terminals
  4: Mina Cerro Lindo
  5: Refineria Cajamarquilla
  6: Taller Saturno Pucusana
  7: Unacem
"""

"""
TEMPLATES
  1: Basic Data
  2: Geofence
  3: Viajes
"""

"""
RESULTS Guardia
  0: Trips between geofences
  1: Trips
  2: Parking
  3: Geofences Chancado I
"""

"""
 [{'nm': 'BBA-880', 'cls': 2, 'id': 10293, 'mu': 3, 'uacl': 19327369763},
  {'nm': 'BBB-850', 'cls': 2, 'id': 10267, 'mu': 3, 'uacl': 19327369763},
  {'nm': 'BBC-924', 'cls': 2, 'id': 10277, 'mu': 3, 'uacl': 19327369763},
  {'nm': 'BBC-929', 'cls': 2, 'id': 10265, 'mu': 3, 'uacl': 19327369763}]}
"""

resources = getResources()

# start = datetime(2022, 2, 10)
# end = datetime(2022, 5, 9)
# unit = 10293


def getTripsFromMine(start, end, unit):
    sdk = login()
    parameterSetLocale = {
        'tzOffset': -18000,
        "language": "en"
    }
    sdk.render_set_locale(parameterSetLocale)

    paramsExecReport = {
        'reportResourceId': resources['items'][0]['id'],
        'reportTemplateId': 2,
        'reportObjectId': unit,
        'reportObjectSecId': 0,
        'interval': {
            'from': int(start.timestamp()),
            'to': int(end.timestamp()),
            'flags': 0
        }
    }
    reports = sdk.report_exec_report(paramsExecReport)
    # TRIPS
    # 6 TripsMine2Lima
    paramsTrips = {
        'tableIndex': 5,
        'indexFrom': 0,
        'indexTo': reports['reportResult']['tables'][5]['rows']
    }
    rowsTrips = sdk.report_get_result_rows(paramsTrips)
    dataTrips = [r['c'] for r in rowsTrips]
    dfTrips = pd.DataFrame(dataTrips)
    # /////////////////////////////////////////////////////////////////////////////
    dfTrips.rename(columns={0: 'parkingDuration', 1: 'tripDuration', 2: 'ratio',
                            3: 'Trip', 4: 'tripFrom', 5: 'tripTo', 6: 'begin', 7: 'end', 8: 'mileage', 9: 'tripDurationHour', 10: 'parkingDurationHour', 11: 'avgSpeed', 12: 'maxSpeed', 13: 'consumed', 14: 'avgConsumed'}, inplace=True)
    dfTrips['parkingDuration'] = dfTrips['parkingDuration'].astype(float)
    dfTrips['tripDuration'] = dfTrips['tripDuration'].astype(float)
    dfTrips['ratio'] = dfTrips['ratio'].apply(
        lambda x: x.split(' ')[0]).astype(float)
    dfTrips['mileage'] = dfTrips['mileage'].apply(
        lambda x: x.split(' ')[0]).astype(float)
    dfTrips['avgSpeed'] = dfTrips['avgSpeed'].apply(
        lambda x: x.split(' ')[0]).astype(float)
    dfTrips['maxSpeed'] = dfTrips['maxSpeed'].apply(
        lambda x: x['t'].split(' ')[0]).astype(float)
    dfTrips['consumed'] = dfTrips['consumed'].apply(
        lambda x: x.split(' ')[0]).astype(float)
    dfTrips['avgConsumed'] = dfTrips['avgConsumed'].apply(
        lambda x: x.split(' ')[0]).astype(float)
    dfTrips['timestampBegin'] = dfTrips['begin'].apply(
        lambda x: x['v'])
    dfTrips['timestampEnd'] = dfTrips['end'].apply(
        lambda x: x['v'])
    dfTrips['datetimeBegin'] = dfTrips['begin'].apply(
        lambda x: x['t'])
    dfTrips['datetimeBegin'] = pd.to_datetime(dfTrips['datetimeBegin'])
    dfTrips['datetimeEnd'] = dfTrips['end'].apply(
        lambda x: x['t'])
    dfTrips['datetimeEnd'] = pd.to_datetime(dfTrips['datetimeEnd'])
    dfTrips['xBegin'] = dfTrips['begin'].apply(
        lambda x: x['x'])
    dfTrips['xEnd'] = dfTrips['end'].apply(
        lambda x: x['x'])
    dfTrips['yBegin'] = dfTrips['begin'].apply(
        lambda x: x['y'])
    dfTrips['yEnd'] = dfTrips['end'].apply(
        lambda x: x['y'])

    return dfTrips
