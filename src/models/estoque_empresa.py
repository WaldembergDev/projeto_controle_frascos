from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from src.database.db import Base

class EstoqueEmpresa(Base):
    __tablename__ = 'estoque_empresa'

    id = Column(Integer, primary_key=True)
    id_frasco = Column(Integer, ForeignKey('frascos.id'), nullable=False)
    quantidade = Column(Integer, nullable=False)

    # Frascos = relationship('Frasco', back_populates='EstoqueEmpresa')