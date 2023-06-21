import datetime

from django.shortcuts import render
import requests

def index(request):
    api_key = 'Api_key'
    current_weather_url = 'https://api.openweathermap.org/data/2.5/weather?q={}&appid={}'

    #forecast_url = 'https://api.openweathermap.org/data/2.5/forecast/daily?lat={}&lon={}&cnt={}&appid={}'
    #forecast_url = 'https://api.openweathermap.org/data/2.5/forecast/daily?lat={}&lon={}&appid={}'

    forecast_url = 'https://api.openweathermap.org/data/2.5/forecast?lat={}&lon={}&appid={}'

    if request.method == 'POST':
        city1 = request.POST['city1']
        city2 = request.POST.get('city2', None)

        #weather_data1, daily_forecasts1 = fetch_weather_and_forecast(city1, api_key, current_weather_url, forecast_url)
        
        weather_data1 = fetch_weather_and_forecast(city1, api_key, current_weather_url, forecast_url)


        if city2 :
            #weather_data2, daily_forecasts2 = fetch_weather_and_forecast(city2, api_key, current_weather_url, forecast_url)
            
            weather_data2 = fetch_weather_and_forecast(city2, api_key, current_weather_url, forecast_url)

        else:
            #weather_data2, daily_forecasts2 = None, None
            
            weather_data2 = None,


        context = {
            'weather_data1': weather_data1,
            #'daily_forecasts1': daily_forecasts1,
            'weather_data2': weather_data2,
            #'daily_forecasts2': daily_forecasts2,
        }

        return render(request, 'weather_app/index.html', context)
    else:
        return render(request, 'weather_app/index.html')


def fetch_weather_and_forecast(city, api_key, current_weather_url, forecast_url):
    response = requests.get(current_weather_url.format(city, api_key)).json()
    print("Response: ", response)
    lat, lon = response['coord']['lat'], response['coord']['lon']
    forecast_response = requests.get(forecast_url.format(lat, lon, api_key)).json()
    #print("Forecast response: ", forecast_response)

    print("Wind: ", response['wind'])

    weather_data = {
        'city': city,
        'temperature': round( 1.8 * (response['main']['temp'] - 273) + 32, 2), #F = 1.8*(K-273) + 32.
        'description': response['weather'][0]['description'],
        'icon': response['weather'][0]['icon'],
        'min_temp': round( 1.8 * (response['main']['temp_min'] - 273) + 32, 2),
        'max_temp': round( 1.8 * (response['main']['temp_max'] - 273) + 32, 2),
        'country' : response['sys']['country'],
    }
    #daily_forecasts = {
        #'temperature': round( 1.8 * (forecast_response['list']['main']['temp'] - 273) + 32, 2),

    #}

    #
    #daily_forecasts = []
    #for daily_data in forecast_response['weather'][:5]:
        #daily_forecasts.append({
            #"id": daily_data['weather'][0]['id'],
            #"main": daily_data['weather'][0]['main'],
            #"description": daily_data['weather'][0]['description'],
            #"icon": daily_data['weather'][0]['icon'],
            ##'day': datetime.datetime.fromtimestamp(daily_data['dt']).strftime('%A'),
            ##'min_temp': round(daily_data['temp']['min'] - 273.15, 2),
            ##'max_temp': round(daily_data['temp']['max'] - 273.15, 2),
            ##'description': daily_data['weather'][0]['description'],
            ##'icon': daily_data['weather'][0]['icon'],
        #})

    #return weather_data, daily_forecasts
    return weather_data