from db import db_learningLocker


# get XAPI statement
async def get_statement():
    collection = db_learningLocker["statements"]

    query = {"objectType": "Activity"}
    projection = {"_id": 0, "verb": 1}
    results = collection.find(query, projection)

    return await results
