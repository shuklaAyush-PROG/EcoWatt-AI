import json
from pymongo import MongoClient
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Get MongoDB URI
uri = os.getenv("MONGO_URI")

# Connect to MongoDB
client = MongoClient(uri)

# Create/access database
db = client["ecowatt"]

# Open JSON file
with open("database/appliances.json") as file:
    data = json.load(file)

# Insert data into MongoDB
db.appliances.insert_many(data)

print("Appliance data imported successfully!")