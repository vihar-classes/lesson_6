import requests
import json
import time
from datetime import datetime

# --- Gemini API Configuration ---
GEMINI_API_KEY = "AIzaSyCFrOVyOzRrSSE29Smq0p-zpJI7ZN9GzIo"
MODEL_NAME = "gemini-2.5-flash-preview-09-2025"
GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL_NAME}:generateContent?key={GEMINI_API_KEY}"
# --------------------------------

def _call_gemini_api(prompt, schema, max_retries=3):
    """
    Handles POST requests to the Gemini API with structured JSON output and exponential backoff.
    """
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "responseMimeType": "application/json",
            "responseSchema": schema
        }
    }

    headers = {'Content-Type': 'application/json'}

    for attempt in range(max_retries):
        try:
            response = requests.post(GEMINI_URL, headers=headers, data=json.dumps(payload))
            response.raise_for_status()

            result = response.json()
            
            # Extract and parse the JSON string from the model's response
            json_str = result.get('candidates', [{}])[0].get('content', {}).get('parts', [{}])[0].get('text')
            if json_str:
                return json.loads(json_str)

            raise ValueError("API response was successful but did not contain valid JSON text.")

        except requests.exceptions.RequestException as e:
            if attempt < max_retries - 1:
                delay = 2 ** attempt
                # print(f"API request failed (Attempt {attempt+1}/{max_retries}). Retrying in {delay}s...")
                time.sleep(delay)
            else:
                # print(f"API request failed after {max_retries} attempts.")
                raise e
        except (json.JSONDecodeError, ValueError) as e:
            # print(f"Error parsing Gemini response: {e}")
            if attempt < max_retries - 1:
                delay = 2 ** attempt
                time.sleep(delay)
            else:
                raise e
    return None


def check_current_year():
    """Checks if the current year is a leap year using the Gemini API."""
    print("--- 1. Checking the Current Year (AI Model) ---")
    current_year = datetime.now().year
    
    prompt = f"Is the year {current_year} a leap year? Return the answer as a JSON object."
    
    # Define the required JSON schema for a boolean result
    schema = {
        "type": "OBJECT",
        "properties": {"result": {"type": "BOOLEAN"}},
        "propertyOrdering": ["result"]
    }
    
    try:
        data = _call_gemini_api(prompt, schema)
        if data and "result" in data:
            result = data["result"]
            status = "is" if result else "is NOT"
            print(f"The current year ({current_year}) {status} a leap year.")
            print(f"AI Response: {json.dumps(data)}")
        else:
            print("AI Model returned an unparseable result.")

    except Exception as e:
        print(f"An error occurred while checking the current year: {e}")
    print("-" * 40 + "\n")


def check_specific_year(year):
    """Checks if a specific year is a leap year using the Gemini API."""
    print(f"--- 2. Checking Specific Year: {year} (AI Model) ---")
    endpoint = f"/{year}"
    
    prompt = f"Is the year {year} a leap year? Return the answer as a JSON object."
    
    # Define the required JSON schema for a boolean result
    schema = {
        "type": "OBJECT",
        "properties": {"result": {"type": "BOOLEAN"}},
        "propertyOrdering": ["result"]
    }
    
    try:
        data = _call_gemini_api(prompt, schema)
        if data and "result" in data:
            result = data["result"]
            status = "is" if result else "is NOT"
            print(f"The year {year} {status} a leap year.")
            print(f"AI Response: {json.dumps(data)}")
        else:
            print("AI Model returned an unparseable result.")

    except Exception as e:
        print(f"An error occurred while checking year {year}: {e}")
    print("-" * 40 + "\n")


def check_year_range(start_year, end_year):
    """Gets a list of leap years within a given range using the Gemini API."""
    print(f"--- 3. Checking Range: {start_year} to {end_year} (AI Model) ---")
    
    prompt = f"List all leap years between {start_year} and {end_year} inclusive. Return only the list of years in the 'result' field of a JSON object."
    
    # Define the required JSON schema for an array of integers
    schema = {
        "type": "OBJECT",
        "properties": {
            "result": {
                "type": "ARRAY",
                "items": {"type": "INTEGER"}
            }
        },
        "propertyOrdering": ["result"]
    }
    
    try:
        data = _call_gemini_api(prompt, schema)
        leap_years = data.get("result", [])
        
        count = len(leap_years)
        print(f"Found {count} leap years between {start_year} and {end_year}.")
        
        if leap_years:
            print("Leap Years:")
            for i, year in enumerate(leap_years):
                print(f"{year:<6}", end=" " if (i + 1) % 10 != 0 else "\n")
            print("\n")
        else:
            print("No leap years found in this range.")
        
        print(f"AI Response (Partial): {json.dumps(data)[:100]}...")

    except Exception as e:
        print(f"An error occurred while checking the range: {e}")
    print("-" * 40 + "\n")


if __name__ == "__main__":
    check_current_year()

    check_specific_year(int(input("year? ")))
