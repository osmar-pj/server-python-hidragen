from main import login
from datetime import datetime, timedelta

"""
 [{'nm': 'BBA-880', 'cls': 2, 'id': 10293, 'mu': 3, 'uacl': 19327369763},
  {'nm': 'BBB-850', 'cls': 2, 'id': 10267, 'mu': 3, 'uacl': 19327369763},
  {'nm': 'BBC-924', 'cls': 2, 'id': 10277, 'mu': 3, 'uacl': 19327369763},
  {'nm': 'BBC-929', 'cls': 2, 'id': 10265, 'mu': 3, 'uacl': 19327369763}]}
"""
sdk = login()
parameterSetLocale = {
    'tzOffset': -18000,
    "language": "en"
}
sdk.render_set_locale(parameterSetLocale)

events = sdk.avl_evts()
