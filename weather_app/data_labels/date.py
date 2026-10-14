"""This is a module to display the dates one the WeatherApp window."""

from datetime import datetime, timedelta

from ..gui_settings import GUISettings


class DateLabels:
    def __init__(self, gui):
        self.gui = gui
        self.settings = GUISettings()

    def draw(self):
        """Display dates in the window."""
        dates = self._get_dates()
        for i, date in enumerate(dates):
            self.gui.window.create_text(
                (i + 0.5) * (self.settings.window_width
                             // self.settings.forecast_days),
                self.settings.date_posy,
                text=self._get_formatted_date(date),
                font=self.settings.date_font,
                fill=self.settings.date_color,
            )

    def _get_dates(self) -> list[str]:
        """Get formatted dates for each forecast day."""
        today = datetime.now()
        dates = []
        for i in range(self.gui.fetcher.forecast_days):
            date = today + timedelta(days=i)
            formatted_date = date.strftime('%a %d/%m')
            dates.append(formatted_date)
        return dates

    @staticmethod
    def _get_formatted_date(date: str) -> str:
        parts = date.split(' ')
        day_month = parts[1].split('/')

        day = day_month[0].lstrip('0')
        month = day_month[1].lstrip('0')

        formatted_date = f"{parts[0]} {day}/{month}"

        return formatted_date
