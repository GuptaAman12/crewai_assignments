# Assignment 2: Multi-Tool Travel Assistant
# Demonstrates how an LlmAgent can orchestrate multiple tools for travel planning.

import os
import requests
import random
from dotenv import load_dotenv
from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm

load_dotenv()
if not os.getenv("GROQ_API_KEY"):
    raise ValueError("GROQ_API_KEY environment variable is not set.")

groq_model = LiteLlm(model="groq/gemma2-9b-it")

def weather_tool(city: str, day: str = "today") -> dict:
    """
    Fetch weather data for a given city using WeatherAPI.com.
    Supports 'today' and 'tomorrow'.
    """
    try:
        api_key = os.getenv("WEATHER_API_KEY")
        if not api_key:
            return {"status": "error", "error_message": "Missing WEATHER_API_KEY."}

        # Decide endpoint based on day
        if day.lower() == "tomorrow":
            url = f"http://api.weatherapi.com/v1/forecast.json?key={api_key}&q={city}&days=2&aqi=no&alerts=no"
        else:
            url = f"http://api.weatherapi.com/v1/current.json?key={api_key}&q={city}&aqi=no"

        resp = requests.get(url)
        if resp.status_code != 200:
            return {"status": "error", "error_message": f"Weather data not available for {city}."}

        data = resp.json()

        if day.lower() == "tomorrow":
            forecast = data["forecast"]["forecastday"][1]["day"]
            condition = forecast["condition"]["text"]
            avg_temp_c = forecast["avgtemp_c"]
            avg_temp_f = forecast["avgtemp_f"]
            return {
                "status": "success",
                "report": (
                    f"Tomorrow's weather in {city}: {condition}, "
                    f"avg {avg_temp_c}°C ({avg_temp_f}°F)."
                ),
            }
        else:
            current = data["current"]
            condition = current["condition"]["text"]
            temp_c = current["temp_c"]
            temp_f = current["temp_f"]
            return {
                "status": "success",
                "report": (
                    f"The current weather in {city} is {condition}, "
                    f"{temp_c}°C ({temp_f}°F)."
                ),
            }

    except Exception as e:
        return {"status": "error", "error_message": str(e)}

def flight_tool(source: str, destination: str) -> dict:
    """
    Return mock flight information between two cities.
    """
    airlines = ["IndiGo", "Air India", "Vistara", "SpiceJet"]
    flight_number = f"{random.choice(['AI', '6E', 'UK', 'SG'])}{random.randint(100, 999)}"
    price = random.randint(3000, 12000)  # INR
    duration = f"{random.randint(1, 3)}h {random.randint(0, 59)}m"

    return {
        "status": "success",
        "report": (
            f"Found a flight from {source} to {destination}: "
            f"{random.choice(airlines)} {flight_number}, "
            f"Duration: {duration}, Price: ₹{price}."
        ),
    }

root_agent = LlmAgent(
    name="travel_assistant_agent",
    model=groq_model,
    description="An agent that helps with travel planning using weather and flight tools.",
    instruction=(
        "You are a helpful travel assistant. Your primary goal is to answer travel-related queries using the available tools.\n"
        "1. **Analyze the user's entire request** to identify all distinct tasks (e.g., finding flights, checking weather).\n"
        "2. **Use tools for every task identified.** If the user asks about both flights and weather, you MUST call both `flight_tool` and `weather_tool` before responding.\n"
        "3. **Do not make assumptions or claim you lack information** if a tool is available for it. Use the tools provided.\n"
        "4. After gathering all necessary information from the tool(s), provide a comprehensive summary to the user."
    ),
    tools=[weather_tool, flight_tool],
)
