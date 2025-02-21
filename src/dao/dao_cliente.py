from src.database.db import create_session
from src.models.cliente import Cliente

class DaoCliente:
  
  @classmethod
  def criar_cliente(cls, identificacao, nome, telefone, email):
    session = create_session()
    try:
      cliente = Cliente(identificacao = identificacao, nome = nome, telefone = telefone, email = email)
      session.add(cliente)
      session.commit()
      return True
    except Exception as e:
      session.rollback()
      print(f'Erro gerado: {e}')
      return False
    finally:
      session.close()   
  
  @classmethod
  def obter_cliente_pelo_id(cls, id):
    session = create_session()
    try:
      cliente = session.query(Cliente).filter(Cliente.id == id).first()
      return cliente
    except Exception as e:
      print(f'Erro gerado: {e}')
    finally:
      session.close()

  
  @classmethod
  def obter_todos_clientes(cls):
    session = create_session()
    try:
      clientes = session.query(Cliente).all()
      return clientes
    except Exception as e:
      print(f'Erro gerado: {e}')
    finally:
      session.close()
  
  @classmethod
  def atualizar_cliente_pelo_id(cls, id, novo_nome, nova_identificacao, novo_email, novo_telefone):
    session = create_session()
    try:
      cliente = session.query(Cliente).filter(Cliente.id == id).first()
      cliente.nome = novo_nome
      cliente.identificacao = nova_identificacao
      cliente.email = novo_email
      cliente.telefone = novo_telefone
      session.commit()
      return True
    except Exception as e:
      session.rollback()
      print(f'Erro gerado: {e}')
      return False
    finally:
      session.close()
  
  @classmethod
  def excluir_cliente(cls, id):
    session = create_session()
    try:
      cliente = session.query(Cliente).filter(Cliente.id == id).first()
      session.delete(cliente)
      session.commit()
    except Exception as e:
      print(f'Erro gerado: {e}')
    finally:
      session.close()
      
  