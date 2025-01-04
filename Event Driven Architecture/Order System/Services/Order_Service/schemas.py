from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

class OrderCreate(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    customer_id: int
    total_amount: float

class OrderResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    customer_id: int
    total_amount: float
    status: str
    created_at: datetime
    updated_at: datetime