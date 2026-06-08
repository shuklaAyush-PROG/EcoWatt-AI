from pymongo import MongoClient
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Get MongoDB URI
uri = os.getenv("MONGO_URI")

# Connect to MongoDB
client = MongoClient(uri)

# Create database
db = client["ecowatt"]

print("MongoDB Connected Successfully")