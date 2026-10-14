"""A module to manage weather humidity visualization."""

import tkinter as tk
from datetime import datetime, timedelta
from typing import cast, Literal

from .data_labels import DataLabels


class HumidityLabels(DataLabels):
    """Extracts and draws humidity data to screen."""

    def draw(self):
        """Draw humidity level and severity labels to the screen."""
        humidities, average_humidities = self._get_humidity()

        for day_num, humidity in enumerate(humidities):
            humidity_posx = (
                (day_num + 0.5)
                * (self.settings.window_width // self.settings.forecast_days)
            )
            humidity_level_posx = humidity_posx

            self._draw_humidity_severity(average_humidities[day_num],
                                         humidity_level_posx)

            humidity_label = tk.Label(
                self.gui.root,
                font=self.settings.humidity_font,
                text=f'Humidity:\n{humidity} '
                     f'({average_humidities[day_num]}%)',
                fg=self.settings.humidity_fg,
                bg=self.settings.humidity_bg,
            )

            humidity_label.update_idletasks()

            humidity_label.place(
                x=humidity_posx - humidity_label.winfo_reqwidth() // 2,
                y=self.settings.humidity_posy
            )

    def _draw_humidity_severity(self, humidity: int, posx: int):
        """Draw humidity severities (ex: very humid, moderately humid)
         to the screen.
         """
        label_str, label_fg = self._get_humidity_severities(humidity)
        humidity_level_label = tk.Label(
            self.gui.root,
            font=self.settings.humidity_sev_font,
            text=label_str,
            fg=label_fg,
            bg=self.settings.humidity_bg,
        )

        humidity_level_label.update_idletasks()

        self.settings.humidity_sev_anchor = cast(
            Literal["nw", "n", "ne", "w", "center", "e", "sw", "s", "se"],
            self.settings.humidity_sev_anchor,
        )
        humidity_level_label.place(
            x=posx,
            y=self.settings.humidity_sev_posy,
            anchor=self.settings.humidity_sev_anchor,
        )

    def _get_humidity(self) -> tuple[list[str], list[int]]:
        """Get the humidity for each forecast day."""
        humidities_str = []
        humidities_avg = []

        hourly_data = []
        for v in self.gui.fetcher.hourly_data['relative_humidity_2m']:
            hourly_data.append(round(float(v)))

        timestamps = []
        for timestamp in self.gui.fetcher.hourly_data['date']:
            timestamps.append(str(timestamp))

        for day_num in range(self.settings.forecast_days):
            date = self._get_date(day_num)

            today_indices = [i for i, s in enumerate(timestamps) if
                             s.startswith(date)]

            current_lp_hourly_data = [hourly_data[i] for i in today_indices]

            humidities_avg.append(round(
                sum(current_lp_hourly_data) / len(current_lp_hourly_data)))
            humidities_str.append(
                f'{min(current_lp_hourly_data)}-{max(current_lp_hourly_data)}%')

        self._check_list(humidities_str)
        self._check_list(humidities_avg)

        return humidities_str, humidities_avg

    @staticmethod
    def _get_date(days_offset: int) -> str:
        """Gate date based on day offset from today"""
        today = datetime.today()
        future_date = today + timedelta(days=days_offset)
        return str(future_date.strftime('%Y-%m-%d'))

    @staticmethod
    def _get_humidity_severities(humidity: int) -> tuple[str, str]:
        """Get humidity severity (ex: very humid, moderately humid)
         based on humidity percentage
         """
        if humidity <= 20:
            return 'Very Low', 'red'
        if 20 < humidity <= 30:
            return 'Low', 'red'
        if 30 < humidity < 40:
            return 'Moderately Low', 'yellow'
        if 40 <= humidity <= 60:
            return 'Moderate', 'green'
        if 60 < humidity <= 70:
            return 'Moderately High', 'yellow'
        if 70 < humidity < 80:
            return 'High', 'red'
        if 80 <= humidity:
            return 'Very High', 'red'
        raise RuntimeError("Shouldn't Happen")

    def _check_list(self, ls: list[str | int]) -> None:
        """
        Checks:
            - Whether humidity data is given for all requested days
        """
        if len(ls) != self.settings.forecast_days:
            raise RuntimeError('Unable to fetch humidity for all '
                               f'{self.settings.forecast_days} days.'
                               f' (humidity: {ls})')
