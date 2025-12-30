import os
import certifi
from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

# Load environment variables
load_dotenv()

MONGO_URI = os.getenv("MONGODB_URI")
DB_NAME = os.getenv("MONGODB_DB_NAME")

if not MONGO_URI or not DB_NAME:
    raise ValueError("❌ MongoDB environment variables not set")

try:
    client = MongoClient(
        MONGO_URI,
        tls=True,
        tlsCAFile=certifi.where(),
        serverSelectionTimeoutMS=30000
    )

    # Test connection
    client.admin.command("ping")
    print("✅ MongoDB connected successfully")

except ConnectionFailure as e:
    print("❌ MongoDB connection failed")
    raise e

# Select database
db = client[DB_NAME]

# Collections
users_collection = db["users"]
appointments_collection = db["appointments"]
doctors_collection = db["doctors"]
