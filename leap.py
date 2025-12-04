import requests
import json
from datetime import datetime

BASE_URL = "https://leap.deno.dev"

def check_current_year():
    """Checks if the current year is a leap year."""
    print("--- 1. Checking the Current Year (GET /) ---")
    try:
        current_year = datetime.now().year
        
        response = requests.get(BASE_URL)
        response.raise_for_status()
        
        data = response.json()
        result = data.get("result", "N/A")
        
        status = "is" if result else "is NOT"
        print(f"The current year ({current_year}) {status} a leap year.")
        print(f"API Response: {json.dumps(data)}")

    except requests.exceptions.RequestException as e:
        print(f"An error occurred while checking the current year: {e}")
    print("-" * 40 + "\n")


def check_specific_year(year):
    """Checks if a specific year is a leap year (GET /:year)."""
    print(f"--- 2. Checking Specific Year: {year} (GET /:year) ---")
    endpoint = f"{BASE_URL}/{year}"
    try:
        response = requests.get(endpoint)
        response.raise_for_status()
        
        data = response.json()
        result = data.get("result", "N/A")
        
        status = "is" if result else "is NOT"
        print(f"The year {year} {status} a leap year.")
        print(f"API Response: {json.dumps(data)}")

    except requests.exceptions.RequestException as e:
        print(f"An error occurred while checking year {year}: {e}")
    print("-" * 40 + "\n")


def check_year_range(start_year, end_year):
    """Gets a list of leap years within a given range (GET /range/:start/:end)."""
    print(f"--- 3. Checking Range: {start_year} to {end_year} (GET /range/:start/:end) ---")
    endpoint = f"{BASE_URL}/range/{start_year}/{end_year}"
    try:
        response = requests.get(endpoint)
        response.raise_for_status()
        
        data = response.json()
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
        
        print(f"API Response (Partial): {json.dumps(data)[:100]}...")

    except requests.exceptions.RequestException as e:
        print(f"An error occurred while checking the range: {e}")
    print("-" * 40 + "\n")


if __name__ == "__main__":
    check_current_year()

    check_specific_year(int(input("enter year> ")))

    check_specific_year(2023)
    
