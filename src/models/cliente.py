from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from src.database.db import Base

class Cliente(Base):
    __tablename__ = 'clientes'

    id = Column(Integer, primary_key=True)
    identificacao = Column(String(14), unique=True, nullable=False)
    nome = Column(String(254), nullable=False)
    telefone = Column(String(11), nullable=True)
    email = Column(String(254), nullable=True)

    solicitacoes = relationship('Solicitacao', back_populates='cliente')

    