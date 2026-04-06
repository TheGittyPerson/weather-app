"""This module is for managing external graphics of the WeatherApp."""

from pathlib import Path
import tkinter as tk


class Graphics:
    def __init__(self):
        """Initaialize attributes."""
        # Loading Screen
        assets_dir = Path(__file__).resolve().parent / "assets" / "graphics"
        self.loading_screen = tk.PhotoImage(
            file=str(assets_dir / "loading_screen.png")
        )

        # Weather Icons
        self.clear = tk.PhotoImage(file=str(assets_dir / "clear.png"))
        self.cloudy = tk.PhotoImage(file=str(assets_dir / "cloudy.png"))
        self.part_cloudy = tk.PhotoImage(file=str(assets_dir / "part_cloudy.png"))
        self.rain_1 = tk.PhotoImage(file=str(assets_dir / "rain_1.png"))
        self.rain_2 = tk.PhotoImage(file=str(assets_dir / "rain_2.png"))
        self.rain_3 = tk.PhotoImage(file=str(assets_dir / "rain_3.png"))
        self.snow_1 = tk.PhotoImage(file=str(assets_dir / "snow_1.png"))
        self.snow_2 = tk.PhotoImage(file=str(assets_dir / "snow_2.png"))
        self.snow_3 = tk.PhotoImage(file=str(assets_dir / "snow_3.png"))
        self.thunderstorm = tk.PhotoImage(
            file=str(assets_dir / "thunderstorm.png")
        )

        # Refresh icon
        self.refresh_icon = tk.PhotoImage(file=str(assets_dir / "refresh.png"))
