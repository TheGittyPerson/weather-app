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
from .data_labels.wind import WindLabels
from .gui_settings import GUISettings
from .graphics import Graphics
from .buttons import *
from .data_labels import *


class AppGUI:
    def __init__(self):
        """Initialize GUI window and settings."""
        print("LOADING...")
        self.root = tk.Tk()
        self.root.withdraw()

        self.settings = GUISettings()
        self.graphics = Graphics()
        self.dates = DateLabels(self)
        self.weather_conditions = WeatherConditionIcons(self)
        self.temperatures = TemperatureLabels(self)
        self.humidities = HumidityLabels(self)
        self.precipitations = PrecipitationLabels(self)
        self.uv_indices = UVILabels(self)
        self.wind = WindLabels(self)

        self.loading_window = None
        self._show_loading_screen()
        sleep(1)  # I put a lot of effort into designing the loading screen

        self.fetcher = DataFetcher()

        print("Welcome to the Python WeatherApp!")

    def run(self):
        """Run Python WeatherApp."""
        self._show_window()
        self._draw_elements()

        self.root.mainloop()

    def _draw_elements(self):
        """Draw visual elements to the screen."""
        self._draw_lines()
        for labels in [
            self.dates,
            self.weather_conditions,
            self.temperatures,
            self.humidities,
            self.precipitations,
            self.uv_indices,
            self.wind,
        ]:
            labels.draw()
        self.refresh_button = RefreshButton(self)
        self._destroy_loading_screen()

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

    def _destroy_loading_screen(self):
        """Destroy the loading screen."""
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
