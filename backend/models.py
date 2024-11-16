from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from backend.database import Base

class Cupcake(Base):
    __tablename__ = "cupcakes"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, index=True)  # Translated to "nome"
    descricao = Column(String)         # Translated to "descricao"
    preco = Column(Float)              # Translated to "preco"

class Order(Base):
    __tablename__ = "pedidos"

    id = Column(Integer, primary_key=True, index=True)
    status = Column(String, default="aberto")
    cupcake_id = Column(Integer, ForeignKey("cupcakes.id"))
    user_id = Column(Integer)
    criado_em = Column(DateTime, default=datetime.utcnow)  # Translated to "criado_em"
    cupcake = relationship("Cupcake")
