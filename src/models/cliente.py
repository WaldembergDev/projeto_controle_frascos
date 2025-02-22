from sqlalchemy import Column, Integer, String, Boolean, Enum
from sqlalchemy.orm import relationship
from src.database.db import Base
import enum

class StatusEnum(str, enum.Enum):
    ATIVO = 'ativo'
    INATIVO = 'inativo'

class Cliente(Base):
    __tablename__ = 'clientes'

    id = Column(Integer, primary_key=True)
    identificacao = Column(String(14), unique=True, nullable=False)
    nome = Column(String(254), nullable=False)
    telefone = Column(String(11), nullable=True)
    email = Column(String(254), nullable=True)
    status = Column(Enum(StatusEnum), default=StatusEnum.ATIVO)

    def to_dict(self):
        return {
            'identificacao': self.identificacao,
            'nome': self.nome,
            'telefone': self.telefone,
            'email': self.email,
        }

    solicitacoes = relationship('Solicitacao', back_populates='cliente')
    # estoques = relationship('EstoqueCliente', back_populates='cliente')
    
    
    