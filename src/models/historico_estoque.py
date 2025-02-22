from sqlalchemy import Column, Integer, String, ForeignKey, Enum, DateTime
from sqlalchemy.orm import relationship
from src.database.db import Base
from sqlalchemy.sql import func
import enum

# Definição dos tipos de transação
class TipoTransacao(enum.Enum):
    ENTRADA = "Entrada"
    SAIDA = "Saída"
    AJUSTE = "Ajuste"
    DEVOLUCAO = "Devolução"

class HistoricoEstoque(Base):
  __tablename__ = "historico_estoque"
  
  id = Column(Integer, primary_key=True)
  data_movimentacao = Column(DateTime, default= func.now())
  id_frasco = Column(Integer, ForeignKey("frascos.id"), nullable=False)
  cliente_id = Column(Integer, ForeignKey("clientes.id"), nullable=True)
  quantidade = Column(Integer, nullable=False)
  tip_transacao = Column(Enum(TipoTransacao), nullable=False)
  descricao = Column(String, nullable=True)


  # id_cliente = relationship("clientes", back_populates="historico_estoque")
  # id_frasco = relationship("clientes", back_populates="historico_estoque")