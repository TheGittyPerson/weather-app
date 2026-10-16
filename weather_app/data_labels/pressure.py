"""Contains the PressureLabels class."""

from itertools import batched

from .data_labels import DataLabels


class PressureLabels(DataLabels):
    """Extract and display pressure info to screen."""

    def draw(self) -> None:
        """Draw pressure info to screen."""
        pressures: list[float] = self._get_pressures()

        for day_num, pressure in zip(
                range(self.settings.forecast_days), pressures):
            self._create_text(
                self._posx(day_num),
                self.settings.pressure_posy,
                font=self.settings.pressure_font + ("bold",),
                text=f"Surface pressure:",
                fill=self.settings.pressure_fg,
            )
            self._create_text(
                self._posx(day_num),
                self.settings.pressure_posy + 25,
                font=self.settings.pressure_font,
                text=f"{pressure:g} hPa",
                fill=self.settings.pressure_fg,
            )

    def _get_pressures(self) -> list[float]:
        """Extract average daily surface pressures for requested days.

        In hPa. Compresses data for given hourly data into daily data by
        calculating average.
        """
        out = self.gui.fetcher.hourly_data["surface_pressure"]
        floatified = [float(x) for x in out]
        return self._check_list(
            [round(sum(chunk) / 24, 1) for chunk in batched(floatified, 24)],
        )

    def _check_list(self, ls: list[float]) -> list[float]:
        """Checks whether data is given for all requested days."""
        if len(ls) != self.settings.forecast_days:
            raise RuntimeError('Unable to fetch pressure data for all '
                               f'{self.settings.forecast_days} days.'
                               f' (list: {ls})')
        return ls
