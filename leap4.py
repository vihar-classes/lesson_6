def is_leap_year(year):
  return (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)

input_year = int(input("Enter a year: "))
if is_leap_year(input_year):
  print(f"{input_year} is a leap year.")
else:
  print(f"{input_year} is not a leap year.")
