from api.db import db_XAPI
from urllib.parse import urlparse, parse_qs
import re


TEST_OBJ_ID = "https://elecom.qualitus.net/goto.php?target=copa_1649&client_id=elecom&h5p_object_id=246&h5p-subContentId=118704d2-f551-4e1e-9f27-752e526dd12d&obj_id_lrs=1813"

# get XAPI statement using query
async def get_done_MLE(user_id):
    condition_de_complete = {"statement.verb.display.de-DE": "completed"}
    condition_en_complete = {"statement.verb.display.en-US": "completed"}
    condition_user_id = {"statement.actor.account.name": re.compile(f"^{user_id}@")}
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
    result = db_XAPI["statements"].find(query, filter_keys)
    async for document in result:
        obj_id = extract_obj_id(document["statement"]["object"]["id"])
        done_MLE.append(int(obj_id[0]))
    return done_MLE


# Method to check if user has interaction with any MLE
async def check_user(user_id):
    # Condition
    condition_user_id = {"statement.actor.account.name": re.compile(f"^{user_id}@")}
    # Filter result
    filter_keys = {"_id": 0, "statement.object.id": 1}

    attempted_MLE = []
    result = db_XAPI["statements"].find(condition_user_id, filter_keys)
    async for document in result:
        obj_id = extract_obj_id(document["statement"]["object"]["id"])
        attempted_MLE.append(int(obj_id[0]))
    return attempted_MLE


async def get_preference(user_id, test_obj_id):
    DESCRIPTION = ["Lernformat", "Vorwissen"]

    combined_preference = []

    submit_time = await get_submit_time(user_id, test_obj_id)

    for desc in DESCRIPTION:
        # Conditions
        condition_user_id = {"statement.actor.account.name": re.compile(f"^{user_id}@")}
        condition_en_answered = {"statement.verb.display.en-US": "interacted"}
        condition_de_answered = {"statement.verb.display.de-DE": "interacted"}
        condition_test_obj = {"statement.object.id": re.compile(f"{test_obj_id}$")}
        condition_question_description = {"statement.object.definition.name.de-DE": re.compile(f".*{desc}.*")}
        condition_submit_time = {"timestamp": {"$lt": submit_time}}

        query = {
            '$and': [
                {
                    '$or': [condition_en_answered, condition_de_answered]
                },
                condition_user_id,  condition_test_obj, condition_question_description, condition_submit_time
            ]
        }

        # Filter result
        filter_keys = {"_id": 0, "statement.result.response": 1}

        preference = []

        result = db_XAPI["statements"].find(query, filter_keys)
        async for document in result:
            obj_id = document["statement"]["result"]["response"]
            preference.append(int(obj_id[0]))
        if preference:
            combined_preference.append(preference[-1])
    return combined_preference


# Get the latest submit time
async def get_submit_time(user_id, test_obj_id):
    # Condition
    condition_user_id = {"statement.actor.account.name": re.compile(f"^{user_id}@")}
    condition_en_answered = {"statement.verb.display.en-US": "answered"}
    condition_de_answered = {"statement.verb.display.de-DE": "answered"}
    condition_test_obj = {"statement.object.id": re.compile(f"{test_obj_id}$")}

    query = {
        '$and': [
            {
                '$or': [condition_en_answered, condition_de_answered]
            },
            condition_user_id, condition_test_obj
        ]
    }

    # Filter result
    filter_keys = {"_id": 0, "timestamp": 1}

    submit_time = []

    result = db_XAPI["statements"].find(query, filter_keys)
    async for document in result:
        datetime = document["timestamp"]
        submit_time.append(datetime)
    return submit_time[-1]


def extract_obj_id(url):
    parsed_url = urlparse(url)
    query_params = parse_qs(parsed_url.query)
    obj_id = query_params.get('obj_id_lrs')
    return obj_id
