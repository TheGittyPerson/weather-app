"""A module to manage weather humidity visualization."""

from datetime import datetime, timedelta

from .data_labels import DataLabels


class HumidityLabels(DataLabels):
    """Extracts and draws humidity data to screen."""

    def draw(self):
        """Draw humidity level and severity labels to the screen."""
        humidities, average_humidities = self._get_humidity()

        for day_num, humidity in enumerate(humidities):
            self._create_text(
                self._posx(day_num),
                self.settings.humidity_posy,
                font=self.settings.humidity_font + ("bold",),
                text="Humidity:",
                fill=self.settings.humidity_fg,
            )
            self._create_text(
                self._posx(day_num),
                self.settings.humidity_posy + 25,
                font=self.settings.humidity_font,
                text=f'{humidity} ({average_humidities[day_num]}%)',
                fill=self.settings.humidity_fg,
            )

            label_str, label_fill = (
                self._get_humidity_severities(average_humidities[day_num]))
            self._create_text(
                self._posx(day_num),
                self.settings.humidity_sev_posy,
                font=self.settings.humidity_sev_font,
                text=label_str,
                fill=label_fill,
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

        return (
            self._check_list(humidities_str), self._check_list(humidities_avg)
        )

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
            return 'Low', '#fc7703'
        if 30 < humidity < 40:
            return 'Moderately Low', '#fcba03'
        if 40 <= humidity <= 60:
            return 'Moderate', 'green'
        if 60 < humidity <= 70:
            return 'Moderately High', '#fcba03'
        if 70 < humidity < 80:
            return 'High', 'orange'
        if 80 <= humidity:
            return 'Very High', 'red'
        raise RuntimeError("Shouldn't Happen")

    def _check_list[T: (str, int)](self, ls: list[T]) -> list[T]:
        """
        Checks:
            - Whether humidity data is given for all requested days
        """
        if len(ls) != self.settings.forecast_days:
            raise RuntimeError('Unable to fetch humidity for all '
                               f'{self.settings.forecast_days} days.'
                               f' (humidity: {ls})')
        return ls
