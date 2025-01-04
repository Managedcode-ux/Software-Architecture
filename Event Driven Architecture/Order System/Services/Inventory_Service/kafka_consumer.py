from kafka import KafkaConsumer
import json
import logging
from typing import Callable,Dict,Any
import asyncio

logger = logging.getLogger(__name__)

class KafkaInventoryConsumer:
    def __init__(self,bootstrap_servers:str, topic:str, group_id:str):
        self.consumer = KafkaConsumer(
            topic,
            bootstrap_servers = bootstrap_servers,
            group_id=group_id,
            value_deserializer=lambda m: json.loads(m.decode('utf-8')),
            auto_offset_reset = 'earliest',
            enable_auto_commit=True
        )
        logger.info(f"Kafka Consumer connected to topic {topic}")


    async def process_events(self, event_handler:Callable):
        # Continuously process incoming events using the provided handler
        try:
            while True:
                messages = self.consumer.poll(timeout_ms=1000)
                for tp,msgs in messages.items():
                    for message in msgs:
                        try:
                            print("MESSAGE printed here -",message.value)
                            await event_handler(message.value)
                        except Exception as e:
                            logger.error(f"Error processing message: {e}")
                await asyncio.sleep(0.1)
        except Exception as e:
            logger.error(f"Consumer error: {e}")
            raise

    def close_consumer(self):
        if self.consumer:
            self.consumer.close()
            logger.info("Kafka consumer closed!")
