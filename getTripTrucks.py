from main import login
from datetime import datetime, timedelta
from getUnit import getUnits
from getResource import getResources
import pandas as pd


def getTrips():
    sdk = login()
    resources = getResources()
    parameterSetLocale = {
        'tzOffset': -18000,
        "language": "en"
    }
    sdk.render_set_locale(parameterSetLocale)
    start = (datetime.now() - timedelta(days=14)).timestamp()
    # end = int(datetime.now().timestamp())
    end = (datetime.now() - timedelta(days=1)).timestamp()
    # unit = 10277
    tripProduction = []
    units = getUnits()
    for unit in units['items']:
        paramsExecReport = {
            'reportResourceId': resources['items'][0]['id'],
            'reportTemplateId': 2,
            'reportObjectId': unit['id'],
            'reportObjectSecId': 0,
            'reportObjectIdList': 0,
            'interval': {
                'from': int(start),
                'to': int(end),
                'flags': 0
            }
        }
        reports = sdk.report_exec_report(paramsExecReport)
        paramsGetResultRows = {
            'tableIndex': 0,
            'indexFrom': 0,
            'indexTo': reports['reportResult']['tables'][0]['rows'] * 3
        }
        rows = sdk.report_get_result_rows(paramsGetResultRows)
        dataRows = [r['c'] for r in rows]
        df_rows = pd.DataFrame(dataRows)
        # SE CREA COLUMNAS Y SE EXTRAE VALORES DE OTRAS COLUMNAS
        df_rows[13] = 0
        df_rows[14] = 0
        df_rows[15] = 0
        df_rows[16] = 0
        df_rows[17] = 0
        df_rows[18] = 0
        df_rows[19] = 0
        df_rows[20] = 0
        df_rows[21] = 0
        df_rows[22] = 0
        df_rows[23] = 0
        df_rows[24] = 0
        df_rows[25] = 0
        df_rows[26] = 0
        df_rows[27] = ''
        for i, v in enumerate(df_rows.T):
            df_rows[13][i] = df_rows[4][i]['v']
            df_rows[14][i] = df_rows[4][i]['y']
            df_rows[15][i] = df_rows[4][i]['x']
            df_rows[16][i] = df_rows[5][i]['v']
            df_rows[17][i] = df_rows[5][i]['y']
            df_rows[18][i] = df_rows[5][i]['x']
            df_rows[19][i] = df_rows[6][i].split(' ')[0]
            df_rows[20][i] = df_rows[9][i].split(' ')[0]
            df_rows[21][i] = df_rows[10][i]['t'].split(' ')[0]
            df_rows[22][i] = df_rows[11][i].split(' ')[0]
            df_rows[23][i] = df_rows[12][i].split(' ')[0]
            df_rows[24][i] = datetime.fromtimestamp(
                df_rows[5][i]['v']).strftime("%D")
            df_rows[25][i] = datetime.fromtimestamp(
                df_rows[5][i]['v']).strftime("%V")
            df_rows[26][i] = datetime.fromtimestamp(
                df_rows[5][i]['v']).strftime("%B")
            df_rows[27][i] = unit['nm']
        df_rows[19] = pd.to_numeric(df_rows[19], errors='coerce')
        df_rows[20] = pd.to_numeric(df_rows[20], errors='coerce')
        df_rows[21] = pd.to_numeric(df_rows[21], errors='coerce')
        df_rows[22] = pd.to_numeric(df_rows[22], errors='coerce')
        df_rows[23] = pd.to_numeric(df_rows[23], errors='coerce')
        df_rows.drop(
            df_rows.columns[[4, 5, 6, 9, 10, 11, 12]], axis=1, inplace=True)
        df_rows.set_axis(['ratio', 'ruta', 'start', 'end', 'tripDuration', 'parkingDuration', 'timeStart', 'xStart', 'yStart', 'timeEnd',
                          'xEnd', 'yEnd', 'mileage', 'avSpeed', 'maxSpeed', 'consumed', 'avComsumed', 'date', 'week', 'month', 'tag'], axis=1, inplace=True)
        tripProduction.extend(df_rows.to_dict(orient='records'))
    return tripProduction
# sdk.logout()
