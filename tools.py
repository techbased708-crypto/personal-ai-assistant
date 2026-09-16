import os
import math
import requests
import pytz
from datetime import datetime
from serpapi import GoogleSearch

# ══════════════════════════════════════════
# 🔍 TOOL 1: Google Search
# ══════════════════════════════════════════
def serpapi_search(query: str) -> str:
    """
    Google pe search karta hai SerpAPI se.
    Use karo jab koi current info chahiye.
    """
    params = {
        "q": query,
        "hl": "en",
        "gl": "us",
        "api_key": os.getenv("SERP_API_KEY")
    }
    search = GoogleSearch(params)
    results = search.get_dict()

    if "organic_results" in results:
        output = ""
        for r in results["organic_results"][:5]:
            output += f"Title: {r['title']}\n"
            output += f"Snippet: {r.get('snippet', 'N/A')}\n"
            output += f"Link: {r['link']}\n\n"
        return output

    return "No results found."


# ══════════════════════════════════════════
# ☀️ TOOL 2: Weather
# ══════════════════════════════════════════
def get_weather(city: str) -> str:
    """
    Kisi bhi city ka current weather batata hai.
    """
    api_key = os.getenv("WEATHER_API_KEY")
    url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city,
        "appid": api_key,
        "units": "metric"
    }
    try:
        response = requests.get(url, params=params)
        data = response.json()

        if data.get("cod") != 200:
            return f"City '{city}' nahi mila. Dobara check karo."

        return f"""
🌍 City: {data['name']}, {data['sys']['country']}
🌡️ Temperature: {data['main']['temp']}°C
🤔 Feels like: {data['main']['feels_like']}°C
💧 Humidity: {data['main']['humidity']}%
🌤️ Condition: {data['weather'][0]['description'].capitalize()}
💨 Wind Speed: {data['wind']['speed']} m/s
        """.strip()

    except Exception as e:
        return f"Weather fetch karne mein error: {str(e)}"


# ══════════════════════════════════════════
# 📰 TOOL 3: Latest News
# ══════════════════════════════════════════
def get_latest_news(topic: str) -> str:
    """
    Kisi bhi topic ki latest news laata hai.
    """
    api_key = os.getenv("NEWS_API_KEY")
    url = "https://newsapi.org/v2/everything"
    params = {
        "q": topic,
        "sortBy": "publishedAt",
        "pageSize": 5,
        "language": "en",
        "apiKey": api_key
    }
    try:
        response = requests.get(url, params=params)
        data = response.json()

        if data.get("status") != "ok" or not data.get("articles"):
            return f"'{topic}' ke baare mein koi news nahi mili."

        output = f"📰 Latest news about '{topic}':\n\n"
        for i, article in enumerate(data["articles"], 1):
            output += f"{i}. {article['title']}\n"
            output += f"   Source: {article['source']['name']}\n"
            output += f"   {article.get('description', '')}\n"
            output += f"   🔗 {article['url']}\n\n"
        return output

    except Exception as e:
        return f"News fetch karne mein error: {str(e)}"


# ══════════════════════════════════════════
# 🧮 TOOL 4: Calculator
# ══════════════════════════════════════════
def calculate(expression: str) -> str:
    """
    Math calculations karta hai.
    """
    try:
        allowed = {
            "sqrt": math.sqrt, "log": math.log,
            "log10": math.log10, "sin": math.sin,
            "cos": math.cos, "tan": math.tan,
            "pi": math.pi, "e": math.e,
            "abs": abs, "round": round, "pow": pow
        }
        result = eval(expression, {"__builtins__": {}}, allowed)
        return f"🧮 {expression} = {result}"

    except ZeroDivisionError:
        return "❌ Zero se divide nahi kar sakte!"
    except Exception as e:
        return f"❌ Expression samajh nahi aaya: {str(e)}"


# ══════════════════════════════════════════
# 🕐 TOOL 5: Date & Time
# ══════════════════════════════════════════
def get_datetime(timezone: str = "Asia/Karachi") -> str:
    """
    Current date aur time batata hai kisi bhi timezone mein.
    """
    city_to_tz = {
        "pakistan": "Asia/Karachi",
        "karachi": "Asia/Karachi",
        "lahore": "Asia/Karachi",
        "london": "Europe/London",
        "new york": "America/New_York",
        "dubai": "Asia/Dubai",
        "tokyo": "Asia/Tokyo",
        "sydney": "Australia/Sydney",
        "paris": "Europe/Paris",
    }
    try:
        tz_name = city_to_tz.get(timezone.lower(), timezone)
        tz = pytz.timezone(tz_name)
        now = datetime.now(tz)
        return f"""
🕐 Timezone: {tz_name}
📅 Date: {now.strftime('%A, %d %B %Y')}
⏰ Time: {now.strftime('%I:%M %p')}
        """.strip()

    except Exception:
        tz = pytz.timezone("Asia/Karachi")
        now = datetime.now(tz)
        return f"Pakistan Time → {now.strftime('%A, %d %B %Y — %I:%M %p')}"