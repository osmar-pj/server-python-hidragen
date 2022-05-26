import pandas as pd
from main import login
from datetime import datetime, timedelta
from getResource import getResources
from getTripComplete import getTripComplete

# BBB-850 = 10267

# start = datetime.now() - timedelta(days=5)
# end = datetime.now()
# unit = 10265


def getLastTrips(unit):
    sdk = login()
    resources = getResources()
    parameterSetLocale = {
        'tzOffset': -18000,
        "language": "en"
    }
    sdk.render_set_locale(parameterSetLocale)
    start = (datetime.now() - timedelta(days=3))
    end = datetime.now()
    # print(end, start, datetime.now())
    paramsExecReport = {
        'reportResourceId': resources['items'][0]['id'],
        'reportTemplateId': 2,
        'reportObjectId': unit,
        'reportObjectSecId': 0,
        'reportObjectIdList': 0,
        'interval': {
            'from': int(start.timestamp()),
            'to': int(end.timestamp()),
            'flags': 0
        }
    }
    reports = sdk.report_exec_report(paramsExecReport)
    paramsGetResultRows = {
        'tableIndex': 0,
        'indexFrom': 0,
        'indexTo': reports['reportResult']['tables'][0]['rows']
    }
    rows = sdk.report_get_result_rows(paramsGetResultRows)
    dataRows = [r['c'] for r in rows]
    dfTrips = pd.DataFrame(dataRows).tail(2)
    dfTrips.rename(columns={0: 'ratio', 1: 'trip', 2: 'tripFrom', 3: 'tripTo', 4: 'timestampFrom', 5: 'timestampTo', 6: 'mileage',
                            7: 'tripDuration', 8: 'parkingDuration', 9: 'avgSpeed', 10: 'maxSpeed', 11: 'consumed', 12: 'avgConsumed'}, inplace=True)
    dfTrips['ratio'] = dfTrips['ratio'].apply(
        lambda x: x.split(' ')[0]).astype(float)
    dfTrips['mileage'] = dfTrips['mileage'].apply(
        lambda x: x.split(' ')[0]).astype(float)
    dfTrips['avgSpeed'] = dfTrips['avgSpeed'].apply(
        lambda x: x.split(' ')[0]).astype(int)
    dfTrips['maxSpeed'] = dfTrips['maxSpeed'].apply(
        lambda x: x['t'].split(' ')[0]).astype(int)
    dfTrips['consumed'] = dfTrips['consumed'].apply(
        lambda x: x.split(' ')[0]).astype(float)
    dfTrips['tripDuration'] = pd.to_numeric(dfTrips['tripDuration'])
    dfTrips['parkingDuration'] = pd.to_numeric(dfTrips['parkingDuration'])
    dfTrips['avgConsumed'] = dfTrips['avgConsumed'].apply(
        lambda x: x.split(' ')[0]).astype(float)
    dfTrips['timestampFrom'] = dfTrips['timestampFrom'].apply(lambda x: x['v'])
    # dfTrips['datetimeFrom'] = pd.to_datetime(
    #     dfTrips['datetimeFrom'].apply(lambda x: x['t']))
    dfTrips['timestampTo'] = dfTrips['timestampTo'].apply(lambda x: x['v'])
    # dfTrips['datetimeTo'] = pd.to_datetime(
    #     dfTrips['datetimeTo'].apply(lambda x: x['t']))

    return dfTrips

# sdk.logout()
