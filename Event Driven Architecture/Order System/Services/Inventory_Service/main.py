from fastapi import FastAPI
import logging
from sqlalchemy.orm import Session,sessionmaker
from sqlalchemy import create_engine
from .models import Product
from .kafka_consumer import KafkaInventoryConsumer
from .kafka_producer import KafkaInventoryProducer
from contextlib import contextmanager
from typing import Dict,Any
import asyncio
from datetime import datetime
import uvicorn

'''
To run the server use the following command from the services directory.
`fastapi run .\Inventory_Service\main.py --port 8001 --reload`
OR
`uvicorn Inventory_Service.main:app --port 8001 `
'''

#Configuring logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Inventory Service")


#Database setup
DATABASE_URL = "postgresql://admin:postgres@localhost:5432/postgres"
engine = create_engine(DATABASE_URL)
SessionLocal  = sessionmaker(autocommit=False, autoflush= False, bind= engine)

kafka_consumer = KafkaInventoryConsumer(
    bootstrap_servers="localhost:29092",
    topic='order.created',
    group_id="inventory-service"
)
kafka_producer = KafkaInventoryProducer(
    bootstrap_servers="localhost:29092"
)

@contextmanager
def get_db():
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        db.rollback()
        raise
    finally:
        db.close()

@app.on_event("startup")
async def startup_event():
    app.state.kafka_task = asyncio.create_task(kafka_consumer.process_events(check_inventory))
    logger.info("Inventory service started and listening for orders")

@app.on_event("shutdown")
async def shutdown_event():
    if hasattr(app.state,'kafka_task'):
        app.state.kafka_task.cancel()
        try:
            await app.state.kafka_task
        except asyncio.CancelledError:
            pass
    kafka_consumer.close_consumer()
    logger.info("Inventory Consumer shutdown!")

async def check_inventory(order_data:Dict[str,Any]):
    with get_db() as db:
        try:
            order_id = order_data['order_id']
            inventory_available = True
            event_data = {
                "order_id": order_id,
                "inventory_available": inventory_available,
                "checked_at": datetime.now().isoformat()
            }
            kafka_producer.send_event("inventory.checked",event_data)
            logger.info(f"Processed inventory check for order {order_id}")
        except Exception as e:
            logger.error(f"Error checking inventory: {e}")

if __name__=="__main__":
    uvicorn.run(app,port=8001,reload=True)
