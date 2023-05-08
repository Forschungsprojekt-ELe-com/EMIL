from api.db import db_XAPI
import asyncio

# get game performance model
async def get_statement():
    async for document in db_XAPI["statements"].find():
        print(document)
    #return await db_XAPI["statements"].find()
