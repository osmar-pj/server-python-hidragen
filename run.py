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
    arrA = []
    arrB = []

    for u in units['items']:
        unit = u['id']
        dfDay = getBasicData(start, end, unit)
        dfA, dfB = getGroup(unit)
        dfDay['nm'] = u['nm']
        dfA['nm'] = u['nm']
        dfB['nm'] = u['nm']
        arrDay.extend(dfDay.to_dict(orient='records'))
        arrA.extend(dfA.to_dict(orient='records'))
        arrB.extend(dfB.to_dict(orient='records'))
    df_rutaA = pd.DataFrame(arrA)
    df_rutaB = pd.DataFrame(arrB)

    df_rutaA['date'] = df_rutaA['timestampBegin'].apply(
        lambda x: datetime.fromtimestamp(x).date())
    df1 = df_rutaA.query('nm == "BBA-880"').query('consumed < 20')
    df2 = df_rutaA.query('nm == "BBB-850"').query('consumed < 20')
    df3 = df_rutaA.query('nm == "BBC-924"')
    df4 = df_rutaA.query('nm == "BBC-929"')

    df_ahorro1 = pd.merge(df1, df2, on=['trip', 'date'])
    df_ahorro1['ahorro'] = (df_ahorro1['consumed_x'] -
                            df_ahorro1['consumed_y'])
    df_ahorro1['week'] = pd.to_datetime(df_ahorro1['date']).dt.strftime('w %U')
    df_ahorro1['ahorro'].replace([np.inf, -np.inf], np.nan, inplace=True)
    df_ahorro1.dropna(inplace=True)
    df_ahorro1 = df_ahorro1.groupby(['week']).sum()
    df_ahorro1.reset_index(inplace=True)
    df_ahorro1 = df_ahorro1[['week', 'ahorro']]

    df_ahorro2 = pd.merge(df3, df4, on=['trip', 'date'])
    df_ahorro2['ahorro'] = (df_ahorro2['consumed_x'] -
                            df_ahorro2['consumed_y'])
    df_ahorro2['week'] = pd.to_datetime(df_ahorro2['date']).dt.strftime('w %U')
    df_ahorro2['ahorro'].replace([np.inf, -np.inf], np.nan, inplace=True)
    df_ahorro2.dropna(inplace=True)
    df_ahorro2 = df_ahorro2.groupby(['week']).sum()
    df_ahorro2.reset_index(inplace=True)
    df_ahorro2 = df_ahorro2[['week', 'ahorro']]

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
    df_week = df_week.merge(df_ahorro1, how='inner', on='week').merge(
        df_ahorro2, how='inner', on='week', suffixes=('_BBB850', '_BBC929'))
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
# schedule.every().saturday.at("00:01").do(updateData)
schedule.every().day.at("11:08").do(updateStat)
schedule.every().day.at("11:08").do(updateData)

"""
 [{'nm': 'BBA-880', 'cls': 2, 'id': 10293, 'mu': 3, 'uacl': 19327369763},
  {'nm': 'BBB-850', 'cls': 2, 'id': 10267, 'mu': 3, 'uacl': 19327369763},
  {'nm': 'BBC-924', 'cls': 2, 'id': 10277, 'mu': 3, 'uacl': 19327369763},
  {'nm': 'BBC-929', 'cls': 2, 'id': 10265, 'mu': 3, 'uacl': 19327369763}]}
"""


while True:
    schedule.run_pending()
    time.sleep(1)
