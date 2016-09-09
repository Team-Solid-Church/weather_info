from sys import argv, exit
import datetime

import requests


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
        exit(0)

    payload = {
        "appid": api_key,
        "q": ';assdf',
        "units": "imperial",
    }

    #start with user setting location
    city = input("What city? > ")
    country = input ("What country code? > ")
    payload ["q"] = city + "," + country

    '''
    #error check for real city
    if  weather["cod"] == "404":
        print ("That is not a real city.")
    '''
    while True:
        #1 day vs 5 day forecast
        print("\n1 = Current Forecast")
        print("2 = Five Day Forecast")
        forecast_length = input("> ")
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
            # TODO: Just do a function
            days_only = [entry for entry in weather["list"]
                         if "11:" in datetime.datetime.fromtimestamp(
                             int(entry["dt"])).strftime('%Y-%m-%d %H: %M: %S')
                         ]
            for day in days_only:
                date = datetime.datetime.fromtimestamp(
                    int(day["dt"])
                ).strftime('%Y-%m-%d')
                print(date)


    # print("Current Temp: {}".format(weather["main"]["temp"]))

if __name__ == '__main__':
    main()
