from sqlalchemy import Column, Integer, String, Boolean, Enum, ForeignKey
from sqlalchemy.orm import relationship
from src.database.db import Base
import enum

class HistoricoEstoque(Base):
    __tablename__ = 'historico_estoque'

    id = Column(Integer, primary_key=True)
    id_item_frasco = Column(Integer, ForeignKey('item_frasco.id'), nullable=False)
    estoque_antes_empresa = Column(Integer, nullable=False)
    estoque_depois_empresa = Column(Integer, nullable=False)
    estoque_antes_cliente = Column(Integer, nullable=True)
    estoque_depois_cliente = Column(Integer, nullable=True)