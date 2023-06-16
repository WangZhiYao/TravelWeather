import json
import logging
import os
import re
import smtplib
from datetime import datetime
from email.mime.text import MIMEText

import requests
from requests import HTTPError

from model import City, Weather, CityWeather

# Email
EMAIL_ADDRESS = os.getenv('EMAIL_ADDRESS')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')
EMAIL_RECEIVER = os.getenv('EMAIL_RECEIVER')

# SMTP
SMTP_SERVER = 'smtp.exmail.qq.com'
SMTP_PORT = 465

# QWeather API
WEATHER_API = 'https://devapi.qweather.com/v7/weather/7d'
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")

# Set log level
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y.%m.%d %H:%M:%S')


def get_cities():
    with open('city.json', 'r', encoding='utf-8') as cities:
        return [City.from_dict(city) for city in json.load(cities)]


def get_city_weather(sunny_cities, city):
    logging.info(f'Requesting weather for {city.name} for the next 7 days')
    params = {'key': WEATHER_API_KEY, 'location': city.location_id}
    response = requests.get(WEATHER_API, params=params)
    try:
        response.raise_for_status()
    except HTTPError as ex:
        logging.error(ex)
        return

    weather = Weather.from_dict(response.json())
    if weather.code != '200':
        logging.error(response.text)
        return

    logging.info(f'Successfully retrieved weather for {city.name}')

    for i, day in enumerate(weather.daily[:-1]):
        if datetime.strptime(day.fx_date, '%Y-%m-%d').weekday() == 5 and all(
                day.text_day == '晴' for day in weather.daily[i:i + 2]):
            logging.info(f'{city.name} has good weather for the coming weekend')
            sunny_cities.append(CityWeather(city, update_time=weather.update_time, daily=weather.daily[i:i + 2]))
            return

    logging.info(f'{city.name} does not have good weather for the coming weekend')


def send_email(subject, body):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = EMAIL_RECEIVER

    with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as smtp:
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.send_message(msg)


def make_email(city_weathers):
    body = '以下城市将在本周末天气晴好：\n\n'
    for city_weather in city_weathers:
        city = city_weather.city
        daily = city_weather.daily
        saturday, sunday = daily
        update_time = datetime.strptime(city_weather.update_time, '%Y-%m-%dT%H:%M%z').strftime('%Y-%m-%d %H:%M')
        body += f'{city.name} 更新时间 - {update_time}:\n'
        body += f'{saturday.fx_date} 最高气温: {saturday.temp_max}°C 最低气温: {saturday.temp_min}°C 夜间：{saturday.text_night}\n'
        body += f'{sunday.fx_date} 最高气温: {sunday.temp_max}°C 最低气温: {sunday.temp_min}°C 夜间：{saturday.text_night}\n\n'
    return body.strip('\n')


def update_readme(new_content):
    with open('README.md', 'r+', encoding='utf-8') as f:
        content = f.read()
        pattern = re.compile(r'(?<=## Current Status).*?(?=## Configuration)', re.DOTALL)
        new_content = re.sub(pattern, f'\n\n```\n{new_content}\n```\n\n', content)
        f.seek(0)
        f.write(new_content)
        f.truncate()


def check_weather():
    sunny_cities = []
    for city in get_cities():
        get_city_weather(sunny_cities, city)

    today = datetime.today().strftime('%Y-%m-%d')
    if sunny_cities:
        body = make_email(sunny_cities)
        title = f'{today} - 周末天气晴好提醒'
        send_email(title, body)
        content = f'{title}\n{body}'
    else:
        content = f'{today} - 未来7日内无晴好周末'

    update_readme(content)
    logging.info(content)


if __name__ == '__main__':
    check_weather()
