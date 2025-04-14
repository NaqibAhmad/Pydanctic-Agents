from typing import Annotated
from pydantic import BaseModel, Field
from pydantic_ai import RunContext, ModelRetry
from utils.deps import Deps
import logfire

class LatLong(BaseModel):
    lat: Annotated[float, Field(..., description="Latitude")]
    long: Annotated[float, Field(..., description="Longitude")]
    
async def get_lat_long(ctx: RunContext[Deps], location_description: str) -> dict[str, float]:
    if ctx.deps.geo_api_key is None:
        return {'lat': 51.1, 'long': -0.1}
    
    params = {
        'q': location_description,
        'key': ctx.deps.geo_api_key,
        'format': 'json'
    }

    with logfire.span("calling geocode api", params=params) as span:
        r = await ctx.deps.client.get("https://geocode.maps.co/search", params=params)
        r.raise_for_status()
        data = r.json()
        span.set_attribute("response", data)

    if data and isinstance(data, list) and 'lat' in data[0] and 'lon' in data[0]:
        return {'lat': float(data[0]['lat']), 'long': float(data[0]['lon'])}
    else:
        raise ModelRetry("Couldn't find the location")
