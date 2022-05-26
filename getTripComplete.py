import pandas as pd
from main import login
from datetime import datetime, timedelta
from getResource import getResources

# BBB-850 = 10267

# unit = 10267


def getTripComplete(unit):
    start = datetime.now() - timedelta(days=5)
    end = datetime.now()
    sdk = login()
    resources = getResources()
    parameterSetLocale = {
        'tzOffset': -18000,
        "language": "en"
    }
    sdk.render_set_locale(parameterSetLocale)
    start = (datetime.now() - timedelta(days=5)).timestamp()
    end = datetime.now().timestamp()
    # print(end, start, datetime.now())
    unit = 10267
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
        'tableIndex': 2,
        'indexFrom': 0,
        'indexTo': reports['reportResult']['tables'][2]['rows'] * 3
    }
    rows = sdk.report_get_result_rows(paramsGetResultRows)
    dataRows = [r['c'] for r in rows]
    df_rows = pd.DataFrame(dataRows).tail(1)

    return df_rows

# sdk.logout()
