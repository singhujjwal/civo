import os


KAFKA_TOPIC = os.getenv('KAFKA_TOPIC', "URL")
KAFKA_CONSUMER_GROUP_PREFIX = os.getenv('KAFKA_CONSUMER_GROUP_PREFIX', 'url-group')
KAFKA_BOOTSTRAP_SERVERS = os.getenv('KAFKA_BOOTSTRAP_SERVERS', '127.0.0.1:9093')

import aiokafka
import asyncio
aioproducer = aiokafka.AIOKafkaProducer(loop=asyncio.get_event_loop(), 
                    bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS)

def get_producer():
    '''
    Callable to be used as dependency
    '''
    global aioproducer
    return aioproducer