from dataclasses import dataclass
from typing import Any
from typing import List


@dataclass
class City:
    name: str
    location_id: str

    @staticmethod
    def from_dict(obj: Any) -> 'City':
        _name = str(obj.get('name'))
        _location_id = str(obj.get('location_id'))
        return City(_name, _location_id)


@dataclass
class Daily:
    fx_date: str
    sunrise: str
    sunset: str
    moonrise: str
    moonset: str
    moon_phase: str
    moon_phase_icon: str
    temp_max: str
    temp_min: str
    icon_day: str
    text_day: str
    icon_night: str
    text_night: str
    wind360_day: str
    wind_dir_day: str
    wind_scale_day: str
    wind_speed_day: str
    wind360_night: str
    wind_dir_night: str
    wind_scale_night: str
    wind_speed_night: str
    humidity: str
    precip: str
    pressure: str
    vis: str
    cloud: str
    uv_index: str

    @staticmethod
    def from_dict(obj: Any) -> 'Daily':
        _fx_date = str(obj.get('fxDate'))
        _sunrise = str(obj.get('sunrise'))
        _sunset = str(obj.get('sunset'))
        _moonrise = str(obj.get('moonrise'))
        _moonset = str(obj.get('moonset'))
        _moon_phase = str(obj.get('moonPhase'))
        _moon_phase_icon = str(obj.get('moonPhaseIcon'))
        _temp_max = str(obj.get('tempMax'))
        _temp_min = str(obj.get('tempMin'))
        _icon_day = str(obj.get('iconDay'))
        _text_day = str(obj.get('textDay'))
        _icon_night = str(obj.get('iconNight'))
        _text_night = str(obj.get('textNight'))
        _wind360_day = str(obj.get('wind360Day'))
        _wind_dir_day = str(obj.get('windDirDay'))
        _wind_scale_day = str(obj.get('windScaleDay'))
        _wind_speed_day = str(obj.get('windSpeedDay'))
        _wind360_night = str(obj.get('wind360Night'))
        _wind_dir_night = str(obj.get('windDirNight'))
        _wind_scale_night = str(obj.get('windScaleNight'))
        _wind_speed_night = str(obj.get('windSpeedNight'))
        _humidity = str(obj.get('humidity'))
        _precip = str(obj.get('precip'))
        _pressure = str(obj.get('pressure'))
        _vis = str(obj.get('vis'))
        _cloud = str(obj.get('cloud'))
        _uv_index = str(obj.get('uvIndex'))
        return Daily(_fx_date, _sunrise, _sunset, _moonrise, _moonset, _moon_phase, _moon_phase_icon, _temp_max,
                     _temp_min, _icon_day, _text_day, _icon_night, _text_night, _wind360_day, _wind_dir_day,
                     _wind_scale_day, _wind_speed_day, _wind360_night, _wind_dir_night, _wind_scale_night,
                     _wind_speed_night, _humidity, _precip, _pressure, _vis, _cloud, _uv_index)


@dataclass
class Weather:
    code: str
    update_time: str
    fx_link: str
    daily: List[Daily]

    @staticmethod
    def from_dict(obj: Any) -> 'Weather':
        _code = str(obj.get('code'))
        _update_time = str(obj.get('updateTime'))
        _fx_link = str(obj.get('fxLink'))
        if obj.get('daily'):
            _daily = [Daily.from_dict(y) for y in obj.get('daily')]
        else:
            _daily = []
        return Weather(_code, _update_time, _fx_link, _daily)


@dataclass
class CityWeather:
    city: City
    update_time: str
    daily: List[Daily]
