from fastapi import Depends, APIRouter
import time
import datetime

from ai_model import ai_prediction_model
from api import db_manager, data_filtering
from model.EMIL import EMIL
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from typing_extensions import Annotated

# add to APIRouter
ai_service = APIRouter()

# Add HTTP Basic Auth
security = HTTPBasic()


# Recommendation endpoint
@ai_service.get("/{user_id}/{count_recommendation}")
# async def get_recommendation(user_id: int, count_recommendation: int, credentials: Annotated[HTTPBasicCredentials, Depends(security)]):
async def get_recommendation(user_id: int, count_recommendation: int):
    # check username and password
    # if not credentials.username == xxx or not credentials.password == xxx:
    #     return

    # Create Emil object
    emil = EMIL()
    recommendation = []

    # Get done_MLE object ids from database using user_id
    done_MLE = await db_manager.get_done_MLE(user_id)
    # Check if user exist in LRS
    user_exist = await db_manager.check_user(user_id)
    user_preference = await get_preference(user_id)

    # get recommendations
    df = ai_prediction_model.recommendation(done_MLE, user_preference)
    obj_id_column = [col for col in df.columns if col.startswith('obj_id')]
    recommendation = df[obj_id_column[0]].dropna().tolist()

    # If there are obj_ids in done_MLE list, get recommendation using AI model
    if done_MLE:
        emil.data.recommendation_reason = "Abgestimmt auf Ihre bisherige Auswahl schlage ich vor:"

    # If there is no obj_ids, check if the user_id exist in the LRS.
    elif user_exist:
        emil.data.recommendation_reason = "Aufgrund Ihrer aktuellen Einstellungen schlage ich Ihnen folgendes vor:"

    # If user doesn't exist, set error message
    elif not user_exist:
        emil.meta.error = "user_id not found or no user data"

    # Set the number of recommendations in response body.
    filtered_recommendation = recommendation[:count_recommendation]
    emil.data.MLE_ref_id = filtered_recommendation

    # convert timestamp format
    timestamp = time.time()
    dt = datetime.datetime.fromtimestamp(timestamp)
    formatted_datetime = dt.strftime("%Y-%m-%dT%H:%M:%S.%f%z")
    emil.meta.transmitted_at = formatted_datetime

    return emil


async def get_preference(user_id):
    user_preference = await db_manager.get_preference(user_id, 2078)

    # enable this snippet when have the obj_id of second video.
    # use the id of the second video above, and the id of the first video below.

    # if len(user_preference) < 3:
    #     user_preference = await db_manager.get_preference(user_id, 1813)

    return user_preference
