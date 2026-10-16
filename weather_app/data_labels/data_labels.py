"""Contains the DataLabel base class."""

from abc import ABC
from typing import TYPE_CHECKING

from ..gui_settings import GUISettings

if TYPE_CHECKING:
    from ..app_gui import AppGUI


class DataLabels(ABC):
    def __init__(self, gui: AppGUI) -> None:
        """Initialize Settings instance and reference to GUI."""
        self.gui = gui
        self.settings = GUISettings()

    def draw(self) -> None:
        """Draw data for all dates to screen."""
        raise NotImplementedError

    def _create_text(self, *args, **kw) -> None:
        """Draw text to screen. Same as ``self.gui.window.create_text()``."""
        self.gui.window.create_text(*args, **kw)

    def _posx(self, day_num: int) -> int:
        """Get x position of an element based on day number."""
        return (day_num + 0.5) * (self.settings.window_width
                                  // self.settings.forecast_days)

    def _check_list[T](self, ls: list[T]) -> list[T]:
        """Check if the given list contains enough data after extracting.

        Returns list if no issues.
        Call this write before returning the final values in the get() methods.
        Should raise a RuntimeError if not.
        """
        raise NotImplementedError
