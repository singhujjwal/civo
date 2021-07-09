import os
import logging

import asyncio
import aiokafka
from random import randint
from kafka import TopicPartition


from .utils.formatlogs import CustomFormatter

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(CustomFormatter())
log.addHandler(ch)



aioproducer = aiokafka.AIOKafkaProducer(loop=loop, 
                    bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS)
consumer = None
consumer_task = None


def get_producer() -> aiokafka.AIOKafkaProducer:
    global aioproducer
    print ("Although producer is not being used and it is not explicitly defined in the router"
    "but still it can be included in a path")
    return aioproducer



async def send_consumer_message(consumer):
    try:
        async for msg in consumer:
            log.info(f"Consumed message {msg}")
            
    finally:
        log.warning("Stopping consumeer...")
        await consumer.stop()


def done_consuming():
    log.info("Consumer is done consuming the message... so an acknowledgement be sent...")

async def consume():
    
    global consumer_task
    consumer_task = asyncio.create_task(send_consumer_message(consumer))
    consumer_task.add_done_callback(done_consuming())
    return