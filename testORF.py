import pandas as pd
from getUnit import getUnits
from datetime import datetime, timedelta
from getGroupA import getGroupA

units = getUnits()
# dfLastTrips = getLastTrips(units['items'][0]['id'])
rutaA = []
rutaB = []
start = datetime.now() - timedelta(days=60)
end = datetime.now()
for u in units['items']:
    unit = u['id']
    dfRutaA, dfRutaB = getGroupA(start, end, unit)
    dfRutaA['nm'] = u['nm']
    dfRutaB['nm'] = u['nm']
    rutaA.extend(dfRutaA.to_dict(orient='records'))
    rutaB.extend(dfRutaB.to_dict(orient='records'))
dfA = pd.DataFrame(rutaA)
dfBC = pd.DataFrame(rutaB)
