from api.db import db_XAPI
from urllib.parse import urlparse, parse_qs
import re


# get XAPI statement
async def get_done_MLE(user_id):
    condition_de_complete = {"statement.verb.display.de-DE": "completed"}
    condition_en_complete = {"statement.verb.display.en-US": "completed"}
    condition_user_id = {"statement.actor.account.name": re.compile(f"^{user_id}")}
    query = {
        '$and': [
            {
                '$or': [condition_de_complete, condition_en_complete]
            },
            condition_user_id
        ]
    }
    filter_keys = {"_id": 0, "statement.object.id": 1}

    done_MLE = []
    result = db_XAPI["statements"].find(query, filter_keys).sort([['_id', -1]])
    async for document in result:
        obj_id = extract_obj_id(document["statement"]["object"]["id"])
        done_MLE.append(int(obj_id[0]))
    done_MLE.reverse()
    return done_MLE


def extract_obj_id(url):
    parsed_url = urlparse(url)
    query_params = parse_qs(parsed_url.query)
    obj_id = query_params.get('obj_id_lrs')
    return obj_id
