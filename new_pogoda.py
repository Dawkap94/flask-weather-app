from datetime import datetime
import requests


class GetLatLong:
    def __init__(self, city_name):
        self.city_name = city_name

    def get_lat_long_from_city(self, city_name):
        self.city_name = city_name
        url = requests.get(
            f"http://api.openweathermap.org/geo/1.0/direct?q={city_name}&limit=5&appid=2710484a6f4fe1e0870d0df45afff109")
        if url.status_code == 200:
            try:
                city_dict = url.json()
                lat = city_dict[0]["lat"]
                lon = city_dict[0]["lon"]
                return lat, lon
            except IndexError:
                return "Wystapil blad"
        else:
            return "Wystapil blad"


class CheckWeather:
    def __init__(self, lat, lon, date):
        self.lat = lat
        self.lon = lon
        self.date = date

    def get_weather_dict(self, date):
        url = "https://community-open-weather-map.p.rapidapi.com/forecast/daily"
        querystring = {"lat": f"{self.lat}", "lon": f"{self.lon}", "cnt": "5", "units": "metric"}
        headers = {
            "X-RapidAPI-Host": "community-open-weather-map.p.rapidapi.com",
            "X-RapidAPI-Key": "2c3490a5a5msh7b8251db5d10e6dp18b803jsna62957589597"
        }
        response = requests.request("GET", url, headers=headers, params=querystring)
        data = response.json()
        weather_dict = {}

        for elem in data["list"]:
            weather_dict[datetime.utcfromtimestamp(elem["dt"]).strftime('%Y-%m-%d')] = elem["weather"][0]["main"]

        return weather_dict[date]


class Temperature(CheckWeather):
    def __init__(self, lat, lon, date):
        super().__init__(lat, lon, date)

    def get_celcius_temp(self, date):
        url = "https://community-open-weather-map.p.rapidapi.com/forecast/daily"
        querystring = {"lat": f"{self.lat}", "lon": f"{self.lon}", "cnt": "5", "units": "metric"}
        headers = {
            "X-RapidAPI-Host": "community-open-weather-map.p.rapidapi.com",
            "X-RapidAPI-Key": "2c3490a5a5msh7b8251db5d10e6dp18b803jsna62957589597"
        }
        response = requests.request("GET", url, headers=headers, params=querystring)
        data = response.json()
        weather_dict = {}

        for elem in data["list"]:
            weather_dict[datetime.utcfromtimestamp(elem["dt"]).strftime('%Y-%m-%d')] = elem["temp"]

        return weather_dict[date]

    def get_fahrenheit_temp(self, date):
        url = "https://community-open-weather-map.p.rapidapi.com/forecast/daily"
        querystring = {"lat": f"{self.lat}", "lon": f"{self.lon}", "cnt": "5", "units": "metric"}
        headers = {
            "X-RapidAPI-Host": "community-open-weather-map.p.rapidapi.com",
            "X-RapidAPI-Key": "2c3490a5a5msh7b8251db5d10e6dp18b803jsna62957589597"
        }
        response = requests.request("GET", url, headers=headers, params=querystring)
        data = response.json()
        weather_dict = {}

        for elem in data["list"]:
            weather_dict[datetime.utcfromtimestamp(elem["dt"]).strftime('%Y-%m-%d')] = elem["temp"]

        for key, val in weather_dict[f"{date}"].items():
            weather_dict[f"{date}"][key] = round((val * 33.8), 2)

        return weather_dict[date]