from fastapi import APIRouter
from ai_model import ai_prediction_model
import api.db_manager

# add to APIRouter
ai_service = APIRouter()


# get all game performance model data
@ai_service.get("/")
async def get_game_performance_model():
    return "aiservice is running"


# get prediction values
@ai_service.get("/predict/{game_id}/{knowledge_name}")
async def predict_value(game_id: str, knowledge_name: str):
    prediction_value = await get_recommendation(knowledge_name, game_id)
    return prediction_value


async def get_recommendation(knowledge_name, game_id):
    recommendation = ai_prediction_model.recommendation()
    if recommendation:
        return recommendation
    else:
        print("no recommendation found")
        return []
