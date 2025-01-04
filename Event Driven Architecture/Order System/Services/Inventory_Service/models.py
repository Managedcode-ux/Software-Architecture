from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Integer, Column, String

class Base(DeclarativeBase):
    pass

class Product(Base):
    __tablename__ = "inventory"

    product_id = Column(Integer,primary_key=True)
    product_name=Column(String,nullable=False)
    stock=Column(Integer,nullable=False)
    price=Column(Integer,nullable=False)

    def to_dict(self):
        return{
            "id":self.product_id,
            "product_name":self.product_name,
            "stock":self.stock,
            "price":self.price
        }


