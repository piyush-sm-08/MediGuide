import os
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()
uri = os.getenv("MONGODB_URI")

if uri and "mongodb+srv" in uri:
    import certifi
    client = MongoClient(uri, tls=True, tlsCAFile=certifi.where())
else:
    client = MongoClient(uri)

client.admin.command("ping")
print("CONNECTED")
