import requests
from django.http import JsonResponse
from django.shortcuts import render


def get_weather(request):
    # Default coordinates are Berlin
    latitude = request.GET.get("lat", "52.52")
    longitude = request.GET.get("lon", "13.41")

    url = (
        f"https://api.open-meteo.com/v1/forecast"
        f"?latitude={latitude}&longitude={longitude}&current_weather=true"
    )

    try:
        response = requests.get(url, timeout=5)
        data = response.json()
        current_weather = data.get("current_weather", {})

        if request.headers.get("x-requested-with") == "XMLHttpRequest":
            return JsonResponse(current_weather)
        else:
            return render(request, "weather/weather.html", {"weather": current_weather})

    except requests.exceptions.RequestException as e:
        return JsonResponse(
            {"error": "Failed to fetch weather data", "details": str(e)}, status=500
        )
