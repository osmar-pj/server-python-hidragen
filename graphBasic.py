import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
from getBasicData import getBasicData
from getGeofence import getGeoSaturno
from getUnit import getUnits

"""
 [{'nm': 'BBA-880', 'cls': 2, 'id': 10293, 'mu': 3, 'uacl': 19327369763},
  {'nm': 'BBB-850', 'cls': 2, 'id': 10267, 'mu': 3, 'uacl': 19327369763},
  {'nm': 'BBC-924', 'cls': 2, 'id': 10277, 'mu': 3, 'uacl': 19327369763},
  {'nm': 'BBC-929', 'cls': 2, 'id': 10265, 'mu': 3, 'uacl': 19327369763}]}
"""

start = datetime(2022, 2, 10)
end = datetime(2022, 5, 21, 23, 59, 59)
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

# df_week = df.groupby(['week']).agg({'parkingHours': lambda x: list(x), 'engineHours': lambda x: list(x), 'mileage': lambda x: list(
#     x), 'avgSpeed': lambda x: list(x), 'maxSpeed': lambda x: list(x), 'consumed': lambda x: list(x), 'avgConsumed': lambda x: list(x)})
# df_week.reset_index(inplace=True)
# # PARA INFORMACION DE TALLLER SATURNO CALCULAR LA DISPONIBILIDAD

# df_saturno = getGeoSaturno(start, end)
# df_saturno['disponibilidad'] = 24 - df_saturno['durationIn']
# df_saturno.groupby(['date']).agg(
#     {'durationIn': 'sum', 'parkingDuration': 'sum', 'nm': ' '.join})

# fig, ax = plt.subplots(figsize=(15, 5))
# sns.lineplot(data=df_day, ax=ax, x='day', y='consumed')

# fig, ax = plt.subplots(figsize=(15, 5))
# sns.barplot(data=df_week, ax=ax, x='week', y='consumed')
# pd.set_option('display.max_rows', None)
# pd.set_option('display.max_columns', None)

# df = getTripsFromMine(start, end, unit)
