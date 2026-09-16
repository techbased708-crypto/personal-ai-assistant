import os
from langchain_groq import ChatGroq
from langchain.agents import create_agent
from langchain.tools import tool
import requests

from dotenv import load_dotenv

# ✅ Sab tools ek file se import
from tools import (
    serpapi_search,
    get_weather,
    get_latest_news,
    calculate,
    get_datetime
)

load_dotenv()

llm = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0,
    max_retries=2,
    api_key=os.getenv("GROQ_API_KEY")
)

@tool
def search(query: str) -> str:
    """Google search karo current info ke liye."""
    return serpapi_search(query)
def get_weather(city: str) -> str:
    api_key = os.getenv("OPENWEATHER_API_KEY")

    if not api_key:
        return "❌ OPENWEATHER_API_KEY .env file mein nahi mili."

    url = "https://api.openweathermap.org/data/2.5/weather"

    params = {
        "q": city,
        "appid": api_key,
        "units": "metric"
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        data = response.json()

        if response.status_code != 200:
            return f"❌ Weather nahi mil saka: {data.get('message', 'Unknown error')}"

        temp = data["main"]["temp"]
        feels_like = data["main"]["feels_like"]
        humidity = data["main"]["humidity"]
        description = data["weather"][0]["description"]

        return (
            f"🌤️ {city} ka current weather:\n"
            f"Temperature: {temp}°C\n"
            f"Feels like: {feels_like}°C\n"
            f"Condition: {description}\n"
            f"Humidity: {humidity}%"
        )

    except Exception as e:
        return f"❌ Weather error: {str(e)}"

@tool
def weather(city: str) -> str:
    """Kisi city ka live weather batao."""
    return get_weather(city)

@tool
def news(topic: str) -> str:
    """Kisi topic ki latest news lao."""
    return get_latest_news(topic)

@tool
def calculator(expression: str) -> str:
    """Math calculate karo. Jaise '15 * 200' ya 'sqrt(81)'."""
    return calculate(expression)

@tool
def current_time(timezone: str) -> str:
    """Current date aur time batao. City name do jaise 'Lahore' ya 'London'."""
    return get_datetime(timezone)


ALL_TOOLS = [search, weather, news, calculator, current_time]

def get_agent():
    agent = create_agent(
        model=llm,
        tools=ALL_TOOLS,
        system_prompt="You are a helpful personal AI assistant. Use the available tools when needed."
    )

    return agent