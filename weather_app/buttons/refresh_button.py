"""A module to manage and draw the refresh button to the WeatherApp."""

import tkinter as tk

from ..gui_settings import GUISettings
from ..graphics import Graphics


class RefreshButton:
    """A class to manage and draw the refresh button to the WeatherApp."""
    def __init__(self, gui):
        """Initialize the refresh button."""
        self.gui = gui
        self.settings = GUISettings()
        self.graphics = Graphics()

        self.refresh_button = tk.Button(
            self.gui.root,
            image=self.graphics.refresh_icon,
            command=self.gui.refresh
        )
        self._place_refresh_button()

    def _place_refresh_button(self):
        """Draw the button in the lower-right corner of the window."""
        self.refresh_button.place(
            x=self.settings.refresh_icon_posx,
            y=self.settings.refresh_icon_posy
        )
        self.refresh_button.lift()
