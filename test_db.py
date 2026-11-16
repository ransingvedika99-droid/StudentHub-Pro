import os
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv(".env", override=True)

try:
    client = MongoClient(
        f"mongodb+srv://{os.getenv('MONGO_HOST')}/",
        username=os.getenv("MONGO_USER"),
        password=os.getenv("MONGO_PASSWORD"),
        authSource="admin",
        serverSelectionTimeoutMS=10000
    )

    client.admin.command("ping")
    print("SUCCESS! Connected to MongoDB Atlas.")

except Exception as e:
    print("Connection failed.")
    print("Error:", e)