import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from server/.env
env_path = Path(__file__).parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

MONGO_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
DB_NAME = os.getenv("MONGODB_DB_NAME", "mediguide")

# Mock database for development (when MongoDB is not available)
class MockCollection:
    def __init__(self, name):
        self.name = name
        self.data = []

    def find_one(self, query):
        for item in self.data:
            if all(item.get(k) == v for k, v in query.items()):
                return item
        return None

    def insert_one(self, document):
        # Simple mock - just append with auto-generated ID
        doc = dict(document)
        if "_id" not in doc:
            doc["_id"] = len(self.data) + 1
        self.data.append(doc)
        return {"inserted_id": doc["_id"]}

    def find(self, query=None):
        if query is None:
            return self.data
        return [item for item in self.data if all(item.get(k) == v for k, v in query.items())]

# Try to connect to MongoDB, fallback to mock
try:
    import certifi
    from pymongo import MongoClient
    from pymongo.errors import ConnectionFailure

    if "mongodb+srv" in MONGO_URI:
        # Atlas connection
        client = MongoClient(
            MONGO_URI,
            tls=True,
            tlsCAFile=certifi.where(),
            serverSelectionTimeoutMS=30000,
            connectTimeoutMS=10000,
            socketTimeoutMS=20000,
        )
    else:
        # Local connection
        client = MongoClient(
            MONGO_URI,
            serverSelectionTimeoutMS=30000,
            connectTimeoutMS=10000,
            socketTimeoutMS=20000,
        )

    # Test connection
    client.admin.command("ping")
    print("MongoDB connected successfully.")

    # Select database
    db = client[DB_NAME]

    # Collections
    users_collection = db["users"]
    appointments_collection = db["appointments"]
    doctors_collection = db["doctors"]
    reports_collection = db["reports"]

except (ImportError, ConnectionFailure) as e:
    print("MongoDB not available:", e)
    print("Using mock database for development...")

    # Mock database
    users_collection = MockCollection("users")
    appointments_collection = MockCollection("appointments")
    doctors_collection = MockCollection("doctors")
    reports_collection = MockCollection("reports")

    print("Mock database initialized")


