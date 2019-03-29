import pprint
import requests
from dateutil.parser import parse

class YahooWeatherForecast:

    def __init__(self):
        self._city_cache = {}

    def get(self, city):
        if city in self._city_cache:
            return self._city_cache[city]
        url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&dt=&units=metric&APPID=da6ec9481ed461ee397cd64c78f4b23c"
        print("Sending HTTP request")
        data = requests.get(url).json()
        forecast = {}
        forecast["city"] = data["city"]["name"]
        forecast["list"] = []
        for date in data["list"]:
            forecast["list"].append({"dt": parse(date["dt_txt"]),
                                       "temp_max": date["main"]["temp_max"],
                                       "temp_min": date["main"]["temp_min"]})
        self._city_cache[city] = forecast
        return forecast

class CityInfo():

    def __init__(self, city, weather_forecast=None):
        self.city = city
        self._weather_forecast = weather_forecast or YahooWeatherForecast()

    def weather_forecast(self):
        return self._weather_forecast.get(self.city)

def _main():
    weather_forecast = YahooWeatherForecast()
    forecast = CityInfo("Kiev", weather_forecast)
    pprint.pprint(forecast.weather_forecast())

if __name__ == "__main__":
    _main()