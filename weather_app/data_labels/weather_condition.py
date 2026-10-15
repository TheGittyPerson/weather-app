"""
A module to manage weather icon display.
"""

import tkinter as tk

from ..gui_settings import GUISettings


class WeatherConditionIcons:
    def __init__(self, gui):
        """Initalize self."""
        self.gui = gui
        self.settings = GUISettings()

    def draw(self):
        """Draw the weather icons and descriptions."""
        self.draw_weather_icons()
        self.draw_weather_descriptions()

    def draw_weather_icons(self):
        """Draw the weather weather_conditions to the screen."""
        icons = self._get_weather_icons()
        for day_num, icon in enumerate(icons):
            x_position = (
                (day_num + 0.5) * (self.settings.window_width //
                                   self.settings.forecast_days)
            )
            temp_iconlabel = tk.Label(
                self.gui.root,
                bg=self.settings.icons_bg,
                image=icon,
            )
            temp_iconlabel.place(
                x=x_position - icon.width() // 2,
                y=self.settings.icons_posy
            )

    def draw_weather_descriptions(self):
        descriptions = self._get_weather_descriptions()
        for day_num, des in enumerate(descriptions):
            x_position = (
                (day_num + 0.5) * (self.settings.window_width //
                                   self.settings.forecast_days)
            )

            des_label = tk.Label(
                self.gui.root,
                font=self.settings.descriptions_font,
                text=des,
                bg=self.settings.descriptions_bg,
                fg=self.settings.descriptions_fg,
            )

            des_label.update_idletasks()

            des_label.place(
                x=x_position - des_label.winfo_reqwidth() // 2,
                y=self.settings.descriptions_posy
            )

    def _get_weather_icons(self) -> list[tk.PhotoImage]:
        """Get the weather weather_conditions (as tk.PhotoImage objects)
         for each forecast day.
         """
        weather_icons = []
        weather_codes = self._get_weather_codes()

        for code in weather_codes:
            for codes_tuple, icon in self.settings.weather_icon_mapping.items():
                if code in codes_tuple:
                    weather_icons.append(icon)

        return self._check_list(weather_icons)

    def _get_weather_descriptions(self) -> list[str]:
        """Fetch the weather descriptions for each forecast day."""
        weather_des = []
        weather_codes = self._get_weather_codes()

        for code in weather_codes:
            weather_des.append(self.settings.weather_description_mapping[code])

        return self._check_list(weather_des)

    def _get_weather_codes(self) -> list[int]:
        """Fetch the weather code for each forecast day."""
        weather_codes = []
        for day in range(self.settings.forecast_days):
            weather_codes.append(
                self.gui.fetcher.daily_data['weather_code'][day]
            )
        return weather_codes

    def _check_list[T: (tk.PhotoImage, str)](self, ls: list[T]) -> list[T]:
        """Check if the weather_conditions or descriptions list is valid."""
        if len(ls) != self.settings.forecast_days:
            raise RuntimeError(
                "Unable to find weather icon for the provided weather code. "
                f"(weather_conditions list length: {len(ls)})"
            )
        return ls
