from fastapi import APIRouter
import time
import datetime

from ai_model import ai_prediction_model
from api import db_manager
from model.LENA import LENA
from model.EMIL import EMIL


# add to APIRouter
ai_service = APIRouter()


# Recommendation endpoint
@ai_service.get("/{user_id}/{count_recommendation}")
async def get_recommendation(user_id: int, count_recommendation: int):

    done_MLE = await db_manager.get_done_MLE(user_id)
    df = ai_prediction_model.recommendation([], done_MLE)
    recommendation = df["ref_id1"].tolist()

    emil = EMIL()
    emil.data.MLE_ref_id = recommendation
    emil.data.recommendation_reason = "1"

    # concert timestamp format
    timestamp = time.time()
    dt = datetime.datetime.fromtimestamp(timestamp)
    formatted_datetime = dt.strftime("%Y-%m-%dT%H:%M:%S.%f%z")
    emil.transmitted_at = formatted_datetime

    return emil


@ai_service.get("/")
async def hello():
    return "the server is running"
