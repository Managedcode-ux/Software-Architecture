from kafka import KafkaProducer
import json
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class KafkaClient:
    def __init__(self, bootstrap_servers: str):
        self.producer = None
        self.bootstrap_servers = bootstrap_servers
        self.connect()

    def connect(self):
        try:
            self.producer = KafkaProducer(
                bootstrap_servers=self.bootstrap_servers,
                value_serializer=lambda v: json.dumps(v).encode('utf-8'),
                acks='all'
            )
            logger.info("Kafka producer connected successfully")
        except Exception as e:
            logger.error(f"Failed to connect Kafka producer: {e}")
            raise

    def close(self):
        if self.producer:
            self.producer.close()
            logger.info("Kafka producer closed")

    def send_event(self, topic: str, event_data: Dict[str, Any]):
        try:
            future = self.producer.send(topic, event_data)
            self.producer.flush()  # Ensure the message is sent
            future.get(timeout=10)  # Wait for the send to complete
            logger.info(f"Event sent to topic {topic}: {event_data}")
        except Exception as e:
            logger.error(f"Failed to send event to Kafka: {e}")
            raise