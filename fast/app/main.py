from fastapi import FastAPI, APIRouter
import logging
from typing import List






log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

app = FastAPI(openapi_url="/api/v1/poc/openapi.json", 
                docs_url="/api/v1/poc/docs")

# poc = APIRouter()
# app.include_router(
#     poc, 
#     prefix='/api/v1/poc',
#     tags=['poc']
# )


@app.get("/")
async def root():
    return {"message": "Hello World"}

# Order matters
@app.get("/items/me")
async def return_item():
    return {"item_id": "This is current user"}

@app.get("/items/{item_id}")
async def return_items(item_id: str):
    return {"item_id": item_id}


from enum import Enum

class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"


@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    if model_name == ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}

    if model_name.value == "lenet":
        return {"model_name": model_name, "message": "LeCNN all the images"}

    return {"model_name": model_name, "message": "Have some residuals"}

# @poc.get('/ready/')
# async def get_readiness():
#     return {"Hello": "Ready"}

from typing import Set, Tuple
from typing import Dict
from typing import Optional


def say_hi(name: Optional[str] = None):
    if name:
        print (f"Hello {name}")
    else:
        print ("No name was provided")

def process_items(items: List[str], prices: Dict[str, float]):
    for item in items:
        print (item)
    pass


from pydantic import BaseModel
from datetime import datetime

class User(BaseModel):
    id: int
    name =  "Jon Doe"
    signup_ts: Optional[datetime] = None
    friends: List[int] = []


external_data = {
    "id": "123",
    "signup_ts": "2017-06-01 12:22",
    "friends": [1, "2", b"3"],
}

user = User(**external_data)


@app.on_event("startup")
async def startup_event():
    log.info('Initializing URL service  ...')
    print ("I am starting....")
    say_hi()
    say_hi("Ujjwal!!")
    print (user)


@app.on_event("shutdown")
async def shutdown_event():
    log.info('Shutting down API')