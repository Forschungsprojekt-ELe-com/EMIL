import sys

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.ai_service import ai_service

app = FastAPI()

sys.path.insert(0, '../..')

# CORS
origins = [
    "http://localhost:4200",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup():
    pass


@app.get("/")
def hello():
    return "The service is running"


app.include_router(ai_service, prefix='/aiservice', tags=['aiservice'])
