"""
This module is for managing the GUI windows, graphics, and appearance settings
of the WeatherApp.
"""

from .graphics import Graphics


class GUISettings:
    """A class to manage window and appearance settings for the GUI."""

    def __init__(self):
        """Initialize window and appearance settings."""
        self.graphics = Graphics()

        # General
        self.title = 'Python WeatherApp'
        self.theme_bg = '#daf0ff'

        # Forecast
        self.forecast_days = 6
        self.weather_icon_mapping = {
            (0,): self.graphics.clear,
            (1, 2): self.graphics.part_cloudy,
            (3, 45, 48): self.graphics.cloudy,
            (51, 53, 56, 61, 80): self.graphics.rain_1,
            (55, 57, 63, 66, 81): self.graphics.rain_2,
            (65, 67, 82): self.graphics.rain_3,
            (71, 85): self.graphics.snow_1,
            (73, 77): self.graphics.snow_2,
            (75, 86): self.graphics.snow_3,
            (95, 96, 99): self.graphics.thunderstorm,
        }
        self.weather_description_mapping = {
            0: 'Clear',
            1: 'Mainly Clear',
            2: 'Partly Cloudy',
            3: 'Overcast',
            45: 'Fog',
            48: 'Depositing Rime Fog',
            51: 'Light Drizzle',
            53: 'Moderate Drizzle',
            55: 'Dense Drizzle',
            56: 'Light Freezing Drizzle',
            57: 'Dense Freezing Drizzle',
            61: 'Slight Rain',
            63: 'Moderate Rain',
            65: 'Heavy Rain',
            66: 'Light Freezing Rain',
            67: 'Heavy Freezing Rain',
            71: 'Slight Snow',
            73: 'Moderate Snow',
            75: 'Heavy Snow',
            77: 'Snow Grains',
            80: 'Slight Rain Showers',
            81: 'Moderate Rain Showers',
            82: 'Violent Rain Showers',
            85: 'Slight Snow Showers',
            86: 'Heavy Snow Showers',
            95: 'Thunderstorm',
            96: 'Thunderstorm with Slight Hail',
            99: 'Thunderstorm with Heavy Hail',
        }

        # Window
        self.window_bg = self.theme_bg
        self.window_width = self.forecast_days * 200
        self.window_height = 600
        self.window_relief = 'raised'
        self.window_width_resizable = False
        self.window_height_resizable = False
        self.window_topmost = False

        # Loading window
        self.loading_screen_title = "Please Wait..."
        self.loading_screen_width = 800
        self.loading_screen_height = 480
        self.loading_screen_topmost = True

        # DateLabels labels
        self.date_font = ('Malgun Gothic', 15, 'bold')
        self.date_posy = 20
        self.date_color = 'black'

        # Weather icon labels
        self.icons_bg = self.theme_bg
        self.icons_posy = self.date_posy + 25

        # Weather descriptions
        self.descriptions_bg = self.theme_bg
        self.descriptions_font = ('Gill Sans MT', 14)
        self.descriptions_fg = 'black'
        self.descriptions_posy = self.icons_posy + 125

        # Temperatures
        self.temperature_bg = self.theme_bg

        self.amb_temperature_font = ('Calibri Light', 30)
        self.app_temperature_font = ('Calibri Light', 15)
        self.max_min_label_font = ('Calibri Light', 15)
        self.feels_like_label_font = ('Calibri Light', 15)

        self.max_amb_temperature_fg = '#f94449'
        self.min_amb_temperature_fg = '#4169e1'
        self.max_app_temperature_fg = '#f77c82'
        self.min_app_temperature_fg = '#82a1ff'

        self.max_label_fg = self.max_amb_temperature_fg
        self.min_label_fg = self.min_amb_temperature_fg
        self.feels_like_label_fg = 'black'

        self.max_min_label_posy = self.descriptions_posy + 30
        self.amb_temperature_posy = self.max_min_label_posy + 22
        self.feels_like_label_posy = self.amb_temperature_posy + 50
        self.app_temperature_posy = self.feels_like_label_posy

        # HumidityLabels
        self.humidity_bg = self.theme_bg
        self.humidity_font = ('Calibri', 14)
        self.humidity_fg = 'black'
        self.humidity_posy = self.app_temperature_posy + 40
        self.humidity_level_font = ('Gill Sans MT', 13, 'bold')
        self.humidity_level_anchor = 'center'
        self.humidity_level_posy = self.humidity_posy + 60

        # Refresh icon
        self.refresh_icon_posx = self.window_width - 40
        self.refresh_icon_posy = self.window_height - 40
