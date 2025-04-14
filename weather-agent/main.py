import asyncio
import os
from httpx import AsyncClient
from utils.agent import weather_agent
from utils.deps import Deps
from dotenv import load_dotenv

load_dotenv()

async def main():
    async with AsyncClient() as client:
        deps = Deps(
            client=client,
            weather_api_key=os.getenv("OPEN_WEATHER_API_KEY"),
            geo_api_key=os.getenv("GEO_API_KEY")
        )
        result = await weather_agent.run(user_prompt="What kind of weather is it in Pakistan?", deps=deps)
        print("response:", result.data)

if __name__ == "__main__":
    asyncio.run(main())
