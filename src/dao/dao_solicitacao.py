from src.database.db import create_session
from src.models.solicitacao import Solicitacao

class Solicitacao:
  @classmethod
  def adicionar_solicitacao(cls, solicitacao : Solicitacao):
    session = create_session()
    try:
      session.add(solicitacao)
      session.commit()
    except Exception as e:
      session.rollback()
      print(f'Erro gerado: {e}')
    finally:
      session.close()
      
  @classmethod
  def obter_solicitacao(cls, id):
    session = create_session()
    try:
      Solicitacoes = session.query(Solicitacao).filter(Solicitacao.id == id).first()
      return Solicitacoes
    except Exception as e:
      session.rollback()
      print(f'Erro gerado: {e}')
    finally:
      session.close()
    
  @classmethod
  def atualizar_solicitacao(cls, id, nova_solicitacao):
    session = create_session()
    try:
      solicitacao = session.query(Solicitacao).filter(Solicitacao.id == id).first()
      solicitacao.responsavel = nova_solicitacao
      session.commit()
    except Exception as e:
      session.rollback()
      print(f'Erro gerado: {e}')
    finally:
      session.close()
  
  @classmethod
  def excluir_solicitacao(cls, id):
    session = create_session()
    try:
      solicitacao = session.query(solicitacao).filter(Solicitacao.id == id). first()
      session.delete(solicitacao)
      session.commit()
    except Exception as e:
      print(f'Erro gerado: {e}')
    finally:
      session.close()
      