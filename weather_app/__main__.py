"""Module entrypoint for running the WeatherApp via `python -m weather_app`."""

from __future__ import annotations

from pathlib import Path
import sys
import traceback
import tkinter.messagebox

from .utils import package_installer


def main() -> None:
    """Install dependencies (if needed) and launch the GUI."""
    try:
        requirements_path = Path(__file__).resolve().parents[1] / "requirements.txt"
        package_installer.install_requirements(requirements_path)

        from .app_gui import AppGUI

        weather_app = AppGUI()
        weather_app.run()

    except KeyboardInterrupt:
        print("\nProgram interrupted.")
        sys.exit(0)
    except Exception:
        tkinter.messagebox.showinfo(
            "ERROR :(",
            "An unexpected error occurred:"
            f"\n{traceback.format_exc()}"
            "\n\nPlease try again."
        )
        sys.exit(1)


if __name__ == "__main__":
    main()
