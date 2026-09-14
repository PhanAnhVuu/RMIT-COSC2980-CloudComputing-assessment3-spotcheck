# =============================================================================
# COSC2980/2638 Cloud Computing - Assessment 3
# Lambda function: fetches current weather for RMIT Hanoi Campus from the
# Open-Meteo third-party API.
#
# Triggered by: API Gateway GET /weather
#
# References (IEEE):
# [1] Open-Meteo, "Weather Forecast API," 2024. [Online].
#     Available: https://open-meteo.com/en/docs
# =============================================================================

import json
import urllib.request

HANOI_LAT = "21.0285"
HANOI_LON = "105.8542"

CORS_HEADERS = {
    "Access-Control-Allow-Origin": "*",
    "Content-Type": "application/json",
}

WEATHER_CODES = {
    0: "Clear sky",
    1: "Mainly clear", 2: "Partly cloudy", 3: "Overcast",
    45: "Fog", 48: "Depositing rime fog",
    51: "Light drizzle", 53: "Moderate drizzle", 55: "Dense drizzle",
    61: "Slight rain", 63: "Moderate rain", 65: "Heavy rain",
    80: "Slight rain showers", 81: "Moderate rain showers", 82: "Violent rain showers",
    95: "Thunderstorm",
}


def lambda_handler(event, context):
    url = (
        f"https://api.open-meteo.com/v1/forecast"
        f"?latitude={HANOI_LAT}&longitude={HANOI_LON}"
        f"&current_weather=true"
    )

    try:
        with urllib.request.urlopen(url, timeout=10) as response:
            data = json.loads(response.read())
    except Exception as exc:
        return {
            "statusCode": 500,
            "headers": CORS_HEADERS,
            "body": json.dumps({"error": str(exc)}),
        }

    current = data["current_weather"]
    code = current.get("weathercode", -1)

    result = {
        "temperature": current["temperature"],
        "description": WEATHER_CODES.get(code, "Unknown"),
        "city": "Hanoi",
    }

    return {
        "statusCode": 200,
        "headers": CORS_HEADERS,
        "body": json.dumps(result),
    }