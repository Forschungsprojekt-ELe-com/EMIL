from fastapi import APIRouter
import time
import datetime

from ai_model import ai_prediction_model
from api import db_manager
from model.LENA import LENA
from model.EMIL import EMIL


# add to APIRouter
ai_service = APIRouter()


# get all game performance model data
@ai_service.post("/")
async def get_recommendation(lena: LENA):
    if lena.user_id:
        user_id = int(lena.user_id)
    ref_id = lena.ref_id_course
    done_MLE = await db_manager.get_done_MLE(user_id)
    df = ai_prediction_model.recommendation(ref_id, done_MLE)
    recommendation = df["ref_id1"].tolist()
    print(recommendation)

    emil = EMIL()
    emil.MLE_ref_id = recommendation
    emil.recommendation_reason = "1"

    # concert timestamp format
    timestamp = time.time()
    dt = datetime.datetime.fromtimestamp(timestamp)
    formatted_datetime = dt.strftime("%Y-%m-%dT%H:%M:%S.%f%z")
    emil.transmitted_at = formatted_datetime

    return emil


@ai_service.get("/predict/")
async def predict():
    return
