# TravelWeather

This project utilizes GitHub Actions to schedule an automatic execution at 00:00am UTC (08:00am China Standard Time) on weekdays and retrieves weather data for the destination within the next 7 days by the [HeWeather weather daily forecast API](https://dev.qweather.com/docs/api/weather/weather-daily-forecast/).  
The program checks if the weather is sunny for two consecutive days on Saturday and Sunday. In such a case, it sends a notification email to a specified email address.

Please note that the free version of the API only provides weather forecasts for 7 days, which means that this project is only suitable for impromptu weekend getaways.

## Current Status

```
2023-07-14 - 未来7日内无晴好周末
```

## Configuration

### Secrets

This project uses the `Repository Secrets` feature of GitHub Actions. The following parameters are required:

- `SMTP_SERVER`: The SMTP server.
- `SMTP_PORT`: The SMTP port.
- `EMAIL_ADDRESS`: The email address of the SMTP sender.
- `EMAIL_PASSWORD`: The password of the SMTP sender.
- `EMAIL_RECEIVER`: The email address of the recipient.
- `WEATHER_API_KEY`: The API key of HeWeather. You need to create a free project
  on [HeWeather console](https://console.qweather.com/#/console) and apply for the API key.

### Destination

The `city.json` file contains the `name` and `locationId` of the cities returned by
the [HeWeather GEO API](https://dev.qweather.com/docs/api/geoapi/city-lookup/).

## TODO

- [ ] Allow users to choose their preferred email service provider for notifications
- [ ] Improve email notification content to use html

## License

    Copyright 2023 WangZhiYao
    
    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at
    
        http://www.apache.org/licenses/LICENSE-2.0
    
    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
