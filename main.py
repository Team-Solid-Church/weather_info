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

    r = requests.get("http://api.openweathermap.org/data/2.5/weather",
                     params=payload)
 


    # print(r.url)
    weather = r.json()
    
    if  weather["cod"] == "404":
        print ("That is not a real city.")






    # print("Current Temp: {}".format(weather["main"]["temp"]))

if __name__ == '__main__':
    main()
