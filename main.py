from sys import argv, exit
import requests


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

    #fetching data from API
    r = requests.get("http://api.openweathermap.org/data/2.5/weather",
                     params=payload)
    weather = r.json()
    
    #error check for real city    
    if  weather["cod"] == "404":
        print ("That is not a real city.")

    while True:
        #1 day vs 5 day forecast   
        print("\n1 = Current Forecast")
        print("2 = Five Day Forecast")    
        forecast_length = input("> ")
        #1day
        if forecast_length == "1":
            print ("\nCurrent Weather: ")
            print("\tTemperature: " + str(weather["main"]["temp"]))
            print("\tHumidity: " + str(weather["main"]["humidity"]))
            print("\tDescription: " + str(weather["weather"] [0] ["description"]))
            print("\tWind Speed: " + str(weather["wind"]["speed"]))

        #5 day
        elif forecast_length == "2":
            pass


    # print("Current Temp: {}".format(weather["main"]["temp"]))

if __name__ == '__main__':
    main()
