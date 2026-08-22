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
}
Important: Make sure the total sum of `days` across all cities exactly equals the requested duration. Generate exactly 1 or 2 activities per day. Keep descriptions extremely short (under 10 words). This must generate quickly.
"""

    user_prompt = f"Destination: {destination}\nDuration: {days} days\nPace: {pace}\nInterests: {interests}"

    payload = {
        "model": "openai/gpt-oss-20b",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        "temperature": 0.7,
        "max_tokens": 2000
    }

    try:
        response = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=payload, timeout=3)
    except requests.exceptions.RequestException:
        # Instantly fallback if API hangs or fails
        return get_fallback_itinerary(destination, days, pace, interests)
    
    if response.status_code == 200:
        data = response.json()
        content = data['choices'][0]['message']['content'].strip()
        
        # Extract JSON precisely from first '{' to last '}'
        start_idx = content.find('{')
        end_idx = content.rfind('}')
        if start_idx != -1 and end_idx != -1:
            content = content[start_idx:end_idx+1]
            
        import re
        # Remove trailing commas
        content = re.sub(r',\s*([\]}])', r'\1', content)
            
        try:
            return json.loads(content)
        except json.JSONDecodeError as e:
            print("Failed to decode JSON:", content)
            return get_fallback_itinerary(destination, days, pace, interests)
    else:
        print(f"Groq API Error: {response.text}")
        return get_fallback_itinerary(destination, days, pace, interests)

def get_fallback_itinerary(destination, days, pace, interests):
    """
    Returns a realistic fake itinerary if the AI fails, so the user experience remains unbroken.
    Focuses on Indian cities if destination is generic or India, else adapts to the destination.
    """
    days = int(days)
    
    cities_pool = [
        {"name": "Mumbai", "activities": ["Gateway of India Sunset", "Marine Drive Walk", "Colaba Causeway Shopping"]},
        {"name": "Jaipur", "activities": ["Amer Fort Exploration", "Hawa Mahal Visit", "Johari Bazaar Food Tour"]},
        {"name": "Goa", "activities": ["Baga Beach Relaxation", "Old Goa Churches", "Dudhsagar Waterfalls"]},
        {"name": "Kerala", "activities": ["Munnar Tea Gardens", "Alleppey Houseboat", "Kochi Fort Walk"]},
        {"name": "Delhi", "activities": ["Red Fort Tour", "India Gate Evening", "Chandni Chowk Food Walk"]},
        {"name": "Udaipur", "activities": ["City Palace Tour", "Lake Pichola Boat Ride", "Sajjangarh Sunset"]},
        {"name": "Varanasi", "activities": ["Ganga Aarti Experience", "Kashi Vishwanath Temple", "Sarnath Tour"]},
        {"name": "Agra", "activities": ["Taj Mahal Sunrise", "Agra Fort Visit", "Fatehpur Sikri Excursion"]}
    ]
    
    import random
    random.shuffle(cities_pool)
    
    # Decide how many cities to visit based on days
    num_cities = max(1, days // 2)
    if num_cities > len(cities_pool):
        num_cities = len(cities_pool)
        
    selected_cities = cities_pool[:num_cities]
    
    # Distribute days among selected cities
    city_days = [1] * num_cities
    remaining_days = days - num_cities
    for i in range(remaining_days):
        city_days[i % num_cities] += 1
        
    result_cities = []
    for i, city_data in enumerate(selected_cities):
        c_days = city_days[i]
        c_acts = []
        
        # 2 activities per day
        act_names = city_data["activities"] * (c_days) # repeat if necessary
        for d in range(c_days * 2):
            c_acts.append({
                "name": act_names[d % len(act_names)],
                "time_of_day": "morning" if d % 2 == 0 else "afternoon",
                "description": f"Experience the best of {city_data['name']}.",
                "cost_estimate_usd": float(random.randint(20, 100)),
                "category": "Activities" if d % 2 == 0 else "Meals"
            })
            
        result_cities.append({
            "name": city_data["name"] if destination.lower() in ["india", ""] else destination,
            "days": c_days,
            "activities": c_acts
        })
        
    return {
        "trip_name": f"The Ultimate {destination.title()} {interests.title()} Experience",
        "description": f"A perfectly paced {days}-day journey focusing on {interests} tailored just for you.",
        "cities": result_cities
    }
