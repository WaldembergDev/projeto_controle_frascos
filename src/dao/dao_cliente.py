from src.database.db import create_session
from src.models.cliente import Cliente
from src.models.solicitacao import Solicitacao

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
  