from api.db import db_XAPI
from urllib.parse import urlparse, parse_qs


# get XAPI statement
async def get_done_MLE(user_id):
    condition_complete = {"statement.verb.display.en-US": "completed"}
    condition_user_id = {"statement.actor.account.name": user_id}
    query = {'$and': [condition_complete, condition_user_id]}
    filter_keys = {"_id": 0, "statement.object.id": 1}

    done_MLE = []

    async for document in db_XAPI["statements"].find(query, filter_keys):
        ref_id = extract_ref_id(document["statement"]["object"]["id"])
        done_MLE.append(ref_id)
    return done_MLE


def extract_ref_id(url):
    parsed_url = urlparse(url)
    query_params = parse_qs(parsed_url.query)
    copa = query_params.get('target', [None])[0]
    if copa is not None and copa.startswith('copa_'):
        ref_id = copa.split('_')[1]
    return ref_id
