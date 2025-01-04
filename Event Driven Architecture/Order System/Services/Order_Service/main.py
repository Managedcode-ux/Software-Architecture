from fastapi import FastAPI,HTTPException,Depends
import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from .models import Base, Order
from .schemas import OrderCreate, OrderResponse
from .kafka_client import KafkaClient
from contextlib import contextmanager
import uvicorn


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# Database setup
DATABASE_URL = "postgresql://admin:postgres@localhost:5432/postgres"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Kafka setup
kafka_client = KafkaClient(bootstrap_servers="localhost:29092")

@contextmanager
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.on_event("startup")
async def startup_event():
    # Create database tables
    Base.metadata.create_all(bind=engine)
    logger.info("Database tables created")

@app.on_event("shutdown")
async def shutdown_event():
    kafka_client.close()
    logger.info("Application shutdown complete")

@app.get('/')
def greetings():
    return {"Message":"Hey there5"}



@app.post("/orders/", response_model=OrderResponse)
def create_order(order: OrderCreate):
    with get_db() as db:
        try:
            # Create order in database
            db_order = Order(
                customer_id=order.customer_id,
                total_amount=order.total_amount
            )
            db.add(db_order)
            db.commit()
            db.refresh(db_order)
            
            # Send order.created event
            kafka_client.send_event(
                "order.created",
                {
                    "order_id": db_order.id,
                    "customer_id": db_order.customer_id,
                    "total_amount": db_order.total_amount,
                    "status": db_order.status.value
                }
            )
            
            return db_order
        except Exception as e:
            db.rollback()
            logger.error(f"Error creating order: {e}")
            raise HTTPException(status_code=500, detail=str(e))


if __name__ ==  "__main__":
    uvicorn.run(app,port=8000)