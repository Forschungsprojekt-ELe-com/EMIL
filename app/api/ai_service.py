from fastapi import APIRouter
import time

from ai_model import ai_prediction_model
from api import db_manager
from model.LENA import LENA
from model.EMIL import EMIL


# add to APIRouter
ai_service = APIRouter()


# get all game performance model data
@ai_service.post("/")
async def get_recommendation(lena: LENA):
    statements = await db_manager.get_statements()
    result = ai_prediction_model.recommendation(statements)

    emil = EMIL()
    emil.MLE_ref_id = [1, 2, 3]
    emil.recommendation_reason = "1"
    emil.transmitted_at = time.time()
    return emil


@ai_service.get("/predict/")
async def predict():
    prediction_value = await db_manager.get_statements()
    return prediction_value
