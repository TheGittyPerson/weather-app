"""Module entrypoint for running the WeatherApp via `python -m weather_app`."""

from __future__ import annotations

import sys

from .app_gui import AppGUI


def main() -> None:
    """Install dependencies (if needed) and launch the GUI."""
    try:
        weather_app = AppGUI()
        weather_app.run()
    except KeyboardInterrupt:
        print("\nProgram interrupted.")
        sys.exit(0)


if __name__ == "__main__":
    main()
