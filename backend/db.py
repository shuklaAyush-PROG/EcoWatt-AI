from pymongo import MongoClient
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# MongoDB URI
uri = os.getenv("MONGO_URI")

# Connect to MongoDB
client = MongoClient(uri)

# Access database
db = client["ecowatt"]

print("MongoDB Connected Successfully")

# Fetch one appliance
appliance = db.appliances.find_one({"name": "Fan"})

print(appliance)

all_appliances = db.appliances.find()

for item in all_appliances:
    print(item["name"], "-", item["power"], "W")

solar = db.solar_pricing.find_one({"size_kw": 5})

print(solar)