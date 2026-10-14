"""A module to manage weather temperature visualization."""

import tkinter as tk
from typing import TYPE_CHECKING

from ..gui_settings import GUISettings

if TYPE_CHECKING:
    from ..app_gui import AppGUI


class TemperatureLabels:
    def __init__(self, gui: AppGUI):
        """Initialize self."""
        self.gui = gui
        self.settings = GUISettings()

    def draw(self):
        """Draw temperature information to the screen."""
        temperatures = self._get_temperatures()
        for day_num, temps in enumerate(temperatures):

            max_amb_temp_posx = ((day_num + 0.27)
                                 * (self.settings.window_width
                                    // self.settings.forecast_days))
            min_amb_temp_posx = ((day_num + 0.73)
                                 * (self.settings.window_width
                                    // self.settings.forecast_days))
            feels_like_label_posx = max_amb_temp_posx - 50
            max_app_temp_posx = feels_like_label_posx + 90
            min_app_temp_posx = max_app_temp_posx + 50

            self._draw_feels_like_label(feels_like_label_posx)
            self._draw_max_min_labels(max_amb_temp_posx, min_amb_temp_posx)

            max_amb_temp_int = temps['max_amb_temp']
            max_amb_temp = tk.Label(
                self.gui.root,
                font=self.settings.amb_temperature_font,
                text=f"{max_amb_temp_int}°C",
                fg=self.settings.max_amb_temperature_fg,
                bg=self.settings.temperature_bg,
            )

            min_amb_temp_int = temps['min_amb_temp']
            min_amb_temp = tk.Label(
                self.gui.root,
                font=self.settings.amb_temperature_font,
                text=f"{min_amb_temp_int}°C",
                fg=self.settings.min_amb_temperature_fg,
                bg=self.settings.temperature_bg,
            )

            max_app_temp_int = temps['max_app_temp']
            max_app_temp = tk.Label(
                self.gui.root,
                font=self.settings.app_temperature_font,
                text=f"{max_app_temp_int}°C",
                fg=self.settings.max_app_temperature_fg,
                bg=self.settings.temperature_bg,
            )

            min_app_temp_int = temps['min_app_temp']
            min_app_temp = tk.Label(
                self.gui.root,
                font=self.settings.app_temperature_font,
                text=f"{min_app_temp_int}°C",
                fg=self.settings.min_app_temperature_fg,
                bg=self.settings.temperature_bg,
            )

            temp_types = \
                [max_amb_temp, min_amb_temp, max_app_temp, min_app_temp]
            for temp in temp_types:
                temp.update_idletasks()

            max_amb_temp.place(
                x=max_amb_temp_posx - max_amb_temp.winfo_reqwidth() // 2,
                y=self.settings.amb_temperature_posy
            )
            min_amb_temp.place(
                x=min_amb_temp_posx - min_amb_temp.winfo_reqwidth() // 2,
                y=self.settings.amb_temperature_posy
            )
            max_app_temp.place(
                x=max_app_temp_posx,
                y=self.settings.app_temperature_posy
            )
            min_app_temp.place(
                x=min_app_temp_posx,
                y=self.settings.app_temperature_posy
            )

    def _draw_max_min_labels(self,
                             max_amb_temp_posx: int,
                             min_amb_temp_posx: int,) -> None:
        """Draw the text labels "MAX" and "MIN" above the temperatures."""
        max_label = tk.Label(
            self.gui.root,
            font=self.settings.max_min_label_font,
            text="MAX",
            fg=self.settings.max_label_fg,
            bg=self.settings.temperature_bg,
        )
        max_label.update_idletasks()

        min_label = tk.Label(
            self.gui.root,
            font=self.settings.max_min_label_font,
            text="MIN",
            fg=self.settings.min_label_fg,
            bg=self.settings.temperature_bg,
        )
        min_label.update_idletasks()

        max_label.place(
            x=max_amb_temp_posx - max_label.winfo_reqwidth() // 2,
            y=self.settings.max_min_label_posy
        )
        min_label.place(
            x=min_amb_temp_posx - min_label.winfo_reqwidth() // 2,
            y=self.settings.max_min_label_posy
        )

    def _draw_feels_like_label(self,
                               posx: int):
        feels_like_label = tk.Label(
            self.gui.root,
            font=self.settings.feels_like_label_font,
            text='Feels like:',
            fg=self.settings.feels_like_label_fg,
            bg=self.settings.temperature_bg,
        )
        feels_like_label.update_idletasks()

        feels_like_label.place(
            x=posx,
            y=self.settings.feels_like_label_posy
        )

    def _get_temperatures(self) -> list[dict[str, int]]:
        """Get the temperatures for each forecast day."""
        temperatures = []
        for day in range(self.settings.forecast_days):
            max_amb_temp = (
                self.gui.fetcher.daily_data)['temperature_2m_max'][day]
            min_amb_temp = (
                self.gui.fetcher.daily_data)['temperature_2m_min'][day]
            max_app_temp = (
                self.gui.fetcher.daily_data)['apparent_temperature_max'][day]
            min_app_temp = (
                self.gui.fetcher.daily_data)['apparent_temperature_min'][day]
            temperatures.append({
                'max_amb_temp': round(max_amb_temp),
                'min_amb_temp': round(min_amb_temp),
                'max_app_temp': round(max_app_temp),
                'min_app_temp': round(min_app_temp),
            })
        self._check_list(temperatures)
        return temperatures

    def _check_list(self, list_: list[dict[str, int]]):
        """Check if list is valid."""
        if len(list_) != self.settings.forecast_days:
            raise RuntimeError("Unable to fetch temperatures for all 5 days. "
                               f"(temps: {list_})")
        for dic in list_:
            if len(list(dic.items())) != 4:
                raise RuntimeError("Unable to fetch all temperatures. "
                                   f"(temps: {list_})")
            for val in dic:
                if val is None:
                    raise RuntimeError('Unable to fetch all temperatures. '
                                       f' (temps: {list_})')
