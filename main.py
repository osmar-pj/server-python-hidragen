from datetime import datetime
# pip install wialon
from wialon.sdk import WialonSdk, WialonError, SdkException
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
"""
WialonSDK example usage
"""
# Initialize Wialon instance
sdk = WialonSdk(
    is_development=True,
    scheme='https',
    host='orf-monitor4.com'
)

try:
    # If you haven't a token, you should use our token generator
    token = '04bc3a31b5b56602a41049ef70682b8aC41E26716CAA92AC3983E481976D4E55D9A5EFC5'
    # https://goldenmcorp.com/resources/token-generator
    response = sdk.login(token)

    # sdk.logout()
except SdkException as e:
    print(f'Sdk related error: {e}')
except WialonError as e:
    print(f'Wialon related error: {e}')
except Exception as e:
    print(f'Python error: {e}')
