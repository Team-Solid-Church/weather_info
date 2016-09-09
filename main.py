from sys import argv
import datetime
import json
import os

import requests
import sys


def save_location(city, country):
    with open('saved_state/save.json', 'w') as json_file:
        json.dump([city, country], json_file)


def load_saved_state():
    with open('saved_state/save.json', 'r') as json_file:
        data = json.load(json_file)
    return (data[0], data[1])


def get_location():
    city = input("What city? > ")
    country = input ("What country code? > ")
    user_input = input('Do you want to save that location? Y or N ')
    if user_input.lower() == 'y':
        save_location(city, country)
    return (city, country)


def get_weather(payload, forecast_length='1'):
    """
    Fetches the weather information and returns a python dictionary.

    Params:
        payload = The data to be sent in the API request
        forecast_length = 1 for current, 2 for five day
    """
    #fetching data from API
    if forecast_length == '1':
        api_url = "http://api.openweathermap.org/data/2.5/weather"
    elif forecast_length == '2':
        api_url = "http://api.openweathermap.org/data/2.5/forecast/weather"

    r = requests.get(api_url, params=payload)
    return r.json()


def main():
    try:
        api_key = argv[1]
    except IndexError:
        print('Please pass in an API key')
        sys.exit(0)

    payload = {
        "appid": api_key,
        "q": ';assdf',
        "units": "imperial",
    }

    #start with user setting location
    if os.path.exists('saved_state/save.json'):
        city, country = load_saved_state()
        user_input = input('Do you want to see the weather for {}, {}? Y or N '
                           .format(city, country))
        if user_input.lower() == 'n':
            city, country = get_location()
    else:
        print('Error: file not found')
        city, country = get_location()

    payload["q"] = city + "," + country


    '''
    #error check for real city
    if  weather["cod"] == "404":
        print ("That is not a real city.")
    '''

    print('City = {}\nCountry = {}'.format(city, country))

    while True:
        #1 day vs 5 day forecast
        print("\n1 = Current Forecast")
        print("2 = Five Day Forecast")
        print("0 = Exit")
        forecast_length = input("> ")

        #exit program
        if forecast_length =="0":
            sys.exit(0)

        weather = get_weather(payload, forecast_length)

        #1day
        if forecast_length == "1":
            print ("\nCurrent Weather: ")
            print("\tTemperature: " + str(weather["main"]["temp"]))
            print("\tHumidity: " + str(weather["main"]["humidity"]))
            print("\tDescription: " + str(weather["weather"][0]["description"]))
            print("\tWind Speed: " + str(weather["wind"]["speed"]))

        #5 day
        elif forecast_length == "2":
            print("Five Day Forecast:")
            # TODO: Just do a function
            days_only = [entry for entry in weather["list"]
                         if "11:" in datetime.datetime.fromtimestamp(
                             int(entry["dt"])).strftime('%Y-%m-%d %H: %M: %S')
                         ]
            for day in days_only:
                date = datetime.datetime.fromtimestamp(
                    int(day["dt"])
                ).strftime('%Y-%m-%d')
                print("\tDay: " + str(date))
                print("\t\tTemperature: " + str(day["main"]["temp"]))
                print("\t\tHumidity: " + str(day["main"]["humidity"]))
                print("\t\tDescription: " + str(day["weather"][0]["description"]))
                print("\t\tWind Speed: " + str(day["wind"]["speed"]))



if __name__ == '__main__':
    main()
