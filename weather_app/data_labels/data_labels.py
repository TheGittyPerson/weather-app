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

    def _check_list(self, ls: list) -> None:
        """Check if the given list contains enough data after extracting.

        Call this write before returning the final values in the get() methods.
        Should raise a RuntimeError if not.
        """
        raise NotImplementedError
