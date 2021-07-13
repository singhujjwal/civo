from typing import final

from aiokafka.producer import producer
from .models import UrlIn, UrlOut
import hashlib
import logging
import os
from aiokafka import AIOKafkaProducer
from ..utils.formatlogs import CustomFormatter
import asyncio


log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(CustomFormatter())
log.addHandler(ch)


KAFKA_TOPIC = os.getenv('KAFKA_TOPIC', "URL")
KAFKA_CONSUMER_GROUP_PREFIX = os.getenv('KAFKA_CONSUMER_GROUP_PREFIX', 'url-group')
KAFKA_BOOTSTRAP_SERVERS = os.getenv('KAFKA_BOOTSTRAP_SERVERS', '127.0.0.1:9093')

async def get_producer():
    aioproducer = AIOKafkaProducer(loop=asyncio.get_event_loop(), 
                    bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS)
    try:
        aioproducer.start()
        yield aioproducer
    finally:
        aioproducer.stop()


# import string
# BASE_LIST = string.digits + string.letters 
BASE_LIST = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGGHIJKLMNOPQRSTUVWXYZ'
BASE_DICT = dict((c, i) for i, c in enumerate(BASE_LIST))

def base_encode(hash_val: int, base=BASE_LIST) -> str:
    if hash_val == 0:
        return base[0]
    length = len(base)
    ret = ''
    while hash_val != 0:
        ret = base[hash_val % length] + ret
        hash_val = int(hash_val/length)
    return ret


def calculate_tiny_url(input_url: str) ->str:
    '''
    Design :
    1. Suppose we have a-z, A-Z and 0-9 and _ and @ as the characters in the tinyurl there will total of
    26+26+10 characters == 62 characters and let's suppose we need to have a tinyurl of 8 characters so total of pow(62,8) combinations of the input set which is 
    218 340 105 584 896 which is 218 trillion records wooah should be enough

    1000 000 requests per day * it will take years so lets move to a lower number say 6 characters long
    pow(62,6) == 56,800 235,584 56 billion records 

    '''
    h = hashlib.md5(input_url.encode('ascii'))
    hexnumber = h.hexdigest()[:11]
    # import pdb
    # pdb.set_trace()
    decimal_value = int(hexnumber, 16)
    return base_encode(decimal_value)


PREFIX = "https://u.co/"

# def get_tiny_url(redis_client, input_url: str) -> str:
#     '''
#     1. Check if already a tiny url is present in cache
#     '''
#     result_json = {}
#     if redis_client.exists(input_url):
#         log.info("tiny url already present in the cache, returning....")
#         suffix =  redis_client.get(input_url)
#         result_json['shortUrl'] = f"{PREFIX}{suffix}"
#         log.debug ("the tinyurl returned is {}".format(result_json['shortUrl']))
#         return result_json
#     else:
#         db_client = None
#         db_item = db_client.get(input_url)
#         if db_item:
#             redis_client.set(input_url, db_item)
#             return result_json['shortUrl'] = f"{PREFIX}{suffix}"
#         redis_client.set(input_url, db_client.get(input_url))


async def get_short_url(redis_client, payload: UrlIn):
    '''
    1. Check if already a tiny url is mapped to the long url requested
    2. Check in cache first (use a redis connection pool)
    3. Check in DB (again use a connection pool here and use that to check in DB) if present update cache and return value
    4. Create a tiny url, push to Kafka, update redis return (pass through cache)
    5. This is a synchronous operation
    '''
    log.debug ("Getting short url....")
    log.debug (payload.longUrl)
    result_json = {}
    tiny_url = calculate_tiny_url(payload.longUrl)
    
    if redis_client.exists(tiny_url):
        log.info("tiny url already present in the cache, not putting it again...")
        suffix =  redis_client.get(tiny_url)
        result_json['shortUrl'] = f"{PREFIX}{suffix}"
    else:
        log.info("Skipping DB logic for now.............")
        redis_client.set(tiny_url, payload.longUrl)
        result_json['shortUrl'] = f"{PREFIX}{tiny_url}"
        producer = get_producer()
        log.critical (producer)
        # push_to_kafka(tiny_url, payload.longUrl)
        # producer.send_and_wait(tiny_url, long_url.encode('utf-8'))
        pass
        # db_client = None
        # is_present = db_client.exists(tiny_url)
        # if is_present:
        #     redis_client.set(tiny_url, payload.longUrl)
        #     result_json['shortUrl'] = f"{PREFIX}{tiny_url}"
        # else:
        #     redis_client.set(tiny_url, payload.longUrl)
        #     push_to_kafka(tiny_url, payload.longUrl)

    log.debug ("the tinyurl returned is {}".format(result_json['shortUrl']))
    return result_json

async def get_long_url(redis_client, short_url: str):
    longUrl = None
    if redis_client.exists(short_url):
        longUrl = redis_client.get(short_url)
        log.debug (f"Getting Long url....{longUrl}")
    else:
        log.info(f"No long url mapped to the short url {short_url}")

    return longUrl
