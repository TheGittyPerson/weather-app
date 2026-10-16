"""Contains the UVILabels class."""

import tkinter as tk

from .data_labels import DataLabels


class WindLabels(DataLabels):
    """Extract and display wind speed and direction info to screen."""

    def draw(self) -> None:
        """Draw wind info to screen."""
        speeds: list[float] = self._get_wind_speeds()
        directions: list[str] = self._get_wind_directions()

        for day_num, speed, direction_text in zip(
                range(self.settings.forecast_days), speeds, directions):

            posx = (
                    (day_num + 0.5) * (self.settings.window_width
                                       // self.settings.forecast_days)
            )

            tk.Label(
                self.gui.root,
                font=self.settings.wind_font + ("bold",),
                text=f"Max wind speed:",
                fg=self.settings.wind_fg,
                bg=self.settings.window_bg,
            ).place(
                x=posx,
                y=self.settings.wind_posy,
                anchor="center"
            )

            tk.Label(
                self.gui.root,
                font=self.settings.wind_font,
                text=f"{speed:g} km/h | {direction_text}",
                fg=self.settings.wind_fg,
                bg=self.settings.window_bg,
            ).place(
                x=posx,
                y=self.settings.wind_posy + 25,
                anchor="center"
            )

    def _get_wind_speeds(self) -> list[float]:
        """Extract maximum wind speeds for requested days.

        In km/h.
        """
        out = self.gui.fetcher.daily_data["wind_speed_10m_max"]
        return self._check_list([round(float(x), 1) for x in out])

    def _get_wind_directions(self) -> list[str]:
        """Extract dominant wind direction for requested days

        In degrees. Returns string to be displayed directly on screen.
        """
        degrees = self.gui.fetcher.daily_data["wind_direction_10m"]
        degrees = self._check_list([round(float(x), 1) for x in degrees])

        directions = ["N", "NE", "E", "SE", "S", "SW", "W", "NW", "N"]
        arrows = ["↑", "↗", "→", "↘", "↓", "↙", "←", "↖", "↑"]
        indices = [int((degree + 22.5) // 45) for degree in degrees]
        cardinals = [f"{directions[i]} {arrows[i]}" for i in indices]

        return [f"{degree:g}º ({cardinal})"
                for degree, cardinal in zip(degrees, cardinals)]

    def _check_list(self, ls: list[float]) -> list[float]:
        """Checks whether data is given for all requested days."""
        if len(ls) != self.settings.forecast_days:
            raise RuntimeError('Unable to fetch wind data for all '
                               f'{self.settings.forecast_days} days.'
                               f' (list: {ls})')
        return ls
