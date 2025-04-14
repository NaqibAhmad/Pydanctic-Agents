import os
from dotenv import load_dotenv
from pydantic_ai import Agent
from pydantic_ai.models.groq import GroqModel
from pydantic_ai.models.openai import OpenAIModel
from utils.deps import Deps
from utils.tools.get_lat_long import get_lat_long
from utils.tools.get_weather import get_weather
import logfire

load_dotenv()
logfire.configure()

model_name = "gpt-4o"
model = OpenAIModel(model_name=model_name)

weather_agent = Agent(
    model=model,
    deps_type=Deps,
    retries=2,
    instrument=True,
    system_prompt="""
    ENOFORCED INSTRUCTIONS:
        a. You are a weahterh agent, and your job is answer weather realted queries only.
        b. Be concise and reply in a single line of text.
        c. To answer weather-related questions:
            - First, use the `get_lat_long` tool to convert the location into coordinates.
            - ENFORCED STATEMENT: Once you have the resulting latitude and longitude, use the `get_weather` tool to get the weather of the location.
        d. Only return the weather after calling both tools.
    """
)

# Register tools
weather_agent.tool(get_lat_long)
weather_agent.tool(get_weather)
