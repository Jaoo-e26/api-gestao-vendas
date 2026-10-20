from sqlalchemy import Column, ForeignKey, Integer, String, Float, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class Produto(Base):
    __tablename__ = "produtos"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    preco = Column(Float, nullable=False)
    quantidade_estoque = Column(Integer, default=0)

class Venda(Base):
    __tablename__ = "vendas" 

    id = Column(Integer, primary_key=True, index=True)
    data_venda = Column(DateTime, default=datetime.utcnow)
    valor_total = Column(Float, default=0.0)

    itens = relationship("ItemVenda", back_populates="venda")

class ItemVenda(Base):
    __tablename__ = "itens_venda"

    id = Column(Integer, primary_key=True, index=True)
    venda_id = Column(Integer, ForeignKey("vendas.id"))
    produto_id = Column(Integer, ForeignKey("produtos.id"))
    quantidade = Column(Integer, nullable=False)
    preco_unitario = Column(Float, nullable=False)

    venda = relationship("Venda", back_populates="itens")
    produto = relationship("Produto")
           
