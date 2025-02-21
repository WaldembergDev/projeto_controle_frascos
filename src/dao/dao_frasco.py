from src.database.db import create_session
from src.models.frasco import Frasco

class DaoFrasco:
  @classmethod
  def adicionar_frasco(cls, nome, capacidade, descricao): # (cls, frasco: Frasco)
    session = create_session()
    try:
      frasco = Frasco(nome = nome, capacidade = capacidade, descricao = descricao)
      session.add(frasco)
      session.commit()
      return True
    except Exception as e:
      session.rollback()
      print(f'Erro gerado: {e}')
      return False
    finally:
      session.close()
  
  @classmethod
  def obter_todos_frascos(cls):
    session = create_session()
    try:
      frascos = session.query(Frasco).all()
      return frascos
    except Exception as e:
      print(f'Erro: {e}')
    finally:
      session.close()
  
  @classmethod
  def obter_frasco(cls, id):
    session = create_session()
    try:
      frascos = session.query(Frasco).filter(Frasco.id == id).first()
      return frascos
    except Exception as e:
      session.rollback()
      print(f'Erro gerado: {e}')
    finally:
      session.close()
      
  @classmethod
  def atualizar_frasco(cls, id, novo_frasco):
    session = create_session()
    try:
      frasco = session.query(Frasco).filter(Frasco.id == id).first()
      frasco.nome = novo_frasco
      session.commit()
    except Exception as e:
      session.rollback()
      print(f'Erro gerado: {e}')
    finally:
      session.close()
      
  @classmethod
  def excluir_frasco(cls, id):
    session = create_session()
    try:
      frasco = session.query(frasco).filter(Frasco.id == id). first()
      session.delete(frasco)
      session.commit()
    except Exception as e:
      print(f'Erro gerado: {e}')
    finally:
      session.close()
      
      
# frasco = Frasco(nome = 'Ambar', capacidade = 500, descricao = 'Frasco de vidro')
# DaoFrasco.adicionar_frasco(frasco)

      
      