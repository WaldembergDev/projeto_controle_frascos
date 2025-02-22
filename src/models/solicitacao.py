from sqlalchemy import Column, Integer, String, DateTime, LargeBinary, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from src.database.db import Base
from datetime import datetime, timezone

class Solicitacao(Base):
    __tablename__ = 'solicitacoes'

    id = Column(Integer, primary_key=True)
    data_solicitacao = Column(DateTime, default= func.now())
    responsavel = Column(String(254), nullable=False)
    assinatura = Column(LargeBinary, nullable=False)
    id_cliente = Column(Integer, ForeignKey('clientes.id'), nullable=False)

    cliente = relationship('Cliente', back_populates='solicitacoes')