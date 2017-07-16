#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import datetime

def data_parsing(data):
    newlist = []
    status = ""
    timestamp = data["currently"]["time"]
    date = datetime.datetime.utcfromtimestamp(timestamp)
    
    #time = date.strftime("%H:%M")
    #day = date.strftime("%a")
    time = "00:00"
    day = "Mon"
    
    
    # check if current time is 06:00 am
    if time == "06:00":
    
        d = date.strftime("%d.%m")
        hourly_summary = data["hourly"]["summary"]
        tMin = temp(data["daily"]["data"][0]["temperatureMin"])
        tMax = temp(data["daily"]["data"][0]["temperatureMax"])
        direction = "ЮЗЗ"#degree_to_direction(data["daily"]["data"][0]["windBearing"])
        speed = data["daily"]["data"][0]["windSpeed"]
        gust = data["daily"]["data"][0]["windGust"]
        humidity = (int)(data["daily"]["data"][0]["humidity"] * 100)
        status = "{}\n{}\n{}...{}\nВетер {} {}м/с, порывы {}м/с\nВлажность {}%".format(d, hourly_summary, tMin, tMax, direction, speed, gust, humidity)
        
    # check if current time is 12:00 pm or 6:00 pm
    elif time == "12:00" or time == "18:00":
        # check if current weekday is Monday, Wednesday or Friday
        if time == "12:00" and (day == "Mon" or day== "Wed" or day == "Fri"):
            status = data["daily"]["summary"]
        else:
            print("started")
            t= temp(data["currently"]["temperature"])
            hourly_summary = data["hourly"]["summary"].lower()
            direction = "ЮЗЗ"#degree_to_direction(data["daily"]["data"][0]["windBearing"])
            speed = data["currently"]["windSpeed"]
            gust = data["currently"]["windGust"]
            humidity = (int)(data["currently"]["humidity"] * 100)
            
            status = "{}\n{}, {}\nВетер {} {}м/c, порывы {}м/с, влажность {}%".format(time, t, hourly_summary, direction, speed, gust, humidity)
    else:
        summary = data["currently"]["summary"]
        summary = summary[0] + summary[1:].lower()
        t= temp(data["currently"]["temperature"])
        tAp = temp(data["currently"]["apparentTemperature"])
        direction = "ЮЗЗ"#degree_to_direction(data["daily"]["data"][0]["windBearing"])
        speed = data["currently"]["windSpeed"]
        gust = data["currently"]["windGust"]
        humidity = (int)(data["currently"]["humidity"] * 100)
        status = "{}\n{}, {}, ощущается как {}, ветер {} {}м/с, порывы {}м/с, влажность {}%".format(time, summary, t, tAp, direction, speed, gust, humidity)
    
    # append status to newlist
    newlist.append(status)
    
    # check if wind alert
        # append wind alert status to newlist
    
    return newlist
    
def temp(t):
    temp = ""
    if t > 0:
        temp += "+"
    return temp + str(round(t))