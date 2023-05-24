from api.db import db_XAPI
import asyncio


# get XAPI statement
async def get_done_MLE(user_id):
    condition_complete = {"statement.verb.display.en-US": "completed"}
    condition_user_id = {"statement.actor.account.name": user_id}
    query = {'$and': [condition_complete, condition_user_id]}
    filter_keys = {"_id": 0, "statement.object.id": 1}

    done_MLE = []

    async for document in db_XAPI["statements"].find(query, filter_keys):
        print(document)
        done_MLE.append(document["statement"]["object"]["id"])

    return done_MLE