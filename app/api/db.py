import motor.motor_asyncio
import os

# environment variables
USER = os.getenv('MONGODB_USER')
PASSWORD = os.getenv('MONGODB_PASS')

# mongodb database URI
DATABASE_URI = "mongodb://127.0.0.1:27017"

client = motor.motor_asyncio.AsyncIOMotorClient(DATABASE_URI)

# database collections
db_XAPI = client["learninglocker_v2"]
