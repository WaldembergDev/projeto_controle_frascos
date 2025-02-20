from src.database.db import create_session
from src.models.cliente import Cliente

class DaoCliente:
  
  @classmethod
  def criar_cliente(cls, cliente: Cliente):
    session = create_session()
    try:
      session.add(cliente)
      session.commit()
    except Exception as e:
      session.rollback()
      print(f'Erro gerado: {e}')
    finally:
      session.close()   
  
  @classmethod
  def obter_cliente(cls, id):
    session = create_session()
    try:
      clientes = session.query(Cliente).filter(Cliente.id == id).first()
      return clientes
    except Exception as e:
      print(f'Erro gerado: {e}')
    finally:
      session.close()
  
  @classmethod
  def atualizar_cliente(cls, id, novo_nome):
    session = create_session()
    try:
      cliente = session.query(Cliente).filter(Cliente.id == id).first()
      cliente.nome = novo_nome
      session.commit()
    except Exception as e:
      session.rollback()
      print(f'Erro gerado: {e}')
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
      
  