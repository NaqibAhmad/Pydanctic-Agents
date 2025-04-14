from dataclasses import dataclass
from httpx import AsyncClient

@dataclass
class Deps:
    client: AsyncClient
    weather_api_key: str
    geo_api_key: str
