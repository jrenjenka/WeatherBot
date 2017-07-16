#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import requests

from config import WAPI_key
from helpers import data_parsing

def lookup():
    # make HTTP request
    try:
        url = "https://api.darksky.net/forecast/{}/55.75,37.62?lang=ru&units=si".format(WAPI_key)
        response = requests.get(url)
        if response.status_code == 200:
            json_data = response.json()
            
            # return parsed data for bot
            return data_parsing(json_data)
        else: return None
    
    except:
        return None
    
def degree_to_direction():
    return

def is_wind_alert(wind_speed, wind_gust):
    return

# test
l = lookup()

for s in l:
    print(s)
    print(len(s))
