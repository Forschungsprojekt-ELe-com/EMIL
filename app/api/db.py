import motor.motor_asyncio
import os

# environment variables
USER = os.getenv('MONGODB_USER')
PASSWORD = os.getenv('MONGODB_PASS')

# mongodb database URI
DATABASE_URI = "mongodb://{user}:{password}@mongodb:27017".format(user=USER, password=PASSWORD)


client = motor.motor_asyncio.AsyncIOMotorClient(DATABASE_URI)

# database collections
db_XAPI = client.XAPI
