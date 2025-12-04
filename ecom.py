# customer prime num = free
# cart value greater than 2000 + free
# cart value is bewteen 500 - 1000 devlivery is 40
# cart is less than 500, delviery 60
# location is remote than india = delviry + 50 rupees extra

import math

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
  5. Location is 'remote' or 'outside India': +50 extra on top of base fee
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
    # Handles cart values > 1000 and <= 2000. Assuming standard flat rate here.
    # Since only 500-1000 and < 500 were specified, let's treat the remaining
    # range (1001-2000) as the next tier, let's say 20 rupees, or perhaps free
    # if it's considered premium. Based on the tiers, let's set it to 20.
    base_charge = 20
  
  # --- Step 2: Apply Prime Number Discount (Rule 1) ---
  if is_prime(customer_id):
    print(f"\n✅ Customer ID {customer_id} is a prime number! Delivery is FREE.")
    base_charge = 0
  
  # --- Step 3: Apply Remote/Outside India Surcharge (Rule 5) ---
  surcharge = 0
  
  # Normalize location input for case-insensitive check
  location_lower = location.strip().lower()

  if location_lower in ['remote', 'outside india']:
    surcharge = 50
    print(f"⚠️ Location '{location}' is remote/outside India. A surcharge of +{surcharge} will be added.")
  
  # --- Step 4: Calculate Final Total ---
  final_charge = base_charge + surcharge
  return final_charge


# --- MAIN EXECUTION BLOCK ---

if __name__ == "__main__":
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
      
    # 3. Location (for surcharge check)
    location = input("Enter Location (e.g., India, Remote, Outside India): ")
    
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
