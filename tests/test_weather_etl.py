from app.etl.weather_etl import (
    transform_weather
)


def test_transform_weather():

    sample = {

        "name": "Nairobi",

        "main": {
            "temp": 25,
            "humidity": 60
        },

        "wind": {
            "speed": 5
        },

        "weather": [
            {
                "main": "Clouds"
            }
        ]
    }

    result = transform_weather(
        sample
    )

    assert result["city"] == "Nairobi"

    assert result["temperature"] == 25

    assert result["humidity"] == 60