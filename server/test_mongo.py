import os
from dotenv import load_dotenv
from pymongo import MongoClient
import certifi

load_dotenv()
uri =os.getenv("MONGODB_URI")

client = MongoClient(uri, tls=True, tlsCAFile=certifi.where())
client.admin.command("ping")
print("CONNECTED")
