from calculator import (
    calculate_units,
    calculate_bill,
    recommend_solar,
    calculate_carbon,
    sustainability_score
)

# Sample user input
appliances = [
    {
        "name": "Air Conditioner",
        "quantity": 2,
        "hours": 8
    },
    {
        "name": "Fan",
        "quantity": 4,
        "hours": 12
    },
    {
        "name": "LED Bulb",
        "quantity": 10,
        "hours": 10
    }
]

# Daily units
daily_units = calculate_units(appliances)

# Monthly units
monthly_units = daily_units * 30

# Bill calculation
bill = calculate_bill(monthly_units, 7)

# Solar recommendation
solar = recommend_solar(monthly_units)

# Carbon footprint
carbon = calculate_carbon(monthly_units)

# Sustainability score
score = sustainability_score(
    has_led=True,
    has_solar=True
)

print("Daily Units:", daily_units)

print("Monthly Units:", monthly_units)

print("Estimated Bill: ₹", bill)

print("Solar Recommendation:", solar)

print("Carbon Footprint:", carbon, "kg CO2")

print("Sustainability Score:", score)