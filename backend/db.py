from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

uri = os.getenv("MONGO_URI")

client = MongoClient(uri)

db = client["ecowatt"]
from db import db

appliance = db.appliances.find_one({"name": "Fan"})
print(appliance)