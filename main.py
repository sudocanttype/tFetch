
import json
import math
import os
import time
import datetime
import subprocess

import requests
from dotenv import load_dotenv

load_dotenv()

def getWeather(apikey, location, apiUnits):
    #extract dat data
    data = requests.get('https://api.openweathermap.org/data/2.5/weather?q='+location+'&units='+apiUnits+'&appid='+apikey).text
    data = json.loads(data)
    weather = data['weather'][0]['description']
    weatherID = str(data['weather'][0]['id'])
    weatherIconFromSource = str(data['weather'][0]['icon'])
    temp_feels = data['main']['feels_like']
    temp_actual = math.ceil((data['main']['temp']))
    humidity = str(data['main']['humidity']) + "%"



    #check by first number for weather condition codes https://openweathermap.org/weather-conditions
    #I know, theres prob a better way of doing this, but eh it works

    if weatherID[0]  == "2":
        if weatherID == "202 "or weatherID == "212":
            weatherIcon = ""
        else:
            weatherIcon = ""
    elif weatherID[0]  == "3":
        weatherIcon = ""
    elif weatherID[0] == "5":
        if weatherID == "502 "or weatherID == "503 "or weatherID == "504 "or weatherID == "522":
            weatherIcon = ""
        else:
            weatherIcon = ""
    elif weatherID[0] == "6":
        weatherIcon = ""
    elif weatherID[0] == "7":
        weatherIcon = ''
    elif weatherID == "800":
        weatherIcon = ''
    elif weatherID[0] == "8":
        weatherIcon = ''
    else:
        weatherIcon = weatherIconFromSource

    return {
        'weather':weather,
        'weatherID':weatherID,
        'temp_feels':temp_feels,
        'temp_actual':temp_actual,
        'humidity':humidity,
        'weatherIcon':weatherIcon

    }

def get_time():
    return datetime.datetime.now().strftime('%A, %B %d %I:%M:%S %p %Z')

def get_i3_workspaces():
    #i3-msg returns a string json

    active_workspaces = []
    i3output = subprocess.check_output('i3-msg -t get_workspaces', stderr=subprocess.STDOUT, shell=True)
    dict_output = json.loads(i3output)

    for i in dict_output:
        active_workspaces.append(str(i['num']))

    return ", ".join(active_workspaces)

def init_weather():
    apikey = os.getenv("API")
    location = 'houston'
    apiUnits = 'imperial' #for us filthy americans
    #wait a couple seconds on run, because for some reason without this it returns HTTPSConnectionPool Max retries exceeded
    #also added fallback because it would give errors

    try:
        info = getWeather(apikey, location, apiUnits)
    except Exception as e:
        print(e)
        exit(1)

    return info


if __name__ == "__main__":

    weatherInfo = init_weather()
    print(f"Time: {get_time()}")
    print()
    print(f"Weather: {weatherInfo['weatherIcon']}")
    print(f"Temperature: {weatherInfo['temp_actual']}°F")
    print(f"Feels Like Temperature: {weatherInfo['temp_feels']}°F")
    print(f"Humidity: {weatherInfo['humidity']}")
    print()
    print(f"Workspaces: {get_i3_workspaces()}")
