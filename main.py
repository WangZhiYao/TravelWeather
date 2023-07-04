import concurrent.futures
import json
import logging
import os
import re
import smtplib
from concurrent.futures import ThreadPoolExecutor, wait
from datetime import datetime
from email.mime.text import MIMEText

import requests
from requests import HTTPError

from model import City, Weather, CityWeather

# QWeather API
WEATHER_API = 'https://devapi.qweather.com/v7/weather/7d'
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")

# Set log level
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y.%m.%d %H:%M:%S')


def get_cities():
    with open('city.json', 'r', encoding='utf-8') as cities_file:
        cities_data = json.load(cities_file)
        return [City.from_dict(city) for city in cities_data]


def get_city_weather(city):
    logging.info(f'Requesting weather for {city.name} for the next 7 days')
    params = {'key': WEATHER_API_KEY, 'location': city.location_id}
    try:
        response = requests.get(WEATHER_API, params=params)
        response.raise_for_status()
        weather_data = response.json()
        weather = Weather.from_dict(weather_data)
        if weather.code == '200':
            return weather
        else:
            logging.error(weather_data)
    except HTTPError as ex:
        logging.error(f'HTTPError occurred while requesting weather for {city.name}: {ex}')
    except requests.RequestException as ex:
        logging.error(f'RequestException occurred while requesting weather for {city.name}: {ex}')
    except (ValueError, KeyError) as ex:
        logging.error(f'Error occurred while parsing weather data for {city.name}: {ex}')
    return None


def find_sunny_cities(city):
    city_weather = get_city_weather(city)
    if city_weather is not None:
        for i, daily in enumerate(city_weather.daily[:-1]):
            weekday = datetime.strptime(daily.fx_date, '%Y-%m-%d').weekday()
            if weekday > 5:
                logging.info(f'{city.name} does not have good weather for the coming weekend')
                return None
            if weekday != 5:
                continue
            weekend = city_weather.daily[i:i + 2]
            has_sunny_weekend = all(daily.text_day == '晴' for daily in weekend)
            if has_sunny_weekend:
                logging.info(f'{city.name} has good weather for the coming weekend')
                return CityWeather(city, update_time=city_weather.update_time, daily=weekend)
        else:
            logging.info(f'{city.name} does not have good weather for the coming weekend')
    return None


def send_email(subject, body):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = os.getenv('EMAIL_ADDRESS')
    msg['To'] = os.getenv('EMAIL_RECEIVER')

    smtp_server = os.getenv('SMTP_SERVER')
    smtp_port = os.getenv('SMTP_PORT', '465')

    with smtplib.SMTP_SSL(smtp_server, int(smtp_port)) as smtp:
        smtp.login(os.getenv('EMAIL_ADDRESS'), os.getenv('EMAIL_PASSWORD'))
        smtp.send_message(msg)


def generate_email_content(city_weathers):
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
    with ThreadPoolExecutor(max_workers=10) as executor:
        city_weather_futures = [executor.submit(find_sunny_cities, city) for city in get_cities()]
        wait(city_weather_futures, return_when=concurrent.futures.ALL_COMPLETED)
        for future in city_weather_futures:
            city_weather = future.result()
            if city_weather is not None:
                sunny_cities.append(city_weather)

    today = datetime.today().strftime('%Y-%m-%d')
    if sunny_cities:
        body = generate_email_content(sunny_cities)
        title = f'{today} - 周末天气晴好提醒'
        send_email(title, body)
        content = f'{title}\n{body}'
    else:
        content = f'{today} - 未来7日内无晴好周末'

    update_readme(content)
    logging.info(content)


if __name__ == '__main__':
    check_weather()
