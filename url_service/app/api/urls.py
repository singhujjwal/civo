from typing import List
from aiokafka.consumer.consumer import AIOKafkaConsumer
# from ..dependencies import get_producer
from aiokafka.producer.producer import AIOKafkaProducer
from fastapi import APIRouter, HTTPException, Depends
import logging
import redis
from starlette import responses

from .redis_py import redis_connect

# from ..dependencies import get_producer
from fastapi.param_functions import Depends
from .models import UrlOut, UrlIn
from . import url_manager
import os

## Logging code
from ..utils.formatlogs import CustomFormatter

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(CustomFormatter())
log.addHandler(ch)

## Logging end


import aiokafka
from aiokafka import AIOKafkaProducer
import asyncio


KAFKA_TOPIC = os.getenv('KAFKA_TOPIC', "URL")
KAFKA_CONSUMER_GROUP_PREFIX = os.getenv('KAFKA_CONSUMER_GROUP_PREFIX', 'url-group')
KAFKA_BOOTSTRAP_SERVERS = os.getenv('KAFKA_BOOTSTRAP_SERVERS', '127.0.0.1:9093')


# def get_producer():
#     '''
#     Callable to be used as dependency
#     '''
#     global aioproducer
#     return aioproducer

urls = APIRouter()


async def get_producer():
    aioproducer = AIOKafkaProducer(loop=asyncio.get_event_loop(), 
                    bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS)
    try:
        aioproducer.start()
        yield aioproducer
    finally:
        aioproducer.stop()


@urls.get('/ready/')
async def get_readiness():
    return {"Hello": "Ready"}

@urls.post('/', response_model=UrlOut, status_code=201)
async def get_short_url(payload: UrlIn,
    aioproducer: AIOKafkaConsumer = Depends(AIOKafkaProducer)
    # redis_client: redis.client.Redis= redis_connect()
    ):
    redis_client = redis_connect()
    if redis_client:
        short_url = await url_manager.get_short_url(redis_client, payload)

        response = {
            **short_url
        }
        return response
    else:
        raise HTTPException(status_code=500, 
                detail="Redis cache connection problem")
    

@urls.get('/long/{in_url}/', response_model=UrlIn)
async def get_long_url(in_url: str):
    redis_client = redis_connect()
    longUrl = await url_manager.get_long_url(redis_client, in_url)
    if not longUrl:
        raise HTTPException(status_code=404, 
                detail="No long url mapped to this short url")
    longUrl = longUrl.decode('utf-8')
    log.debug (f"returned long url: {longUrl} from the url_manager")
    result = {}
    result['longUrl'] = longUrl
    
    response = {
        **result
    }
    return response

