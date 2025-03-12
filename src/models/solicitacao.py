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

class TipoMovimentacaoEnum(str, enum.Enum):
    EXTERNO = 'Externa'
    INTERNO = 'Interna'

class DetalheMovimentacaoEnum(str, enum.Enum):
    # tipo externo
    EMPRESTIMO = 'Empréstimo'
    DEVOLUCAO = 'Devolução'
    # tipo interno
    CANCELAMENTO = 'Cancelamento'
    REPOSICAO = 'Reposição'
    AJUSTE = 'Ajuste'


class Movimentacao(Base):
    __tablename__ = 'movimentacoes'

    id = Column(Integer, primary_key=True)
    data = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    responsavel = Column(String(254), nullable=True)
    assinatura = Column(LargeBinary, nullable=True)
    id_usuario = Column(Integer, ForeignKey('usuarios.id'), nullable=False)
    id_cliente = Column(Integer, ForeignKey('clientes.id'), nullable=True)
    tipo_movimentacao = Column(Enum(TipoMovimentacaoEnum), default=TipoMovimentacaoEnum.EXTERNO, nullable=False)
    detalhe_movimentacao = Column(Enum(DetalheMovimentacaoEnum), nullable=False)
    descricao = Column(String(255), nullable=True)
    status = Column(Enum(StatusEnum), default=StatusEnum.PENDENTE, nullable=False)

    cliente = relationship('Cliente', back_populates='movimentacoes')