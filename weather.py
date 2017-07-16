#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import requests
import datetime

from config import WAPI_key

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
    
        
def data_parsing(data):
    newlist = []
    status = ""
    timestamp = data["currently"]["time"]
    date = datetime.datetime.utcfromtimestamp(timestamp)
    #time = date.strftime("%H:%M")
    #day = date.strftime("%a")
    time = "06:00"
    day = "Mon"
    
    
    # check if current time is 06:00 am
    if time == "06:00":
        d = date.strftime("%d.%m")
        hourly_summary = data["hourly"]["summary"]
        tempMin = temp(data["daily"]["data"][0]["temperatureMin"])
        tempMax = temp(data["daily"]["data"][0]["temperatureMax"])
        direction = "ЮЗЗ"#degree_to_direction(data["daily"]["data"][0]["windBearing"])
        speed = data["daily"]["data"][0]["windSpeed"]
        gust = data["daily"]["data"][0]["windGust"]
        humidity = (int)(data["daily"]["data"][0]["humidity"] * 100)
        
        status = "{}\n{}\n{}...{}\nВетер {} {}м/с, порывы {}м/с\nВлажность {}%".format(d, hourly_summary, tempMin, tempMax, direction, speed, gust, humidity)
    # check if current time is 12:00 pm or 6:00 pm
    else if time == "12:00" or time == "18:00":
        # check if current weekday is Monday, Wednesday or Friday
        if time == "12:00" and (day == "Mon" or day== "Wed" or day == "Fri"):
            status = ""
        else:
            status = ""
    else:
        status = ""
    
    # append status to newlist
    newlist.append(status)
    
    # check if wind alert
        # append wind alert status to newlist
    
    return newlist
        
def degree_to_direction():
    return

def is_wind_alert(wind_speed, wind_gust):
    return

def temp(t):
    temp = ""
    if t > 0:
        temp += "+"
    return temp + str(round(t))

l = lookup()
for s in l:
    print(s)
    print(len(s))
