"""
This module is for managing the WeatherApp GUI functioning,
window creation and management of graphical elements.
"""

import importlib
import tkinter as tk
from time import sleep

from . import data_fetcher
from . import gui_settings
from . import graphics
from .data_fetcher import DataFetcher
from .gui_settings import GUISettings
from .graphics import Graphics
from .buttons.refresh_button import RefreshButton
from .data_visuals.date import Date
from .data_visuals.weather_condition import WeatherCondition
from .data_visuals.temperature import Temperature
from .data_visuals.humidity import Humidity


class AppGUI:
    def __init__(self):
        """Initialize GUI window and settings."""
        print("LOADING...")
        self.root = tk.Tk()
        self.root.withdraw()

        self.fetcher = DataFetcher()
        self.settings = GUISettings()
        self.graphics = Graphics()
        self.dates = Date(self)
        self.icons = WeatherCondition(self)
        self.temperature = Temperature(self)
        self.humidity = Humidity(self)

        self._show_loading_screen()
        print("Welcome to the Python WeatherApp!")

    def run(self):
        """Run Python WeatherApp."""
        self._show_window()
        self._draw_elements()

        self.root.mainloop()

    def _draw_elements(self):
        """Draw visual elements to the screen."""
        self._draw_lines()
        self.dates.draw_dates()
        self.icons.draw_weather_icons()
        self.icons.draw_weather_descriptions()
        self.temperature.draw_temperatures()
        self.humidity.draw_humidity()
        self.refresh_button = RefreshButton(self)

    def _show_loading_screen(self):
        """Display the loading screen."""
        self.loading_window = tk.Toplevel()
        self.loading_window.attributes('-topmost',
                                       self.settings.loading_screen_topmost)
        self.loading_window.title(self.settings.loading_screen_title)

        screen_width = self.loading_window.winfo_screenwidth()
        screen_height = self.loading_window.winfo_screenheight()

        width = self.settings.loading_screen_width
        height = self.settings.loading_screen_height

        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)

        self.loading_window.geometry(f'{width}x{height}+{x}+{y}')

        loading_image = self.graphics.loading_screen

        loading_label = tk.Label(self.loading_window, image=loading_image)
        loading_label.pack(fill='both', expand=True)

        self.loading_window.update()

        sleep(self.settings.loading_screen_duration)

        self.loading_window.destroy()

    def _show_window(self):
        """Display main window."""
        self.root.deiconify()
        self.root.title(self.settings.title)
        self.root.attributes('-topmost', self.settings.window_topmost)
        self.root.resizable(
            self.settings.window_width_resizable,
            self.settings.window_height_resizable
        )
        self.window = tk.Canvas(
            self.root,
            bg=self.settings.window_bg,
            width=self.settings.window_width,
            height=self.settings.window_height,
            relief='ridge'
        )
        self.window.grid(row=0, column=0)

    def _draw_lines(self):
        """Draw separation lines to the window."""
        days = self.settings.forecast_days
        line_positions = [self.settings.window_width // days * i
                          for i in range(1, days)]
        for x in line_positions:
            self.window.create_line(
                x, 0, x, self.settings.window_height, fill='black', width=2
            )

    def refresh(self):
        """Refresh the weather data and graphics and update the window."""
        modules = [data_fetcher, gui_settings, graphics]
        for module in modules:
            importlib.reload(module)
        self.fetcher = DataFetcher()
        self.settings = GUISettings()
        self.graphics = Graphics()

        for widget in self.root.winfo_children():
            widget.destroy()
        sleep(1)
        self.run()
