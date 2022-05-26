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
# end = datetime(2022, 5, 9, 23, 59, 59)
# unit = 10267


def getGeoSaturno(start, end):
    sdk = login()
    parameterSetLocale = {
        'tzOffset': -18000,
        "language": "en"
    }
    sdk.render_set_locale(parameterSetLocale)

    paramsExecReport = {
        'reportResourceId': resources['items'][0]['id'],
        'reportTemplateId': 3,
        'reportObjectId': resources['items'][0]['id'],
        'reportObjectSecId': 3,
        'interval': {
            'from': int(start.timestamp()),
            'to': int(end.timestamp()),
            'flags': 0
        }
    }
    reports = sdk.report_exec_report(paramsExecReport)
    # Geofences

    paramGeoSaturno = {
        'tableIndex': 0,
        'indexFrom': 0,
        'indexTo': reports['reportResult']['tables'][0]['rows']
    }
    rowGeoSaturno = sdk.report_get_result_rows(paramGeoSaturno)
    dataGeoSaturno = [r['c'] for r in rowGeoSaturno]
    dfGeoSaturno = pd.DataFrame(dataGeoSaturno)

    # /////////////////////////////////////////////////////////////////////////////
    dfGeoSaturno.rename(columns={0: 'nm', 1: 'timeIn', 2: 'timeOut',
                                 3: 'durationIn', 4: 'parkingDuration'}, inplace=True)
    dfGeoSaturno['timestampIn'] = dfGeoSaturno['timeIn'].apply(
        lambda x: x['v'])
    dfGeoSaturno['timeIn'] = pd.to_datetime(
        dfGeoSaturno['timeIn'].apply(lambda x: x['t']))
    dfGeoSaturno['timestampOut'] = pd.to_datetime(
        dfGeoSaturno['timeOut'].apply(lambda x: x['v']))
    dfGeoSaturno['timeOut'] = dfGeoSaturno['timeOut'].apply(lambda x: x['t'])
    dfGeoSaturno['durationIn'] = dfGeoSaturno['durationIn'].astype(float)
    dfGeoSaturno['parkingDuration'] = dfGeoSaturno['parkingDuration'].astype(
        float)

    # Agrupar total por fechas
    dfGeoSaturno['date'] = dfGeoSaturno['timeIn'].dt.date
    dfGeoSaturno.groupby(['date']).agg(
        {'durationIn': 'sum', 'parkingDuration': 'sum', 'nm': ' '.join})

# Agrupar total por tags

    return dfGeoSaturno
