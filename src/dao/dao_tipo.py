from src.database.db import create_session
from src.models.tipo import Tipo

class DaoTipo:
  @classmethod
  def adicionar_tipo(cls, tipo : Tipo):
    session = create_session()
    try: 
      session.add(tipo)
      session.commit()
    except Exception as e:
      session.rollback()
      print(f'Erro gerado: {e}')
    finally:
      session.close()
      
  @classmethod
  def atualizar_tipo(cls, id, novo_tipo):
    session = create_session()
    try:
      tipo = session.query(Tipo).filter(Tipo.id == id).first()
      tipo.nome = novo_tipo
      session.commit()
    except Exception as e:
      session.rollback()
      print(f'Erro gerado: {e}')
    finally:
      session.close()
      
  @classmethod
  def excluir_tipo(cls, id):
    session = create_session()
    try:
      tipo = session.query(tipo).filter(Tipo.id == id). first()
      session.delete(tipo)
      session.commit()
    except Exception as e:
      print(f'Erro gerado: {e}')
    finally:
      session.close()
      
tipo = Tipo(nome ='entrada')      
DaoTipo.adicionar_tipo(tipo)
