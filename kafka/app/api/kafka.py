import logging

from fastapi.routing import APIRouter


from ..utils.formatlogs import CustomFormatter

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(CustomFormatter())
log.addHandler(ch)


kafka =  APIRouter()

@kafka.get('/ready/')
async def get_readiness():
    return {"Hello": "Ready"}

