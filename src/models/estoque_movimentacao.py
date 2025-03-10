from sqlalchemy import Column, Integer, String, Boolean, Enum, ForeignKey
from sqlalchemy.orm import relationship
from src.database.db import Base
import enum

class EstoqueMovimentacao(Base):
    __tablename__ = 'estoque_movimentacao'

    id = Column(Integer, primary_key=True)
    id_historico_estoque = Column(Integer, ForeignKey('historico_estoque.id'), nullable=False)
    estoque_antes_empresa = Column(Integer, nullable=False)
    estoque_depois_empresa = Column(Integer, nullable=False)
    estoque_antes_cliente = Column(Integer, nullable=True)
    estoque_depois_cliente = Column(Integer, nullable=True)
    
    # historico_estoque = relationship('HistoricoEstoque', back_populates='movimentacao_estoque')