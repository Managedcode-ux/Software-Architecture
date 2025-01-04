from sqlalchemy import Column, Integer, String, Float, DateTime, Enum
from sqlalchemy.orm import DeclarativeBase
import enum
from datetime import datetime

class Base(DeclarativeBase):
    pass

class OrderStatus(enum.Enum):
    CREATED = "created"
    INVENTORY_CHECKED = "inventory_checked"
    PAYMENT_PROCESSED = "payment_processed"
    CONFIRMED = "confirmed"
    SHIPPED = "shipped"
    DELIVERED = "delivered"

class Order(Base):
    __tablename__ = "orders"
    
    id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, nullable=False)
    total_amount = Column(Float, nullable=False)
    status = Column(Enum(OrderStatus), default=OrderStatus.CREATED)
    created_at = Column(DateTime, default=datetime.today)
    updated_at = Column(DateTime, default=datetime.today, onupdate=datetime.today)

    def to_dict(self):
        return {
            "id": self.id,
            "customer_id": self.customer_id,
            "total_amount": self.total_amount,
            "status": self.status.value,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }