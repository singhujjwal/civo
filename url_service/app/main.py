from fastapi import FastAPI
from fastapi import Depends
import logging
import os
from contextvars import ContextVar
from .kafka import get_producer


from .api.urls import urls
# from .dependencies import get_producer, initialize, consume, consumer, consumer_task
from .api.redis_py import redis_connect
from .utils.formatlogs import CustomFormatter


consumer = None
consumer_task = None


USE_KAFKA = os.getenv('USE_KAFKA', False)
USE_REDIS = os.getenv('USE_REDIS', True)


log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(CustomFormatter())
log.addHandler(ch)



app = FastAPI(openapi_url="/api/v1/urls/openapi.json", 
                docs_url="/api/v1/urls/docs")


# Below code will be used to pass the producer object which is not needed in synchronous 
# process
app.include_router(
    urls, prefix='/api/v1/urls',
    dependencies=[Depends(get_producer)],
    tags=['urls']
    )

# app.include_router(
#     urls, prefix='/api/v1/urls',
#     # dependencies=[Depends(redis_connect)],
#     tags=['urls']
#     )


@app.on_event("startup")
async def startup_event():
    log.info('Initializing URL service  ...')
    aioproducer = get_producer()
    await aioproducer.start()

@app.on_event("shutdown")
async def shutdown_event():
    log.info('Shutting down API')
    aioproducer = get_producer()
    await aioproducer.stop()
    # Don't flush all from redis this will kill the stateless nature of the application
    
    # if USE_REDIS:
    #     redis_client = redis_connect()
    #     redis_client.flushall()
    #     redis_client.close()


