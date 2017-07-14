# -*- coding: utf-8 -*-
import pyowm

from config import WAPI_key

city_id = 524901
owm = pyowm.OWM(WAPI_key, language='ru')
obs = owm.weather_at_id(city_id)

w = obs.get_weather()

print(w.get_temperature(unit='celsius'))
print(w.get_status())
print(w.get_detailed_status())


