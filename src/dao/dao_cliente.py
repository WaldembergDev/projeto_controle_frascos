from src.database.db import create_session
from src.models.cliente import Cliente, StatusEnum
from src.models.movimentacao import Movimentacao, DetalheMovimentacaoEnum
from src.models.estoque_cliente import EstoqueCliente
from src.models.frasco import Frasco
from sqlalchemy import select, and_, not_, exists, distinct
from datetime import datetime, timedelta

class DaoCliente:
  
  @classmethod
  def criar_cliente(cls, session, identificacao, nome, telefone, email):
    cliente = Cliente(identificacao = identificacao, nome = nome, telefone = telefone, email = email)
    session.add(cliente)
    return cliente
  
  @classmethod
  def obter_cliente_pelo_id(cls, session, id):
    cliente = session.query(Cliente).filter(Cliente.id == id).first()
    return cliente

  
  @classmethod
  def obter_todos_clientes(cls, session):
    clientes = session.query(Cliente).all()
    return clientes
  
  @classmethod
  def obter_clientes_ativos(cls, session):
    clientes_ativos = session.query(Cliente).filter(Cliente.status == StatusEnum.ATIVO.value).order_by(Cliente.nome).all()
    return clientes_ativos

  @classmethod
  def atualizar_cliente_pelo_id(cls, session, id, novo_nome, nova_identificacao, novo_email, novo_telefone, novo_status):
    cliente = session.query(Cliente).filter(Cliente.id == id).first()
    cliente.nome = novo_nome
    cliente.identificacao = nova_identificacao
    cliente.email = novo_email
    cliente.telefone = novo_telefone
    cliente.status = novo_status
    return cliente
  
  @classmethod
  def excluir_cliente(cls, session, id):
      cliente = session.query(Cliente).filter(Cliente.id == id).first()
      session.delete(cliente)
      return cliente
  
  @classmethod
  def obter_frascos_do_cliente_pelo_id(cls, session, id_cliente):
    cliente = session.query(Cliente).filter(Cliente.id == id_cliente).first()
    estoque_cliente = cliente.estoque_cliente
    return estoque_cliente
  
  @classmethod
  def obter_clientes_sem_movimentacao(cls, session, verificar_estoque_cliente: bool):
      # obtendo a data atual
      data_atual = datetime.now()
      # obtendo a data 60 dias atrás
      data_antiga = data_atual - timedelta(days=60)
        
      # Condições comuns para a subconsulta de clientes com frascos
      conditions = [
            EstoqueCliente.id_cliente == Cliente.id,
            Movimentacao.detalhe_movimentacao == DetalheMovimentacaoEnum.EMPRESTIMO,
            Movimentacao.data < data_antiga,
            Cliente.status == StatusEnum.ATIVO
        ]
        
      # Adiciona a condição EstoqueCliente.quantidade > 0 somente se estoque_cliente for True
      if verificar_estoque_cliente:
          conditions.append(EstoqueCliente.quantidade > 0)
      else:
        conditions.append(EstoqueCliente.quantidade == 0)
        
      # Subconsulta: clientes com frascos
      subquery_clientes_frasco = (
            select(distinct(Cliente.id))
            .join(EstoqueCliente, EstoqueCliente.id_cliente == Cliente.id)
            .join(Movimentacao, Movimentacao.id_cliente == Cliente.id)
            .where(and_(*conditions))
        )
        
      # Subconsulta: clientes ativos que fizeram devolução nos últimos 60 dias
      subquery_devolucoes = (
            select(Cliente.id)
            .where(
                and_(
                    Movimentacao.detalhe_movimentacao == DetalheMovimentacaoEnum.DEVOLUCAO,
                    Movimentacao.data >= data_antiga
                )
            )
        )
        
      # Consulta final: clientes que possuem frascos, mas NÃO fizeram devoluções recentes
      stmt = (
            select(Cliente)
            .where(
                Cliente.id.in_(subquery_clientes_frasco),  # Cliente tem frascos
                not_(exists(subquery_devolucoes.where(Movimentacao.id_cliente == Cliente.id)))  # Cliente não fez devolução recente
            )
        )
        
      clientes_inativos = session.execute(stmt).scalars().all()
    
      return clientes_inativos
  
  @classmethod
  def obter_clientes_ativos_com_frascos(cls, session): 
    session = create_session()
    clientes_frascos = session.query(Cliente.nome, Frasco.identificacao, EstoqueCliente.quantidade)\
      .join(EstoqueCliente, EstoqueCliente.id_cliente == Cliente.id)\
        .join(Frasco, Frasco.id == EstoqueCliente.id_frasco)\
          .filter(EstoqueCliente.quantidade > 0)\
            .order_by(Cliente.nome)\
              .all()
    return clientes_frascos
     