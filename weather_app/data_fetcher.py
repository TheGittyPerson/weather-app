"""
This is a module for fetching and processing weather data
using the Open-Meteo API.
"""

import sys
import tkinter.messagebox


import openmeteo_requests
import requests_cache
import pandas as pd
import geocoder
from retry_requests import retry
import requests.exceptions

from .gui_settings import GUISettings


class DataFetcher:
    class CoordinatesError(RuntimeError):
        pass
    
    class DailyDataError(RuntimeError):
        pass
    
    class HourlyDataError(RuntimeError):
        pass
    
    def __init__(self):
        """Initialize attributes."""
        self.settings = GUISettings()
        try:
            # Set up the Open-Meteo API client with cache and retry on error
            cache_session = requests_cache.CachedSession('.cache',
                                                         expire_after=3600)
            retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
            openmeteo = openmeteo_requests.Client(session=retry_session)
            
            self.url = 'https://api.open-meteo.com/v1/forecast'
            
            # It is important to assign the variables in the correct order
            self.weather_vars_hourly = [
                'relative_humidity_2m',
                'surface_pressure',
            ]
            self.weather_vars_daily = [
                'weather_code',
                'temperature_2m_max',
                'temperature_2m_min',
                'apparent_temperature_max',
                'apparent_temperature_min',
                'precipitation_sum',
                'precipitation_hours',
                'precipitation_probability_mean',
                'uv_index_max',
                'wind_speed_10m_max',
            ]
            
            self.latitude, self.longitude = self._get_coordinates()
            self.forecast_days = self.settings.forecast_days
            params = {
                'latitude': self.latitude,
                'longitude': self.longitude,
                'hourly': self.weather_vars_hourly,
                'daily': self.weather_vars_daily,
                'timezone': 'auto',
                'forecast_days': self.forecast_days,
            }
            responses = openmeteo.weather_api(self.url, params=params)
            
            # Process location
            response = responses[0]
            self.elevation = response.Elevation()
            self.timezone = \
                f'{response.Timezone()} {response.TimezoneAbbreviation()}'
            self.utc_offset_secs = response.UtcOffsetSeconds()
            
            # Process hourly data.
            # The order of variables needs to be the same as requested.
            hourly = response.Hourly()
            
            if hourly is None:
                tkinter.messagebox.showinfo(
                    "ERROR :(",
                    "Unable to get daily weather data."
                    "\n\nTry again later."
                )
                sys.exit(1)
            
            hourly_relative_humidity_2m = hourly.Variables(0).ValuesAsNumpy()
            hourly_surface_pressure = hourly.Variables(1).ValuesAsNumpy()
            
            self.hourly_data = {
                'date': pd.date_range(
                    start=pd.to_datetime(hourly.Time(), unit='s', utc=True),
                    end=pd.to_datetime(hourly.TimeEnd(), unit='s', utc=True),
                    freq=pd.Timedelta(seconds=hourly.Interval()),
                    inclusive='left'
                ), 'relative_humidity_2m': hourly_relative_humidity_2m,
                'surface_pressure': hourly_surface_pressure
            }
            
            self.hourly_dataframe = pd.DataFrame(data=self.hourly_data)
            
            # Process daily data.
            # The order of variables needs to be the same as requested.
            daily = response.Daily()
            
            if daily is None:
                tkinter.messagebox.showinfo(
                    "ERROR :(",
                    "Unable to get daily weather data."
                    "\n\nTry again later."
                )
                sys.exit(1)
            
            daily_weather_code = daily.Variables(0).ValuesAsNumpy()
            daily_temperature_2m_max = daily.Variables(1).ValuesAsNumpy()
            daily_temperature_2m_min = daily.Variables(2).ValuesAsNumpy()
            daily_apparent_temperature_max = daily.Variables(3).ValuesAsNumpy()
            daily_apparent_temperature_min = daily.Variables(4).ValuesAsNumpy()
            daily_precipitation_sum = daily.Variables(5).ValuesAsNumpy()
            daily_precipitation_hours = daily.Variables(6).ValuesAsNumpy()
            daily_precipitation_probability_mean = (
                daily.Variables(7).ValuesAsNumpy()
            )
            daily_uv_index_max = daily.Variables(8).ValuesAsNumpy()
            daily_wind_speed_10m_max = daily.Variables(9).ValuesAsNumpy()
            
            self.daily_data = {
                'date': pd.date_range(
                    start=pd.to_datetime(daily.Time(), unit='s', utc=True),
                    end=pd.to_datetime(daily.TimeEnd(), unit='s', utc=True),
                    freq=pd.Timedelta(seconds=daily.Interval()),
                    inclusive='left'
                ),
                'weather_code': daily_weather_code,
                'temperature_2m_max': daily_temperature_2m_max,
                'temperature_2m_min': daily_temperature_2m_min,
                'apparent_temperature_max': daily_apparent_temperature_max,
                'apparent_temperature_min': daily_apparent_temperature_min,
                'uv_index_max': daily_uv_index_max,
                'precipitation_sum': daily_precipitation_sum,
                'precipitation_hours': daily_precipitation_hours,
                'precipitation_probability_mean':
                    daily_precipitation_probability_mean,
                'wind_speed_10m_max': daily_wind_speed_10m_max
            }
            
            self.daily_dataframe = pd.DataFrame(data=self.daily_data)
        
        except requests.exceptions.ConnectionError:
            tkinter.messagebox.showinfo(
                "ERROR :(",
                "Unable to retrieve weather data."
                "\n\nPlease check your Internet connection and try again."
            )
            sys.exit(1)
        except self.CoordinatesError:
            tkinter.messagebox.showinfo(
                "ERROR :(",
                "Unable to fetch device coordinates."
                "\n\nPlease make sure that the program has permission to "
                "access your location."
            )
            sys.exit(1)
        except self.DailyDataError as e:
            tkinter.messagebox.showinfo(
                "ERROR :(",
                f"Unable to fetch daily weather info. (daily_data: {e})"
                "\n\nPlease try again."
            )
        except self.HourlyDataError as e:
            tkinter.messagebox.showinfo(
                "ERROR :(",
                f"Unable to fetch hourly weather info. (hourly_data: {e})"
                "\n\nPlease try again."
            )
        except requests.exceptions.Timeout:
            tkinter.messagebox.showinfo(
                "ERROR :(",
                "'data_fetcher.py' took too long to respond."
                "\n\nPlease try again."
            )
            sys.exit(1)
        except Exception as e:
            tkinter.messagebox.showinfo(
                "ERROR :(",
                f"Unable to retrieve weather data: {e}"
                "\n\nPlease try again."
            )
            sys.exit(1)
    
    def _get_coordinates(self):
        """Find location information using IP address."""
        coordinates = geocoder.ip('me')
        if coordinates.latlng:
            lat, lng = coordinates.latlng
            return lat, lng
        else:
            raise self.CoordinatesError
