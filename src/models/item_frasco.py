from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from src.database.db import Base

class ItemFrasco(Base):
    __tablename__ = 'item_frasco'
    id = Column(Integer, primary_key=True)
    quantidade = Column(Integer, nullable=False)
    id_frasco = Column(Integer, ForeignKey('frascos.id'), nullable=False)
    id_solicitacao = Column(Integer, ForeignKey('solicitacoes.id'), nullable=False)

    frasco = relationship('Frasco', back_populates='item_frasco')

