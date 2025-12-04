import math
import requests

# --- CORE LOGIC FUNCTIONS ---

def is_prime(n):
  """
  Checks if a number n is a prime number.
  
  A prime number is a natural number greater than 1 that is not a product 
  of two smaller natural numbers.
  
  Args:
    n (int): The number to check.
  
  Returns:
    bool: True if n is prime, False otherwise.
  """
  if n <= 1:
    return False
  # We only need to check divisibility up to the square root of n
  for i in range(2, int(math.sqrt(n)) + 1):
    if n % i == 0:
      return False
  return True

def calculate_delivery_charge(customer_id, cart_value, location):
  """
  Calculates the total delivery charge based on customer status, cart value,
  and delivery location.

  Rules:
  1. Customer is a prime number ID: Free (0)
  2. Cart value > 2000: Free (0)
  3. Cart value 500 - 1000: Base fee of 40
  4. Cart value < 500: Base fee of 60
  5. Location is remote (not India): +50 extra on top of base fee
  
  Args:
    customer_id (int): ID used for prime check.
    cart_value (float): Total value of items.
    location (str): Detected country name (or 'India' on error).
    
  Returns:
    float: The final calculated delivery charge.
  """
  
  base_charge = 0
  
  # --- Step 1: Determine the Base Charge based on Cart Value ---
  if cart_value > 2000:
    # Rule 2: Cart value greater than 2000 is free
    base_charge = 0
  elif cart_value >= 500 and cart_value <= 1000:
    # Rule 3: Cart value between 500 and 1000 is 40
    base_charge = 40
  elif cart_value < 500:
    # Rule 4: Cart value less than 500 is 60
    base_charge = 60
  else:
    # Handles cart values > 1000 and <= 2000 (default tier, 20 rupees)
    base_charge = 20
  
  # --- Step 2: Apply Prime Number Discount (Rule 1) ---
  # Note: The prime discount overrides cart value rules if applicable
  if is_prime(customer_id):
    print(f"\n✅ Customer ID {customer_id} is a prime number! Delivery is FREE.")
    base_charge = 0
  
  # --- Step 3: Apply Remote/Outside India Surcharge (Rule 5) ---
  surcharge = 0
  
  # The surcharge is applied if the detected location is not 'india'.
  # We use .lower() for case-insensitive comparison.
  if location.strip().lower() != 'india':
    surcharge = 50
    # Note: 'location' here is the detected country name
    print(f"⚠️ Detected location '{location}' is outside India. A surcharge of +{surcharge} will be added.")
  
  # --- Step 4: Calculate Final Total ---
  final_charge = base_charge + surcharge
  return final_charge


def get_location_status():
  """
  Uses an external IP-based geolocation API (ip-api.com) to detect the user's 
  current country automatically.
  
  Returns:
    str: The detected country name. Defaults to 'India' on API failure 
         to prevent unintended surcharges.
  """
  try:
    # Use a free, simple IP geolocation API to get the country.
    # The API call automatically uses the client's public IP address.
    api_url = 'http://ip-api.com/json/'
    response = requests.get(api_url, timeout=5)
    response.raise_for_status() # Raise exception for bad status codes (4xx or 5xx)
    data = response.json()
    
    # Extract the country name. The API returns the field 'country'
    country = data.get('country') 
    
    if country:
        return country
    else:
        return "Unknown"
             
  except requests.exceptions.RequestException as e:
    # Handle network errors, timeouts, or API unavailability
    print(f"🚨 Warning: Could not fetch location data ({e}). Defaulting location status to 'India'.")
    return "India" # Default to 'India' to avoid unexpected surcharge on failure


# --- MAIN EXECUTION BLOCK ---

if __name__ == "__main__":
  # Add a note about the requests dependency
  print("# NOTE: This script requires the 'requests' library (pip install requests)")
  print("----------------------------------------------------------------------")
  
  print("🛒 E-Commerce Delivery Calculator Service 🚚")
  print("-" * 45)
  
  # Get required inputs from the user
  try:
    # 1. Customer ID (for prime check)
    customer_id = int(input("Enter Customer ID (integer): "))
    if customer_id < 0:
      raise ValueError("Customer ID must be a non-negative integer.")

    # 2. Cart Value
    cart_value = float(input("Enter Cart Value (e.g., 850.50): "))
    if cart_value < 0:
      raise ValueError("Cart value must be a non-negative number.")
      
    # 3. Location (AUTOMATED DETECTION)
    location = get_location_status()
    print(f"🌍 Detected Location: {location}")
    
    # Calculate the final charge
    total_delivery_charge = calculate_delivery_charge(customer_id, cart_value, location)
    
    print("-" * 45)
    print("✨ FINAL DELIVERY CALCULATION ✨")
    print(f"Customer ID: {customer_id}")
    print(f"Cart Value:  {cart_value:.2f}")
    print(f"Location:    {location}")
    print(f"---------------------------------------------")
    
    if total_delivery_charge == 0:
      print("TOTAL DELIVERY CHARGE: FREE!")
    else:
      print(f"TOTAL DELIVERY CHARGE: {total_delivery_charge:.2f} rupees")
      
    print("-" * 45)

  except ValueError as e:
    print(f"\n🚨 Error in input: {e}. Please run again and enter valid numbers.")
