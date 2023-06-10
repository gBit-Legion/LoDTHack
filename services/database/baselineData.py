import requests
import re 

import time
from datetime import datetime
from loguru import logger
import pandas as pd

def removeEmoji(text):
    emoji_pattern = re.compile("["
            u"\U0001F600-\U0001F64F"  # emoticons
            u"\U0001F300-\U0001F5FF"  # symbols & pictographs
            u"\U0001F680-\U0001F6FF"  # transport & map symbols
            u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                            "]+", flags=re.UNICODE)
    return emoji_pattern.sub(r'', text) # no emoji

texts = pd.read_excel('Московский_постамат_Дата_cет_Этап_2.xlsx', engine='openpyxl')
addresses = pd.read_excel('Реестр домов_v11.xlsx', engine='openpyxl')

adress_index = 0
for label, series in texts.iterrows():
    if adress_index > len(addresses) - 3:
        adress_index = 0
    else:
        adress_index += 1

    text = series[0]
    date = series[1]
    date = date[:-6]
    mark = series[2]
    adress = addresses['Адрес'][adress_index]
    try:
        requests.post('http://178.170.196.251:8081/addReview/', 
                    json={
                        "usertext": removeEmoji(text),
                        "mark": mark,
                        "adress": adress,
                        "reviewdate": str(date),
                        "clusternumber": str(-999),
                        "classnumber": str(-999),
                        "article": 0,
                        "seller": "Anonimous Data",
                        "latitude": 0,
                        "longitude": 0
                    }
                )
    except Exception as e:
        logger.error(e)
        
    time.sleep(1)