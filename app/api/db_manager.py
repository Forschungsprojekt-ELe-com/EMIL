from api.db import db_XAPI
import asyncio

# get XAPI statement
async def get_statements():
    async for document in db_XAPI["statements"].find():
        print(document)
        break
