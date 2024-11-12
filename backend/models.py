from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from backend.database import Base

class Cupcake(Base):
    __tablename__ = "cupcakes"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    price = Column(Float)

class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, index=True)
    status = Column(String, default="aberto")
    cupcake_id = Column(Integer, ForeignKey("cupcakes.id"))
    user_id = Column(Integer)
    timestamp = Column(DateTime, default=datetime.utcnow)
    cupcake = relationship("Cupcake")
