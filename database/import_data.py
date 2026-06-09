import json
from pymongo import MongoClient
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# MongoDB URI
uri = os.getenv("MONGO_URI")

# Connect to MongoDB
client = MongoClient(uri)

# Database
db = client["ecowatt"]

# Clear old appliance data
db.appliances.delete_many({})

# Load appliance data
with open("database/appliances.json") as file:
    appliance_data = json.load(file)

# Insert appliance data
db.appliances.insert_many(appliance_data)

print("Appliance data imported successfully!")

# Clear old business data
db.business_types.delete_many({})

# Load business types data
with open("database/business_types.json") as file:
    business_data = json.load(file)

# Insert business data
db.business_types.insert_many(business_data)

print("Business types imported successfully!")

# Clear old solar pricing data
db.solar_pricing.delete_many({})

# Load solar pricing data
with open("database/solar_pricing.json") as file:
    solar_data = json.load(file)

# Insert solar pricing data
db.solar_pricing.insert_many(solar_data)

print("Solar pricing imported successfully!")

# Clear old sustainability rules
db.sustainability_rules.delete_many({})

# Load sustainability rules
with open("database/sustainability_rules.json") as file:
    sustainability_data = json.load(file)

# Insert sustainability rules
db.sustainability_rules.insert_one(sustainability_data)

print("Sustainability rules imported successfully!")