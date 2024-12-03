import requests
from tkinter import Tk, Label, Entry, Button, StringVar, Frame

API_KEY = '741adf81067cbc594b10e8f7eb49024e'
CURRENT_WEATHER_URL = "http://api.openweathermap.org/data/2.5/weather"
FORECAST_URL = "http://api.openweathermap.org/data/2.5/forecast"

weather_emojis = {
    "Clear": "☀️",
    "Clouds": "☁️",
    "Rain": "🌧️",
    "Thunderstorm": "⛈️",
    "Snow": "❄️",
    "Mist": "🌫️",
    "Drizzle": "🌦️"
}

background_colors = {
    "Clear": "#87CEEB",
    "Clouds": "#D3D3D3",
    "Rain": "#5F9EA0",
    "Thunderstorm": "#4B0082",
    "Snow": "#FFFFFF",
    "Mist": "#F0E68C",
    "Drizzle": "#AFEEEE"
}

def get_weather_data(city):
    params = {
        'q': city,
        'appid': API_KEY,
        'units': 'metric',
        'lang': 'tr'
    }
    response = requests.get(CURRENT_WEATHER_URL, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        return None

def get_forecast_data(city):
    params = {
        'q': city,
        'appid': API_KEY,
        'units': 'metric',
        'lang': 'tr'
    }
    response = requests.get(FORECAST_URL, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        return None

def update_background(condition):
    color = background_colors.get(condition, "#1E1E1E")
    root.configure(bg=color)
    app_frame.configure(bg=color)
    title_label.configure(bg=color, fg="#FFFFFF")
    footer_label.configure(bg=color, fg="#FFFFFF")

def display_weather():
    city = city_var.get()
    weather_data = get_weather_data(city)
    forecast_data = get_forecast_data(city)
    if weather_data:
        condition = weather_data['weather'][0]['main']
        update_background(condition)
        city_label.config(text=f"{weather_data['name']}, {weather_data['sys']['country']}")
        temp_label.config(text=f"{weather_data['main']['temp']}°C {weather_emojis.get(condition, '')}")
        description = weather_data['weather'][0]['description']
        weather_condition_label.config(text=description.capitalize())
        wind_speed = weather_data['wind']['speed']
        wind_label.config(text=f"Rüzgar: {wind_speed} m/s")
        if forecast_data:
            next_hours = forecast_data['list'][:3]
            hourly_forecast = "\n".join(
                [
                    f"{data['dt_txt'][11:16]} - {data['main']['temp']}°C {weather_emojis.get(data['weather'][0]['main'], '')}, {data['weather'][0]['description']}"
                    for data in next_hours
                ]
            )
            today_forecast_label.config(text=f"Bugün:\n{hourly_forecast}")
        daily_forecast = {}
        for data in forecast_data['list']:
            date = data['dt_txt'].split(" ")[0]
            if date not in daily_forecast:
                daily_forecast[date] = data
        five_day_forecast = "\n".join(
            [
                f"{date}: {info['main']['temp']}°C {weather_emojis.get(info['weather'][0]['main'], '')}, {info['weather'][0]['description']}"
                for date, info in list(daily_forecast.items())[:5]
            ]
        )
        five_day_forecast_label.config(text=f"5 Günlük Tahmin:\n{five_day_forecast}")
    else:
        city_label.config(text="Şehir bulunamadı!")
        temp_label.config(text="")
        weather_condition_label.config(text="")
        wind_label.config(text="")
        today_forecast_label.config(text="")
        five_day_forecast_label.config(text="")

root = Tk()
root.title("Hava Durumu Uygulaması")
root.geometry("600x700")
root.configure(bg="#1E1E1E")
root.resizable(False, False)

app_frame = Frame(root, bg="#FFFFFF", relief="flat", padx=20, pady=20)
app_frame.place(relx=0.5, rely=0.5, anchor="center", width=550, height=600)

title_label = Label(root, text="🌤️ Hava Durumu 🌧️", font=("Helvetica", 24, "bold"), bg="#1E1E1E", fg="#FFFFFF")
title_label.pack(pady=10)

city_var = StringVar()
city_entry = Entry(app_frame, textvariable=city_var, font=("Helvetica", 16), relief="flat", bd=2, fg="#333333", bg="#4f4f4f", justify="center")
city_entry.pack(pady=10, ipadx=5, ipady=5)

get_weather_btn = Button(app_frame, text="Hava Durumunu Göster", font=("Helvetica", 14), bg="#00C853", fg="white", relief="flat", command=display_weather)
get_weather_btn.pack(pady=10, ipadx=10, ipady=5)

city_label = Label(app_frame, text="", font=("Helvetica", 18, "bold"), bg="#FFFFFF", fg="#333333")
city_label.pack(pady=10)

temp_label = Label(app_frame, text="", font=("Helvetica", 48, "bold"), bg="#FFFFFF", fg="#333333")
temp_label.pack(pady=10)

weather_condition_label = Label(app_frame, text="", font=("Helvetica", 16), bg="#FFFFFF", fg="#666666")
weather_condition_label.pack(pady=10)

wind_label = Label(app_frame, text="", font=("Helvetica", 14), bg="#FFFFFF", fg="#333333")
wind_label.pack(pady=5)

today_forecast_label = Label(app_frame, text="", font=("Helvetica", 12), bg="#FFFFFF", fg="#333333", justify="left")
today_forecast_label.pack(pady=10)

five_day_forecast_label = Label(app_frame, text="", font=("Helvetica", 12), bg="#FFFFFF", fg="#333333", justify="left")
five_day_forecast_label.pack(pady=10)

footer_label = Label(root, text="KoçWeather", font=("Helvetica", 10), bg="#1E1E1E", fg="#FFFFFF")
footer_label.pack(side="bottom", pady=10)

root.mainloop()
