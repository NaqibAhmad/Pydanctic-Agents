from pydantic import BaseModel, Field
from typing import Annotated
from pydantic_ai import RunContext
from utils.deps import Deps
import logfire


class WeatherInfo(BaseModel):
    temp: Annotated[str, Field(description="Temperature in Celsius, e.g. '26°C'")]
    description: Annotated[str, Field(description="Short description of the weather")]


async def get_weather(
    ctx: RunContext[Deps],
    lat: Annotated[float, Field(description="Latitude of the location")],
    long: Annotated[float, Field(description="Longitude of the location")]
) -> WeatherInfo:
    if ctx.deps.weather_api_key is None:
        return WeatherInfo(temp="21°C", description="Sunny")

    params = {
        'apikey': ctx.deps.weather_api_key,
        'location': f"{lat},{long}",
        'units': 'metric'
    }

    with logfire.span("calling weather api", params=params) as span:
        r = await ctx.deps.client.get("https://api.tomorrow.io/v4/weather/realtime", params=params)
        r.raise_for_status()
        data = r.json()
        span.set_attribute("response", data)

    values = data["data"]["values"]
    code_lookup = {
        1000: 'Clear, Sunny',
        1100: 'Mostly Clear',
        1101: 'Partly Cloudy',
        1102: 'Mostly Cloudy',
        1001: 'Cloudy',
        2000: 'Fog',
        2100: 'Light Fog',
        4000: 'Drizzle',
        4001: 'Rain',
        4200: 'Light Rain',
        4201: 'Heavy Rain',
        5000: 'Snow',
        5001: 'Flurries',
        5100: 'Light Snow',
        5101: 'Heavy Snow',
        6000: 'Freezing Drizzle',
        6001: 'Freezing Rain',
        6200: 'Light Freezing Rain',
        6201: 'Heavy Freezing Rain',
        7000: 'Ice Pellets',
        7101: 'Heavy Ice Pellets',
        7102: 'Light Ice Pellets',
        8000: 'Thunderstorm',
    }

    return WeatherInfo(
        temp=f'{values["temperatureApparent"]:0.0f}°C',
        description=code_lookup.get(values['weatherCode'], 'Unknown')
    )
