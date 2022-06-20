import pytest
from pogoda import check_weather, check_city, check_celcius

def test_check_city_numbers():
    with pytest.raises(IndexError):
        check_city(121212)

def test_check_city_wrong_name():
    with pytest.raises(IndexError):
        check_city("1j189dj19dh21j98dh12j98dj129d8j1298")

def test_check_city_list():
    with pytest.raises(KeyError):
        check_city([1,2,3,4,5])

#London coordinates is: 51.5073219, -0.1276474
def test_check_city_London():
    result = check_city("London")
    assert result == (51.5073219, -0.1276474)

def test_check_weather_string():
    with pytest.raises(KeyError):
        check_weather("12", "121", "121")

