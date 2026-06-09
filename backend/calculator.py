from pymongo import MongoClient
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# MongoDB connection
uri = os.getenv("MONGO_URI")

client = MongoClient(uri)

db = client["ecowatt"]


# Calculate electricity units
def calculate_units(appliances):

    total_units = 0

    for item in appliances:

        appliance_name = item["name"]
        quantity = item["quantity"]
        hours = item["hours"]

        # Fetch appliance data from MongoDB
        appliance_data = db.appliances.find_one(
            {"name": appliance_name}
        )

        if appliance_data:

            power = appliance_data["power"]

            units = (power * quantity * hours) / 1000

            total_units += units

    return round(total_units, 2)


# Calculate monthly bill
def calculate_bill(monthly_units, tariff):

    return round(monthly_units * tariff, 2)


# Calculate solar recommendation
def recommend_solar(monthly_units):

    solar_size = monthly_units / 120

    solar_size = round(solar_size)

    solar_data = db.solar_pricing.find_one(
        {"size_kw": solar_size}
    )

    if solar_data:

        return {
            "recommended_kw": solar_size,
            "estimated_cost": solar_data["price"]
        }

    return {
        "recommended_kw": solar_size,
        "estimated_cost": "Price not available"
    }


# Calculate carbon footprint
def calculate_carbon(monthly_units):

    return round(monthly_units * 0.82, 2)


# Sustainability score
def sustainability_score(has_led, has_solar):

    score = 50

    if has_led:
        score += 20

    if has_solar:
        score += 30

    return score