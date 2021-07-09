from fastapi import FastAPI
import logging

from .utils.formatlogs import CustomFormatter
from .api.kafka import kafka


log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(CustomFormatter())
log.addHandler(ch)


app = FastAPI(openapi_url="/api/v1/kafka/openapi.json", 
                docs_url="/api/v1/kafka/docs")



app.include_router(
    kafka, prefix='/api/v1/kafka',
    # dependencies=[Depends(redis_connect)],
    tags=['urls']
    )


@app.on_event("startup")
async def startup_event():
    log.info('Initializing Kafka service....')

@app.on_event("shutdown")
async def shutdown_event():
    log.info('Shutting down Kafka Service')
