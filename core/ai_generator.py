import os
import json
import requests

def generate_itinerary(destination, days, pace, interests):
    """
    Calls the Groq API to generate a JSON itinerary.
    """
    api_key = os.environ.get('GROQ')
    if not api_key:
        raise ValueError("GROQ API key not found in environment variables.")

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    system_prompt = """You are an expert travel planner. You must respond ONLY with a valid JSON object. Do not include markdown formatting like ```json or any other text before or after the JSON.
Your task is to generate a realistic, mathematically sound itinerary for the requested destination, duration, pace, and interests.

The JSON schema must exactly match this structure:
{
  "trip_name": "A creative name for the trip",
  "description": "A short 2 sentence description",
  "cities": [
    {
      "name": "City Name",
      "days": 2, // Integer number of days to spend here
      "activities": [
        {
          "name": "Activity Name",
          "time_of_day": "morning", // "morning", "afternoon", or "evening"
          "description": "Short description of what you do",
          "cost_estimate_usd": 25.50, // Float cost estimate in USD
          "category": "Activities" // Must be one of: "Transport", "Accommodation", "Activities", "Meals", "Other"
        }
      ]
    }
  ]
}
Important: Make sure the total sum of `days` across all cities exactly equals the requested duration. Generate at least 2-3 activities per day.
"""

    user_prompt = f"Destination: {destination}\nDuration: {days} days\nPace: {pace}\nInterests: {interests}"

    payload = {
        "model": "llama3-70b-8192",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        "temperature": 0.7
    }

    response = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=payload)
    
    if response.status_code == 200:
        data = response.json()
        content = data['choices'][0]['message']['content'].strip()
        
        # Strip potential markdown formatting if the model disobeys
        if content.startswith("```json"):
            content = content[7:]
        if content.endswith("```"):
            content = content[:-3]
            
        try:
            return json.loads(content)
        except json.JSONDecodeError as e:
            print("Failed to decode JSON:", content)
            raise e
    else:
        raise Exception(f"Groq API Error: {response.text}")
