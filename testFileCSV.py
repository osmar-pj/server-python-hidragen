import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from getUnit import getUnits
from datetime import datetime, timedelta
from getGroup import getGroup
from getLastTrips import getLastTrips
from getBasicData import getBasicData
import json

# TEST RUTAS A y B

# units = getUnits()
# arrA = []
# arrB = []

# for u in units['items']:
#     unit = u['id']
#     dfA, dfB = getGroup(unit)
#     dfA['nm'] = u['nm']
#     dfB['nm'] = u['nm']
#     arrA.extend(dfA.to_dict(orient='records'))
#     arrB.extend(dfB.to_dict(orient='records'))
# df_rutaA = pd.DataFrame(arrA)
# df_rutaB = pd.DataFrame(arrB)
# df_rutaA.to_csv('df_rutaA.csv', index=False)
# df_rutaB.to_csv('df_rutaB.csv', index=False)


# ?????????????/?????????????????????
# RUTAS COMPLETAS PARA DASHBOARD

# units = getUnits()
# arr = []
# for u in units['items']:
#     unit = u['id']
#     dfLastTrips = getLastTrips(unit)
#     dfLastTrips['nm'] = u['nm']
#     arr.append(dfLastTrips.to_dict(orient='records'))
# df = pd.DataFrame(arr)
# df.rename(columns={0: 'rutaA', 1: 'rutaB'}, inplace=True)
# df.to_csv('df_lasttrips.csv', index=False)
# df1 = pd.read_csv('df_lasttrips.csv')
# arr1 = df1.to_dict('tight')['data']
# convert to json

# # RUTAS
# dfA = pd.read_csv('df_rutaA.csv')
# dfB = pd.read_csv('df_rutaB.csv')
# dfA['date'] = dfA['timestampBegin'].apply(
#     lambda x: datetime.fromtimestamp(x).date())
# # dfB['date'] = dfB['timestampBegin'].apply(
# #     lambda x: datetime.fromtimestamp(x).date())
# timeFilter = datetime.now() - timedelta(days=7)
# idxa = dfA['timestampBegin'] >= timeFilter.timestamp()
# dfA = dfA[idxa]
# idxb = dfB['timestampBegin'] >= timeFilter.timestamp()
# dfB = dfB[idxb]

start = datetime.now() - timedelta(weeks=6)
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

df_date = df.groupby(['date']).agg({'parkingHours': 'sum', 'engineHours': 'sum', 'mileage': 'sum',
                                    'avgSpeed': 'mean', 'maxSpeed': 'mean', 'consumed': 'sum', 'avgConsumed': 'mean', 'nm': ','.join})
df_date.reset_index(inplace=True)
df_date['week'] = df_date['date'].dt.strftime('w %U')
df_week = df.groupby(['week']).agg({'parkingHours': 'sum', 'engineHours': 'sum', 'mileage': 'sum',
                                    'avgSpeed': 'mean', 'maxSpeed': 'mean', 'consumed': 'sum', 'avgConsumed': 'mean'})
df_week.reset_index(inplace=True)

df_week = df_week.merge(df_ahorro1, how='inner', on='week').merge(
    df_ahorro2, how='inner', on='week', suffixes=('_BBB850', '_BBC929'))


# CODIGO DE APP.PY GETWEEK OLD
# dfw = pd.read_csv('df_week.csv').tail(4).reset_index().T.reset_index()
# dfw = dfw[1:]
# dfw.rename(columns={'index': 'label', 0: 'w1',
#             1: 'w2', 2: 'w3', 3: 'w4'}, inplace=True)

# # NUEVO
# dfw = pd.read_csv('df_week.csv')
#     # dfw.rename(columns={'parkingHours': 'Horas de parqueo (h): ', 'engineHours': 'Horas de motor (h): ', 'mileage': 'Kilometraje (km): ', 'avfSpeed': 'Velocidad Inst. (km/h): ', 'maxSpeed': 'Velocidad Max (km/h): ',
#     #            'consumed': 'Consumo combustible (gal): ', 'avgConsumed': 'Rendimiento (km/gal): ', 'ahorro_BBB850': 'Ahorro BBB-850 (%): ', 'ahorro_BBC929': 'Ahorro BBC-929 (%): '}, inplace=True)
# dfw.tail(4).reset_index().T.reset_index()
# dfw = dfw[1:]
# dfw.rename(columns={'index': 'label', 0: 'w1',
#         1: 'w2', 2: 'w3', 3: 'w4'}, inplace=True)
