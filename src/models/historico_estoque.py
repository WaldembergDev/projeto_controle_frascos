from sqlalchemy import Column, Integer, String, ForeignKey, Enum, DateTime
from sqlalchemy.orm import relationship
from src.database.db import Base
from sqlalchemy.sql import func
import enum
import pytz
from datetime import datetime

# Definição dos tipos de transação
class TipoTransacao(enum.Enum):
    # Transações para o cliente
    EMPRESTIMO = 'Empréstimo'
    DEVOLUCAO = 'Devolução'
    CANCELAMENTO = 'Cancelamento'
    REPOSICAO = 'Reposição'
    AJUSTE = 'Ajuste'

def get_current_utc_time():
    local_tz = pytz.timezone('America/Sao_Paulo')  # Ajuste para seu fuso horário local
    local_time = datetime.now(local_tz)
    return local_time.astimezone(pytz.utc)

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


  # movimentacao_estoque = relationship('EstoqueMovimentacao', back_populates='historico_estoque')