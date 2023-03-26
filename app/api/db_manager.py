from app.api.db import db_XAPI


# get game performance model
async def get_statement():
    return await db_XAPI["XAPI"].find().distinct("statement")