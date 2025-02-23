from sqlalchemy import Column, Integer, String, DateTime, LargeBinary, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from src.database.db import Base
from datetime import datetime
import enum

class StatusEnum(str, enum.Enum):
    PENDENTE = 'pendente'
    CONCLUIDO = 'concluido'
    CANCELADO = 'cancelado'


class Solicitacao(Base):
    __tablename__ = 'solicitacoes'

    id = Column(Integer, primary_key=True)
    data_solicitacao = Column(DateTime, default= func.now())
    responsavel = Column(String(254), nullable=False)
    assinatura = Column(LargeBinary, nullable=True)
    id_cliente = Column(Integer, ForeignKey('clientes.id'), nullable=False)
    status = Column(Enum(StatusEnum), default=StatusEnum.CONCLUIDO)

    cliente = relationship('Cliente', back_populates='solicitacoes')