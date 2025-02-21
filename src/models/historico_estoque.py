from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from src.database.db import Base

class HistoricoEstoque(Base):
  __tablename__ = "historico_estoque"
  
  id = Column(Integer, primary_key=True)
  qtde = Column(Integer, nullable=False)
  id_cliente = Column(Integer, ForeignKey("clientes.id"), nullable=False)
  id_frasco = Column(Integer, ForeignKey("frascos.id"), nullable=False)
  id_tipo = Column(Integer, ForeignKey("tipos.id"), nullable=False)
  
  # id_cliente = relationship("clientes", back_populates="historico_estoque")
  # id_frasco = relationship("clientes", back_populates="historico_estoque")