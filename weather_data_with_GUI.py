import requests
import csv
from datetime import datetime
import tkinter as tk


weather_codes={
    0: "Clear sky ☀️",

    1: "Mainly clear 🌤️",
    2: "Partly cloudy ⛅",
    3: "Overcast ☁️",

    45: "Fog 🌫️",
    48: "Depositing rime fog 🌫️",

    51: "Light drizzle 🌦️",
    53: "Moderate drizzle 🌦️",
    55: "Dense drizzle 🌧️",

    56: "Light freezing drizzle 🧊🌧️",
    57: "Dense freezing drizzle 🧊🌧️",

    61: "Slight rain 🌧️",
    63: "Moderate rain 🌧️",
    65: "Heavy rain 🌧️",

    66: "Light freezing rain 🧊🌧️",
    67: "Heavy freezing rain 🧊🌧️",

    71: "Slight snow fall ❄️",
    73: "Moderate snow fall ❄️",
    75: "Heavy snow fall ❄️",

    77: "Snow grains ❄️",

    80: "Slight rain showers 🌦️",
    81: "Moderate rain showers 🌦️",
    82: "Violent rain showers 🌧️",

    85: "Slight snow showers ❄️",
    86: "Heavy snow showers ❄️",

    95: "Thunderstorm ⛈️",
    96: "Thunderstorm with slight hail ⛈️🧊",
    99: "Thunderstorm with heavy hail ⛈️🧊"
                     
    }    
def get_coordinates(city):
    geo_url="http://geocoding-api.open-meteo.com/v1/search"
    geo_res= requests.get(geo_url,params={"name":city,"count":1}).json()
    
    
    if "results" not in geo_res:
        return None
    
    Name=geo_res["results"][0]["name"]
    
    if city.lower() != Name.lower():
        result_label.config(text="city name not correct!!")
        return
    return geo_res["results"][0]["latitude"] ,geo_res["results"][0]["longitude"]
    

def fetch_weather(lat,lon):
    weather_url = "https://api.open-meteo.com/v1/forecast"
    wea_res = requests.get(weather_url,params={
        "latitude":lat,
        "longitude":lon,
        "current_weather":True
    }).json()
    
    if "current_weather" not in wea_res:
        return None
    return wea_res["current_weather"]

def save_to_csv(city,temp,wind,code,status):
    with open("Weather_data.csv","a",newline="",encoding="utf-8") as file:
        writer= csv.writer(file)
        if file.tell()==0:
            writer.writerow(["Time","City","Temperature","Wind","Code","Status"])
        writer.writerow([
            datetime.now().strftime("%Y-%m-%d %H:%M"),
            city,
            f"{temp}°C",
            f"{wind}km/h",
            code,
            status
        ])

def get_weather():
    city=city_entry.get()
    if not city:
        result_label.config(text="Enter a city!!")
        return
        
    coords= get_coordinates(city)
    if not coords:
        result_label.config(text="city not found!!")
        return
    
    lat,lon=coords
    weather=fetch_weather(lat,lon)
    if not weather:
        result_label.config(text="weather not found")
        return
    
    
    temp =weather["temperature"]
    wind =weather["windspeed"]
    code =weather["weathercode"]
    status=weather_codes.get(code,"Unknown")
    
    result_label.config(
        text=f"{city}:{temp}°C,wind {wind}km/h,{status}"
        )
    
    save_to_csv(city,temp,wind,code,status)
    

      
window = tk.Tk()
window.title("weather app")
window.geometry("500x300")

city_entry= tk.Entry(window,width=30)
city_entry.pack(pady=40)

btn=tk.Button(window,text="Get weather",command=get_weather)
btn.pack(pady=50)

result_label=tk.Label(window,text="",font=("Arial",12))
result_label.pack(pady=10)

window.mainloop()