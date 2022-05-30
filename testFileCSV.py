import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from getUnit import getUnits
from datetime import datetime, timedelta
from getGroup import getGroup
from getLastTrips import getLastTrips
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

units = getUnits()
arr = []
for u in units['items']:
    unit = u['id']
    dfLastTrips = getLastTrips(unit)
    dfLastTrips['nm'] = u['nm']
    arr.append(dfLastTrips.to_dict(orient='records'))
df = pd.DataFrame(arr)
df.rename(columns={0: 'rutaA', 1: 'rutaB'}, inplace=True)
df.to_csv('df_lasttrips.csv', index=False)
# df1 = pd.read_csv('df_lasttrips.csv')
# arr1 = df1.to_dict('tight')['data']
# convert to json
