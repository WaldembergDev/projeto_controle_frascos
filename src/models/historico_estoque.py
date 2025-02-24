from sqlalchemy import Column, Integer, String, ForeignKey, Enum, DateTime
from sqlalchemy.orm import relationship
from src.database.db import Base
from sqlalchemy.sql import func
import enum

# Definição dos tipos de transação
class TipoTransacao(enum.Enum):
    ENTRADA = "Entrada"
    SAIDA = "Saída"
    AJUSTE_POSITIVO = "Ajuste Positivo"
    AJUSTE_NEGATIVO = "Ajuste Negativo"
    DEVOLUCAO = "Devolução"
    CANCELAMENTO = 'Cancelamento'

class HistoricoEstoque(Base):
  __tablename__ = "historico_estoque"
  
  id = Column(Integer, primary_key=True)
  data_movimentacao = Column(DateTime, default= func.now())
  id_frasco = Column(Integer, ForeignKey("frascos.id"), nullable=False)
  id_cliente = Column(Integer, ForeignKey("clientes.id"), nullable=True)
  id_solicitacao = Column(Integer, ForeignKey('solicitacoes.id'), nullable=True)
  id_usuario = Column(Integer, ForeignKey('usuarios.id'), nullable=False)
  quantidade = Column(Integer, nullable=False)
  tipo_transacao = Column(Enum(TipoTransacao), nullable=False)
  descricao = Column(String, nullable=True)


  # id_cliente = relationship("clientes", back_populates="historico_estoque")
  # id_frasco = relationship("clientes", back_populates="historico_estoque")