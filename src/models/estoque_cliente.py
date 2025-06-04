from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from src.database.db import Base

class EstoqueCliente(Base):
    __tablename__ = 'estoque_cliente'

    id = Column(Integer, primary_key=True)
    id_cliente = Column(Integer, ForeignKey('clientes.id'), nullable=False)
    id_frasco = Column(Integer, ForeignKey('frascos.id'), nullable=False)
    quantidade = Column(Integer, nullable=False)

    cliente = relationship('Cliente', back_populates='estoque_cliente')
    frasco = relationship('Frasco', back_populates='estoque_cliente')