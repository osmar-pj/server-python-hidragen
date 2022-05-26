import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
from getTripsFromMine import getTripsFromMine
from getTripsToMine import getTripsToMine
from getUnit import getUnits

"""
 [{'nm': 'BBA-880', 'cls': 2, 'id': 10293, 'mu': 3, 'uacl': 19327369763},
  {'nm': 'BBB-850', 'cls': 2, 'id': 10267, 'mu': 3, 'uacl': 19327369763},
  {'nm': 'BBC-924', 'cls': 2, 'id': 10277, 'mu': 3, 'uacl': 19327369763},
  {'nm': 'BBC-929', 'cls': 2, 'id': 10265, 'mu': 3, 'uacl': 19327369763}]}
"""

start = datetime(2022, 2, 10)
end = datetime(2022, 5, 10)
# unit = 10265

units = getUnits()
arrFromMine = []
arrToMine = []

for u in units['items']:
    unit = u['id']
    df1 = getTripsFromMine(start, end, unit)
    df2 = getTripsToMine(start, end, unit)
    df1['nm'] = u['nm']
    df2['nm'] = u['nm']
    arrFromMine.extend(df1.to_dict(orient='records'))
    arrToMine.extend(df2.to_dict(orient='records'))

df_fromMine = pd.DataFrame(arrFromMine)
df_toMine = pd.DataFrame(arrToMine)
idx_fromMine = (df_fromMine['consumed'] != 0) & (df_fromMine['consumed'] < 80)
idx_toMine = (df_toMine['consumed'] != 0) & (df_toMine['consumed'] < 80)
df_fm = df_fromMine.loc[idx_fromMine]
df_tm = df_toMine.loc[idx_toMine]
fig, ax = plt.subplots(figsize=(15, 5))
sns.lineplot(data=df_fm, ax=ax, x='datetimeBegin', y='consumed', hue='nm')
sns.lineplot(data=df_tm, ax=ax, x='datetimeBegin', y='consumed', hue='nm')

# pd.set_option('display.max_rows', None)
# pd.set_option('display.max_columns', None)

# df = getTripsFromMine(start, end, unit)
