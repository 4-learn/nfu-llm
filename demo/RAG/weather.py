import os
import requests

# OpenWeatherMap API Key
weather_api_key = os.getenv("OPEN_WEATHER_API_KEY")

# 定義檢索函數
def fetch_weather_data(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={weather_api_key}&units=metric&lang=zh_tw"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        weather_desc = data['weather'][0]['description']
        temp_min = data['main']['temp_min']
        temp_max = data['main']['temp_max']
        return f"{city}的天氣是{weather_desc}，溫度範圍在 {temp_min}°C 到 {temp_max}°C 之間。"
    else:
        return "無法取得天氣資訊。"