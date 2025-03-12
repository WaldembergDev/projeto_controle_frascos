from src.database.db import create_session
from src.models.cliente import Cliente, StatusEnum
from src.models.movimentacao import Movimentacao

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
    
  