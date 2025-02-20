from sqlalchemy import Column, Integer, String, DateTime, LargeBinary, ForeignKey
from sqlalchemy.orm import relationship
from src.database.db import Base
from datetime import datetime, timezone

class Solicitacao(Base):
    __tablename__ = 'solicitacoes'

    id = Column(Integer, primary_key=True)
    data_solicitacao = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    responsavel = Column(String(254), nullable=False)
    assinatura = Column(LargeBinary, nullable=False)
    id_cliente = Column(Integer, ForeignKey('clientes.id'), nullable=False)

    # nome da relação = relationship(Nome_classe, nome_)
    cliente = relationship('Cliente', back_populates='solicitacoes')