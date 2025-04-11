import requests
from django.http import JsonResponse
from django.shortcuts import render


def get_weather(request):
    city = request.GET.get("city", "")
    lat = request.GET.get("lat")
    lon = request.GET.get("lon")

    if city:
        geocode_url = (
            f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1"
        )
        try:
            geo_response = requests.get(geocode_url, timeout=5)
            geo_data = geo_response.json()
            results = geo_data.get("results")
            if results:
                lat = results[0]["latitude"]
                lon = results[0]["longitude"]
                city_name = results[0]["name"]
                country_name = results[0]["country"]
            else:
                return render(
                    request,
                    "weather/weather.html",
                    {
                        "error": f"City '{city}' not found.",
                    },
                )
        except requests.exceptions.RequestException as e:
            return JsonResponse(
                {"error": "Geocoding failed", "details": str(e)}, status=500
            )
    elif lat and lon:
        geocode_url = f"https://geocoding-api.open-meteo.com/v1/reverse?latitude={lat}&longitude={lon}&count=1"
        try:
            geo_response = requests.get(geocode_url, timeout=5)
            geo_data = geo_response.json()
            results = geo_data.get("results")
            if results:
                city_name = results[0]["name"]
                country_name = results[0]["country"]
            else:
                return render(
                    request,
                    "weather/weather.html",
                    {
                        "error": f"Coordinates '{lat}, {lon}' not found.",
                    },
                )
        except requests.exceptions.RequestException as e:
            return JsonResponse(
                {"error": "Geocoding failed", "details": str(e)}, status=500
            )
    else:
        city_name = "Unknown"
        country_name = "Unknown"

    lat = lat or "52.52"
    lon = lon or "13.41"

    weather_url = (
        f"https://api.open-meteo.com/v1/forecast"
        f"?latitude={lat}&longitude={lon}&current_weather=true"
    )

    try:
        response = requests.get(weather_url, timeout=5)
        data = response.json()
        current_weather = data.get("current_weather", {})

        return render(
            request,
            "weather/weather.html",
            {
                "weather": current_weather,
                "city": city_name,
                "country": country_name,
                "lat": lat,
                "lon": lon,
            },
        )

    except requests.exceptions.RequestException as e:
        return JsonResponse(
            {"error": "Failed to fetch weather data", "details": str(e)}, status=500
        )
