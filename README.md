# Django Weather API Project

A simple Django project that fetches and displays weather data using the [Open-meteo](https://open-meteo.com/) API.

## Features

- Fetch current weather data from the Open-meteo API
- User input for location (latitude & longitude) or the name of the city
- Focus on clean backend architecture using Django

## Requirements

- Python 3.8+
- Django 4.x
- `requests` library

Install dependencies:

```bash
pip install -r requirements.txt
```

## How It Works

1. User submits a location (latitude and longitude) or the name of the city.
2. Backend sends a GET request to the Open-meteo API.
3. Parsed weather data is returned to the user as JSON or rendered on a template.

Example Open-meteo endpoint:

```
https://api.open-meteo.com/v1/forecast?latitude=52.52&longitude=13.41&current_weather=true
```

## Running the Project

```bash
python manage.py runserver
```

Navigate to `http://127.0.0.1:8000/` in your browser.
