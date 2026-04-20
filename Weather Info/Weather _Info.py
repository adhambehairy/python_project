import requests
from plyer import notification

#Create an object of ToastNotifier class
city="Dortmund"
geo_url="http://geocoding-api.open-meteo.com/v1/search"
geo_params={'name':city,'count':1}
geo_res= requests.get(geo_url, params=geo_params).json()

#Fetch current weather data
if "results" in geo_res:
    lat=geo_res["results"][0]["latitude"]
    long=geo_res["results"][0]["longitude"]
    
    weather_url="https://api.open-meteo.com/v1/forecast"
    weather_params={
        'latitude':lat,
        'longitude':long,
        'current_weather': True
    }
    weather_res= requests.get(weather_url,params=weather_params).json()
    
    #Display the Notification
    
    if 'current_weather' in weather_res:
        temp= weather_res['current_weather']['temperature']
        wsp= weather_res['current_weather']['windspeed']  
    
        weather_info= f"{city}:{temp}°C , Wind {wsp}km/h"
        print('Weather',weather_info) 
    
        notification.notify(
           title="weather_Update",
           message=weather_info,
           timeout=5
        )
    else:
        print("weather data not found")

    
else:
    print("city not found") 
    


