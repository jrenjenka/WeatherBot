#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import requests
import datetime
import pytz

# from config import WAPI_key

def lookup():
    """Make HTTPS request for weather data"""
    
    # ensure environment variables are set
    if not os.environ.get("WAPI_key"):
        raise RuntimeError("WAPI_key not set")
    
    # make HTTPS request
    try:
        url = "https://api.darksky.net/forecast/{}/55.75,37.62?lang=ru&units=si".format(os.environ.get("WAPI_key"))
        response = requests.get(url)
        if response.status_code == 200:
            json_data = response.json()
            
            # return parsed data for bot
            return data_parsing(json_data)
        else: return None
    
    except:
        return None
        
def data_parsing(data):
    """parse weather data and return list of statuses for bot"""
    
    # create new list for statuses
    datalist = []
    status = ""
    
    # fetch timestamp of current weather data and convert it to date
    timestamp = data["currently"]["time"]
    date = datetime.datetime.utcfromtimestamp(timestamp)
    
    # great thanks to solution of converting utc time to local time https://stackoverflow.com/posts/13287083/revisions
    local_tz = pytz.timezone('Europe/Moscow')
    local_date = date.replace(tzinfo=pytz.utc).astimezone(local_tz)
    time = local_date.strftime("%H:%M")
    day = local_date.strftime("%a")
    tm = int(time[0:2])
    
    # check if current time is 06:00 am
    if tm == 6:
        
        # fetch daily weather data for tweet
        d = date.strftime("%d.%m")
        s = data["hourly"]["summary"]
        tMin = temp(data["daily"]["data"][0]["temperatureMin"])
        tMax = temp(data["daily"]["data"][0]["temperatureMax"])
        ws = data["daily"]["data"][0]["windSpeed"]
        h = (int)(data["daily"]["data"][0]["humidity"] * 100)
        
        if ws != "0.0" or ws != None:
            wd = degree_to_direction(data["daily"]["data"][0]["windBearing"])
            wg = data["daily"]["data"][0]["windGust"]
            status = "{}\n{}\n{}...{}\nВетер {} {}м/с, порывы {}м/с\nВлажность {}%".format(d, s, tMin, tMax, wd, ws, wg, h)
        else: 
            status = "{}\n{}\n{}...{}\nВетра нет\nВлажность {}%".format(d, s, tMin, tMax, h)
   
    # check if current time is 12:00 pm or 6:00 pm
    elif tm == 12 or tm == 18:
        
        # check if current weekday is Monday, Wednesday or Friday
        if tm == 12 and (day == "Mon" or day== "Wed" or day == "Fri"):
            status = data["daily"]["summary"]
        else:
            
            # fetch hourly weather data for tweet
            t= temp(data["currently"]["temperature"])
            s = data["hourly"]["summary"].lower()
            ws = data["currently"]["windSpeed"]
            h = (int)(data["currently"]["humidity"] * 100)
            
            if ws != "0.0" or ws != None:
                wd = degree_to_direction(data["currently"]["windBearing"])
                wg = data["currently"]["windGust"]
                status = "{}\n{}, {}\nВетер {} {}м/c, порывы {}м/с, влажность {}%".format(time, t, s, wd, ws, wg, h)
            else: 
                status = "{}\n{}, {}\nВетра нет, влажность {}%".format(time, t, s, h)
            
    else:
        # fetch currently weather data for tweet
        s = data["currently"]["summary"]
        s = s[0] + s[1:].lower()
        t= temp(data["currently"]["temperature"])
        tAp = temp(data["currently"]["apparentTemperature"])
        ws = data["currently"]["windSpeed"]
        h = (int)(data["currently"]["humidity"] * 100)
        
        if ws != "0.0" or ws != None:
            wd = degree_to_direction(data["currently"]["windBearing"])
            wg = data["currently"]["windGust"]
            status = "{}\n{}, {}, ощущается как {}, ветер {} {}м/с, порывы {}м/с, влажность {}%".format(time, s, t, tAp, wd, ws, wg, h)
        else: 
            status = "{}\n{}, {}, ощущается как {}, ветра нет, влажность {}%".format(time, s, t, tAp, h)
            
    # append status to datalist
    datalist.append(status)
    
    # check if wind alert
    wa = wind_alert(data["currently"]["windSpeed"], data["currently"]["windGust"])
    if wa != None:
        # append wind alert status to newlist
        datalist.append(wa)
        
    # return list of statuses    
    return datalist
    
# convert wind degree to direction
def degree_to_direction(degree):
    """Return wind direction"""
    
    if degree != None:
        if degree >= 348.75 or degree <= 11.25:
            return "С"
        elif degree <= 33.75:
            return "ССВ"
        elif degree <= 56.25:
            return "СВ"
        elif degree <= 78.75:
            return "ВСВ"
        elif degree <= 101.25:
            return "В"
        elif degree <= 123.75:
            return "ВЮВ"
        elif degree <= 146.25:
            return "ЮВ"
        elif degree <= 168.75:
            return "ЮЮВ"
        elif degree <= 191.25:
            return "Ю"
        elif degree <= 213.75:
            return "ЮЮЗ"
        elif degree <= 236.25:
            return "ЮЗ"
        elif degree <= 258.75:
            return "ЗЮЗ"
        elif degree <= 281.25:
            return "З"
        elif degree <= 303.75:
            return "ЗСЗ"
        elif degree <= 326.25:
            return "СЗ"
        elif degree > 326.25:
            return "ССЗ"
        
    return None

# check if there is strong wind
def wind_alert(wind_speed, wind_gust):
    """Return string with alert if there is strong wind"""
    
    if wind_speed == 0.0 or wind_speed == None:
        return None
        
    alert = ""
    
    if wind_gust >= 25 and wind_speed < 10.7: 
        alert = "шквалистый ветер" 
        return "Будьте осторожны, {}, скорость {}м/c с порывами {}м/с".format(alert, wind_speed, wind_gust)
    
    if wind_speed < 10.7 and wind_gust < 25:
        return None
    elif wind_speed <= 13.8: 
        alert = "усиление ветра в Москве"
    elif wind_speed <= 17.1:
        alert = "сильный ветер"
    elif wind_speed <= 20.7:
        alert = "очень сильный ветер"
    elif wind_speed <= 24.4:
        alert = "штормовой ветер"
    elif wind_speed <= 28.4:
        alert = "сильный штормовой ветер"
    elif wind_speed <= 32.6:
        alert = "очень сильный штормовой ветер"
    else:
        alert = "ураганный ветер"
        
    return "Будьте осторожны, {}, скорость {}м/c с порывами {}м/с".format(alert, wind_speed, wind_gust)

# add temperature sign to degree
def temp(t):
    """convert float to string and add sign to temperature degree"""
    
    temp = ""
    if t > 0:
        temp += "+"
    return temp + str(round(t))
