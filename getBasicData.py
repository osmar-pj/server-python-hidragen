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

# start = datetime(2022, 5, 18)
# end = datetime(2022, 5, 21, 23, 59, 59)
# unit = 10267


def getBasicData(start, end, unit):
    sdk = login()
    parameterSetLocale = {
        'tzOffset': -18000,
        "language": "en"
    }
    sdk.render_set_locale(parameterSetLocale)

    paramsExecReport = {
        'reportResourceId': resources['items'][0]['id'],
        'reportTemplateId': 1,
        'reportObjectId': unit,
        'reportObjectSecId': 0,
        'interval': {
            'from': int(start.timestamp()),
            'to': int(end.timestamp()),
            'flags': 0
        }
    }
    reports = sdk.report_exec_report(paramsExecReport)
    # Basic Data

    paramsDay = {
        'tableIndex': 0,
        'indexFrom': 0,
        'indexTo': reports['reportResult']['tables'][0]['rows']
    }
    rowDay = sdk.report_get_result_rows(paramsDay)
    dataDay = [r['c'] for r in rowDay]
    dfDay = pd.DataFrame(dataDay)

    # /////////////////////////////////////////////////////////////////////////////
    dfDay.rename(columns={0: 'date', 1: 'parkingHours', 2: 'engineHours',
                          3: 'moveTimeHours', 4: 'mileage', 5: 'avgSpeed', 6: 'maxSpeed', 7: 'moveTime', 8: 'engine', 9: 'parking', 10: 'consumed', 11: 'avgConsumed'}, inplace=True)
    dfDay['date'] = pd.to_datetime(dfDay['date'])
    dfDay['timestamp'] = dfDay['date'].apply(lambda x: x.timestamp())
    dfDay['parkingHours'] = dfDay['parkingHours'].astype(float)
    dfDay['engineHours'] = dfDay['engineHours'].astype(float)
    dfDay['moveTimeHours'] = dfDay['moveTimeHours'].astype(float)
    dfDay['mileage'] = dfDay['mileage'].apply(
        lambda x: x.split(' ')[0]).astype(float)
    dfDay['avgSpeed'] = dfDay['avgSpeed'].apply(
        lambda x: x.split(' ')[0]).astype(float)
    dfDay['maxSpeed'] = dfDay['maxSpeed'].apply(
        lambda x: x['t'].split(' ')[0] if x != '0 km/h' else 0).astype(int)
    dfDay['consumed'] = dfDay['consumed'].apply(
        lambda x: x.split(' ')[0]).astype(float)
    dfDay['avgConsumed'] = dfDay['avgConsumed'].apply(
        lambda x: x.split(' ')[0]).astype(float)

    return dfDay
