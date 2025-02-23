from sqlalchemy import Column, Integer, String, ForeignKey, Enum
from sqlalchemy.orm import relationship
from src.database.db import Base
import enum

class StatusEnum(str, enum.Enum):
    ATIVO = 'ativo'
    INATIVO = 'inativo'

class Frasco(Base):
    __tablename__ = 'frascos'

    id = Column(Integer, primary_key=True)
    identificacao = Column(String(254), nullable=False, unique=True)
    capacidade = Column(Integer, nullable=False)
    estoque = Column(Integer, nullable=False, default=0)
    estoque_minimo = Column(Integer, nullable=False, default=0)
    descricao = Column(String(255), nullable=True)
    status = Column(Enum(StatusEnum), default=StatusEnum.ATIVO)
    

    # item_frasco = relationship('ItemFrasco', back_populates='frasco')
    # EstoqueEmpresa = relationship('EstoqueEmpresa', back_populates='Frascos')
    # estoque_cliente = relationship('EstoqueCliente', back_populates='frascos')
    # historico_estoque = relationship('HistoricoEstoque', back_populates='frasco')