import os

import motor.motor_asyncio
from dotenv import load_dotenv

load_dotenv()

client = motor.motor_asyncio.AsyncIOMotorClient(os.environ["MONGODB_URL"])
db = client.get_database(os.environ["DB_NAME"])

forms_collection = db.get_collection("forms")
form_fields_collection = db.get_collection("form_fields")
