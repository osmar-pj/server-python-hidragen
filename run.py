from calendar import month
import schedule
import time
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
from getBasicData import getBasicData
from getGroup import getGroup
from getUnit import getUnits


def updateData():
    print('starting...')
    start = datetime.now() - timedelta(weeks=5)
    end = datetime.now()
    # unit = 10265

    units = getUnits()
    arrDay = []

    for u in units['items']:
        unit = u['id']
        dfDay = getBasicData(start, end, unit)
        dfDay['nm'] = u['nm']
        arrDay.extend(dfDay.to_dict(orient='records'))

    df = pd.DataFrame(arrDay)
    idx = (df['consumed'] != 0) & (
        df['consumed'] < 100) & (df['engineHours'] < 100)
    df = df.loc[idx]
    df['week'] = pd.to_datetime(df['date']).dt.strftime('w %U')
    df.to_csv('df_tag.csv', index=False)
    df_date = df.groupby(['date']).agg({'parkingHours': 'sum', 'engineHours': 'sum', 'mileage': 'sum',
                                        'avgSpeed': 'mean', 'maxSpeed': 'mean', 'consumed': 'sum', 'avgConsumed': 'mean', 'nm': ','.join})
    df_date.reset_index(inplace=True)
    df_date['week'] = df_date['date'].dt.strftime('w %U')
    df_date.to_csv('df_date.csv', index=False)
    # df_date = df.groupby(['date']).agg({'parkingHours': lambda x: list(x), 'engineHours': lambda x: list(x), 'mileage': lambda x: list(
    #     x), 'avgSpeed': lambda x: list(x), 'maxSpeed': lambda x: list(x), 'consumed': lambda x: list(x), 'avgConsumed': lambda x: list(x), 'nm': lambda x: list(x)})
    # df_date.reset_index(inplace=True)

    df_week = df.groupby(['week']).agg({'parkingHours': 'sum', 'engineHours': 'sum', 'mileage': 'sum',
                                        'avgSpeed': 'mean', 'maxSpeed': 'mean', 'consumed': 'sum', 'avgConsumed': 'mean'})
    df_week.reset_index(inplace=True)

    df_week.to_csv('df_week.csv', index=False)
    return


def updateStat():
    print('starting... STATSTTTSTATSTTATST')
    start = datetime.now() - timedelta(weeks=5)
    end = datetime.now()
    units = getUnits()
    arrA = []
    arrB = []
    arrDay = []

    for u in units['items']:
        unit = u['id']
        dfA, dfB = getGroup(unit)
        dfDay = getBasicData(start, end, unit)
        dfDay['nm'] = u['nm']
        dfA['nm'] = u['nm']
        dfB['nm'] = u['nm']
        arrDay.extend(dfDay.to_dict(orient='records'))
        arrA.extend(dfA.to_dict(orient='records'))
        arrB.extend(dfB.to_dict(orient='records'))
    df_rutaA = pd.DataFrame(arrA)
    df_rutaB = pd.DataFrame(arrB)
    df_rutaA.to_csv('df_rutaA.csv', index=False)
    df_rutaB.to_csv('df_rutaB.csv', index=False)
    df = pd.DataFrame(arrDay)
    idx = (df['consumed'] != 0) & (
        df['consumed'] < 100) & (df['engineHours'] < 100)
    df = df.loc[idx]
    df['week'] = pd.to_datetime(df['date']).dt.strftime('w %U')
    df.to_csv('df_tag.csv', index=False)
    df_date = df.groupby(['date']).agg({'parkingHours': 'sum', 'engineHours': 'sum', 'mileage': 'sum',
                                        'avgSpeed': 'mean', 'maxSpeed': 'mean', 'consumed': 'sum', 'avgConsumed': 'mean', 'nm': ','.join})
    df_date.reset_index(inplace=True)
    df_date['week'] = df_date['date'].dt.strftime('w %U')
    df_date.to_csv('df_date.csv', index=False)
    return


# updateData()
schedule.every().saturday.at("00:01").do(updateData)
schedule.every().day.at("00:15").do(updateStat)

"""
 [{'nm': 'BBA-880', 'cls': 2, 'id': 10293, 'mu': 3, 'uacl': 19327369763},
  {'nm': 'BBB-850', 'cls': 2, 'id': 10267, 'mu': 3, 'uacl': 19327369763},
  {'nm': 'BBC-924', 'cls': 2, 'id': 10277, 'mu': 3, 'uacl': 19327369763},
  {'nm': 'BBC-929', 'cls': 2, 'id': 10265, 'mu': 3, 'uacl': 19327369763}]}
"""


while True:
    schedule.run_pending()
    time.sleep(1)
