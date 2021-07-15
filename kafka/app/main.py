from aiokafka.consumer.subscription_state import TopicPartitionState
from fastapi import FastAPI
import logging
import os
from random import randint
from aiokafka import AIOKafkaConsumer
import asyncio


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
    tags=['kafka']
    )

@app.on_event("startup")
async def startup_event():
    log.info('Initializing Kafka service....')
    await initialize()
    await consume()

@app.on_event("shutdown")
async def shutdown_event():
    log.info('Shutting down Kafka Service')

KAFKA_TOPIC = os.getenv('KAFKA_TOPIC', "URL")
KAFKA_CONSUMER_GROUP_PREFIX = os.getenv('KAFKA_CONSUMER_GROUP_PREFIX', 'url-group')
KAFKA_BOOTSTRAP_SERVERS = os.getenv('KAFKA_BOOTSTRAP_SERVERS', '127.0.0.1:9093')
consumer = None
consumer_task = None


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

async def initialize():
    log.debug("Initializing the kafka consumer....")
    group_id = f'{KAFKA_CONSUMER_GROUP_PREFIX}-{randint(0, 10000)}'
    log.debug(f'Initializing KafkaConsumer for topic {KAFKA_TOPIC} with group_id {group_id} and using bootstrap servers {KAFKA_BOOTSTRAP_SERVERS}')
    global consumer
    consumer = AIOKafkaConsumer(KAFKA_TOPIC, loop=asyncio.get_event_loop(),
                                         bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
                                         group_id=group_id)
    # get cluster layout and join group
    await consumer.start()

    partitions: Set[TopicPartitionState] = consumer.assignment()
    nr_partitions = len(partitions)
    if nr_partitions != 1:
        log.warning(f'Found {nr_partitions} partitions for topic {KAFKA_TOPIC}. Expecting '
                    f'only one, remaining partitions will be ignored!')
    for tp in partitions:

        # get the log_end_offset
        end_offset_dict = await consumer.end_offsets([tp])
        end_offset = end_offset_dict[tp]

        if end_offset == 0:
            log.warning(f'Topic ({KAFKA_TOPIC}) has no messages (log_end_offset: '
                        f'{end_offset}), skipping initialization ...')
            return
        # ACtual code is above one, if there should be no messages in a graceful shutdown
        # mode so there is not much other than start consumner thread to start consuming
        log.debug(f'Found log_end_offset: {end_offset} seeking to {end_offset-1}')
        consumer.seek(tp, end_offset-1)
        msg = await consumer.getone()
        log.info(f'Initializing API with data from msg: {msg}')
        return
