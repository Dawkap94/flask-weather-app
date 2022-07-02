import pytest
from new_pogoda import *
from app import DMY

# London coords
lat = 51.5073219
lon = -0.1276474
# Today date format "YYYY-MM-DD"
date = f"{DMY[2]}-{DMY[1]}-{DMY[0]}"


def test_GetLatLong_London():
    latlonobj = GetLatLong("London")
    latitude, longitude = latlonobj.get_lat_long_from_city("London")
    assert (latitude, longitude) == (51.5073219, -0.1276474)


def test_CheckWeather_result():
    weatherobj = CheckWeather(lat, lon, date)
    result = weatherobj.get_weather_dict(date)
    assert result == "Rain" or result == "Cloud" or result == "Clear"


def test_CheckWeather_wrong_city():
    with pytest.raises(KeyError):
        lat = 444444444444
        lon = -3333333333333
        weatherobj = CheckWeather(lat, lon, date)
        weatherobj.get_weather_dict(date)


def test_Temperature_return_dict():
    tempobj = Temperature(lat, lon, date)
    result = tempobj.get_celcius_temp(date)
    assert type(result) == dict


def test_Temperature_celcius_are_numbers():
    tempobj = Temperature(lat, lon, date)
    result = tempobj.get_celcius_temp(date)
    temp_list = [result[elem] for elem in result]
    for elem in temp_list:
        assert type(elem) == float or type(elem) == int


def test_Temperature_fahrenheit_are_numbers():
    tempobj = Temperature(lat, lon, date)
    result = tempobj.get_fahrenheit_temp(date)
    temp_list = [result[elem] for elem in result]
    for elem in temp_list:
        assert type(elem) == float or type(elem) == int
