from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from src.database.db import Base

class Frasco(Base):
    __tablename__ = 'frascos'

    id = Column(Integer, primary_key=True)
    nome = Column(String(254), nullable=False)
    capacidade = Column(Integer, nullable=False)
    descricao = Column(String(255), nullable=True)

    # item_frasco = relationship('ItemFrasco', back_populates='frasco')
    # estoque_empresa = relationship('EstoqueEmpresa', back_populates='frascos')
    # estoque_cliente = relationship('EstoqueCliente', back_populates='frascos')
    # historico_estoque = relationship('HistoricoEstoque', back_populates='frasco')