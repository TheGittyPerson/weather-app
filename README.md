# WeatherApp

A desktop weather app with a Tkinter GUI that fetches forecasts from Open-Meteo and displays daily conditions, temperatures, humidity, and more.

## Requirements

- Python 3.12 and above recommended
- Internet connection

## Setup

1. Create a virtual environment:

```bash
python -m venv .venv
```

2. Activate the virtual environment:

```bash
source .venv/bin/activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

## Run

```bash
python -m weather_app
```

The entrypoint auto-installs any missing third-party packages listed in
`requirements.txt` before launching the GUI.

## Project Layout

- `weather_app`: application code
- `weather_app/assets/graphics`: image assets used by the GUI

## pyproject.toml

`pyproject.toml` is included for tool and packaging metadata. The app does not
require it to run; `requirements.txt` remains the source of runtime
dependencies.

## Notes

- The app uses IP-based geolocation for coordinates.
- The Open-Meteo client caches responses locally (you may see a `.cache.sqlite` file created).
