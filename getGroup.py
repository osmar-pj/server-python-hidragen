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

# start = datetime(2022, 5, 22)
# end = datetime.now()
# unit = 10293


def getGroup(unit):
    end = datetime.now()
    start = end - timedelta(weeks=6)
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
    paramsRutaA = {
        'tableIndex': 8,
        'indexFrom': 0,
        'indexTo': reports['reportResult']['tables'][8]['rows']
    }
    rowsRutaA = sdk.report_get_result_rows(paramsRutaA)
    dataRutaA = [r['c'] for r in rowsRutaA]
    dfRutaA = pd.DataFrame(dataRutaA)

    paramsRutaB = {
        'tableIndex': 9,
        'indexFrom': 0,
        'indexTo': reports['reportResult']['tables'][9]['rows']
    }
    rowsRutaB = sdk.report_get_result_rows(paramsRutaB)
    dataRutaB = [r['c'] for r in rowsRutaB]
    dfRutaB = pd.DataFrame(dataRutaB)

    dfRutaA.rename(columns={0: 'parkingDuration', 1: 'tripDuration', 2: 'ratio', 3: 'trip', 4: 'tripFrom', 5: 'tripTo', 6: 'datetimeBegin', 7: 'datetimeEnd',
                            8: 'mileage', 9: 'tripDurationTime', 10: 'parkingDurationTime', 11: 'avgSpeed', 12: 'maxSpeed', 13: 'consumed', 14: 'avgConsumed'}, inplace=True)
    dfRutaA['parkingDuration'] = pd.to_numeric(
        dfRutaA['parkingDuration'], errors='coerce')
    dfRutaA['tripDuration'] = pd.to_numeric(
        dfRutaA['tripDuration'], errors='coerce')
    dfRutaA['ratio'] = dfRutaA['ratio'].apply(
        lambda x: x.split(' ')[0]).astype(float)
    dfRutaA['mileage'] = dfRutaA['mileage'].apply(
        lambda x: x.split(' ')[0]).astype(int)
    dfRutaA['avgSpeed'] = dfRutaA['avgSpeed'].apply(
        lambda x: x.split(' ')[0]).astype(float)
    dfRutaA['maxSpeed'] = dfRutaA['maxSpeed'].apply(
        lambda x: x['t'].split(' ')[0]).astype(int)
    dfRutaA['consumed'] = dfRutaA['consumed'].apply(
        lambda x: x.split(' ')[0]).astype(float)
    dfRutaA['avgConsumed'] = dfRutaA['avgConsumed'].apply(
        lambda x: x.split(' ')[0]).astype(float)
    dfRutaA['timestampBegin'] = dfRutaA['datetimeBegin'].apply(
        lambda x: x['v'])
    dfRutaA['datetimeBegin'] = pd.to_datetime(
        dfRutaA['datetimeBegin'].apply(lambda x: x['t']))
    dfRutaA['timestampEnd'] = dfRutaA['datetimeEnd'].apply(lambda x: x['v'])
    dfRutaA['datetimeEnd'] = pd.to_datetime(
        dfRutaA['datetimeEnd'].apply(lambda x: x['t']))

    dfRutaB.rename(columns={0: 'parkingDuration', 1: 'tripDuration', 2: 'ratio', 3: 'trip', 4: 'tripFrom', 5: 'tripTo', 6: 'datetimeBegin', 7: 'datetimeEnd',
                            8: 'mileage', 9: 'tripDurationTime', 10: 'parkingDurationTime', 11: 'avgSpeed', 12: 'maxSpeed', 13: 'consumed', 14: 'avgConsumed'}, inplace=True)
    dfRutaB['parkingDuration'] = pd.to_numeric(
        dfRutaB['parkingDuration'], errors='coerce')
    dfRutaB['tripDuration'] = pd.to_numeric(
        dfRutaB['tripDuration'], errors='coerce')
    dfRutaB['ratio'] = dfRutaB['ratio'].apply(
        lambda x: x.split(' ')[0]).astype(float)
    dfRutaB['mileage'] = dfRutaB['mileage'].apply(
        lambda x: x.split(' ')[0]).astype(int)
    dfRutaB['avgSpeed'] = dfRutaB['avgSpeed'].apply(
        lambda x: x.split(' ')[0]).astype(float)
    dfRutaB['maxSpeed'] = dfRutaB['maxSpeed'].apply(
        lambda x: x['t'].split(' ')[0]).astype(int)
    dfRutaB['consumed'] = dfRutaB['consumed'].apply(
        lambda x: x.split(' ')[0]).astype(float)
    dfRutaB['avgConsumed'] = dfRutaB['avgConsumed'].apply(
        lambda x: x.split(' ')[0]).astype(float)
    dfRutaB['timestampBegin'] = dfRutaB['datetimeBegin'].apply(
        lambda x: x['v'])
    dfRutaB['datetimeBegin'] = pd.to_datetime(
        dfRutaB['datetimeBegin'].apply(lambda x: x['t']))
    dfRutaB['timestampEnd'] = dfRutaB['datetimeEnd'].apply(lambda x: x['v'])
    dfRutaB['datetimeEnd'] = pd.to_datetime(
        dfRutaB['datetimeEnd'].apply(lambda x: x['t']))

    return dfRutaA, dfRutaB

# pd.set_option('display.max_rows', None)
