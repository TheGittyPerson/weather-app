"""Contains the UVILabels class."""

import tkinter as tk

from .data_labels import DataLabels


class UVILabels(DataLabels):
    """Extract and display UV index info to screen."""

    def draw(self) -> None:
        """Draw UV index info to screen."""
        uvis: list[float] = self._get_uv_indices()
        uvi_sevs: list[tk.Label] = self._get_uv_severities(uvis)

        for day_num, uvi, sev_label in zip(
                range(self.settings.forecast_days), uvis, uvi_sevs):
            self._create_text(
                self._posx(day_num),
                self.settings.uvi_posy,
                font=self.settings.uvi_font + ("bold",),
                text="UV Index:",
                fill=self.settings.uvi_fg,
            )
            self._create_text(
                self._posx(day_num),
                self.settings.uvi_posy + 20,
                font=self.settings.uvi_font,
                text=f"{uvi:g}",
                fill=self.settings.uvi_fg,
            )
            sev_label.place(
                x=self._posx(day_num),
                y=self.settings.uvi_sev_posy,
                anchor="center"
            )

    def _get_uv_indices(self) -> list[float]:
        """Extract max UV indices for requested days."""
        out = self.gui.fetcher.daily_data["uv_index_max"]
        return self._check_list([round(float(x), 1) for x in out])

    def _get_uv_severities(self, uvis: list[float]) -> list[tk.Label]:
        """Determine UV severities based on max UV indices.

        Returns list of ``tk.Label`` objects that can be directly drawn to
        screen.

        Severity based on WHO's official guidelines:
        https://www.who.int/news-room/questions-and-answers/item/radiation-the-ultraviolet-(uv)-index
        """
        sev_mapping: dict[int, list[str]] = {
            0: ["Low", "green"],
            1: ["Low", "green"],
            2: ["Low", "green"],
            3: ["Moderate", "#80b334"],
            4: ["Moderate", "#80b334"],
            5: ["Moderate", "#80b334"],
            6: ["High", "#fc7703"],
            7: ["High", "#fc7703"],
            8: ["Very High", "red"],
            9: ["Very High", "red"],
            10: ["Very High", "red"],
            11: ["Extreme", "purple"]
        }
        return [
            tk.Label(
                self.gui.root,
                font=self.settings.uvi_sev_font,
                text=sev_mapping[int(uvis[day_num])][0],
                fg=sev_mapping[int(uvis[day_num])][1],
                bg=self.settings.uvi_bg,
            ) for day_num, uvi in enumerate(uvis)
        ]

    def _check_list(self, ls: list[float]) -> list[float]:
        """
        Checks:
            - Whether UVI data is given for all requested days
            - Whether UVIs are positive/zero integers
        """
        if len(ls) != self.settings.forecast_days:
            raise RuntimeError('Unable to fetch humidity for all '
                               f'{self.settings.forecast_days} days.'
                               f' (humidity: {ls})')
        if not all([
            isinstance(x, float) and x >= 0
            for x in ls
        ]):
            raise RuntimeError('Collected UV indices are not >= 0. '
                               f' (Got: {ls})')
        return ls
