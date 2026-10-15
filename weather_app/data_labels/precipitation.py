"""Contains the PrecipitationLabels class."""

import tkinter as tk

from .data_labels import DataLabels


class PrecipitationLabels(DataLabels):
    """Extracts and draws precipitation data to screen."""

    def draw(self):
        """Draw precipitation data to the screen."""
        precip_probs = self._get_precip_probs()
        precip_sums = self._get_precip_sums()
        precip_hours = self._get_precip_hours()
        for day_num, prob, sum_, hours in (
                zip(
                    range(self.settings.forecast_days),
                    precip_probs,
                    precip_sums,
                    precip_hours
                )):

            posx = (
                (day_num + 0.5) * (self.settings.window_width
                                   // self.settings.forecast_days)
            )

            text = "Precipitation:"
            if prob < self.settings.precip_prob_threshold:
                text += " -"
            else:
                text += f"\n{prob:g}%, {sum_:g} mm, {hours:g} hrs"

            label = tk.Label(
                self.gui.root,
                font=self.settings.precip_font,
                text=text,
                fg=self.settings.precip_fg,
                bg=self.settings.precip_bg,
            )

            label.update_idletasks()
            label.place(
                x=posx,
                y=self.settings.precip_posy,
                anchor="center"
            )

    def _get_precip_probs(self) -> list[int]:
        """Get mean precipitation probability for all days."""
        out = self.gui.fetcher.daily_data["precipitation_probability_mean"]
        self._check_list(out)
        return [round(x) for x in out]

    def _get_precip_sums(self) -> list[int]:
        """Get the precipitation depths for each forecast day."""
        out = self.gui.fetcher.daily_data["precipitation_sum"]
        self._check_list(out)
        return [round(x, 1) for x in out]

    def _get_precip_hours(self) -> list[int]:
        """Get number of hours it will rain for.

        The API docs says "rain" even though the other precipitation params
        refer to precipitation in general.
        """
        out = self.gui.fetcher.daily_data["precipitation_hours"]
        self._check_list(out)
        return out

    def _check_list(self, ls: list[int]) -> None:
        """
        Checks:
            - Whether precipitation data is given for all requested days
        """
        if len(ls) != self.settings.forecast_days:
            raise RuntimeError('Unable to fetch precipitation for all '
                               f'{self.settings.forecast_days} days.'
                               f' (precipitation: {ls})')
