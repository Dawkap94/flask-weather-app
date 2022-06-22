from datetime import datetime
import requests
import webbrowser

def check_city(city_name: str):
    url = requests.get(
        f"http://api.openweathermap.org/geo/1.0/direct?q={city_name}&limit=5&appid=2710484a6f4fe1e0870d0df45afff109")
    city_dict = url.json()
    lat = city_dict[0]["lat"]
    lon = city_dict[0]["lon"]
    return lat, lon


def check_weather(lat, lon, day):
    url = "https://community-open-weather-map.p.rapidapi.com/forecast/daily"
    querystring = {"lat": f"{lat}", "lon": f"{lon}", "cnt": "5", "units": "metric"}
    headers = {
        "X-RapidAPI-Host": "community-open-weather-map.p.rapidapi.com",
        "X-RapidAPI-Key": "2c3490a5a5msh7b8251db5d10e6dp18b803jsna62957589597"
    }
    response = requests.request("GET", url, headers=headers, params=querystring)
    data = response.json()
    weather_dict = {}

    for elem in data["list"]:
        weather_dict[datetime.utcfromtimestamp(elem["dt"]).strftime('%Y-%m-%d')] = elem["weather"][0]["main"]

    return weather_dict[day]

def check_celcius(lat, lon, day):
    url = "https://community-open-weather-map.p.rapidapi.com/forecast/daily"
    querystring = {"lat": f"{lat}", "lon": f"{lon}", "cnt": "5", "units": "metric"}
    headers = {
        "X-RapidAPI-Host": "community-open-weather-map.p.rapidapi.com",
        "X-RapidAPI-Key": "2c3490a5a5msh7b8251db5d10e6dp18b803jsna62957589597"
    }
    response = requests.request("GET", url, headers=headers, params=querystring)
    data = response.json()
    weather_dict = {}

    for elem in data["list"]:
        weather_dict[datetime.utcfromtimestamp(elem["dt"]).strftime('%Y-%m-%d')] = elem["temp"]

    return weather_dict[day]


def main():

    city_name, day = input("For which city do you want to check the weather? "), input(
        "For which day? Format YYYY-MM-DD: ")
    latitude, longitude = check_city(city_name)

    print(f"The weather for city coordinates:{latitude, longitude} is: {check_weather(latitude, longitude, day)}, the"
          f" celcius is {check_celcius(latitude, longitude, day)} ")

    webbrowser.open(f'https://www.google.com/maps/place/50%C2%B002\'01.2%22N+19%C2%B015\'36.3%22E/@{latitude},{longitude},17z')

#
# if __name__ == '__main__':
#     main()
