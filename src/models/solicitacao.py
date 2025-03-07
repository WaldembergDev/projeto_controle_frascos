from sqlalchemy import Column, Integer, String, DateTime, LargeBinary, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from src.database.db import Base
from datetime import datetime, timezone
import enum

class StatusEnum(str, enum.Enum):
    PENDENTE = 'pendente'
    CONCLUIDO = 'concluido'
    CANCELADO = 'cancelado'

class TipoSolicitacaoEnum(str, enum.Enum):
    EXTERNO = 'Externa'
    INTERNO = 'Interna'    


class Solicitacao(Base):
    __tablename__ = 'solicitacoes'

    id = Column(Integer, primary_key=True)
    data_solicitacao = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    responsavel = Column(String(254), nullable=True)
    assinatura = Column(LargeBinary, nullable=True)
    id_cliente = Column(Integer, ForeignKey('clientes.id'), nullable=True)
    status = Column(Enum(StatusEnum), default=StatusEnum.CONCLUIDO, nullable=False)
    tipo_solicitacao = Column(Enum(TipoSolicitacaoEnum), default=TipoSolicitacaoEnum.EXTERNO, nullable=False)

    cliente = relationship('Cliente', back_populates='solicitacoes')