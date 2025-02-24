from src.database.db import create_session
from src.models.solicitacao import Solicitacao
from datetime import datetime

class DaoSolicitacao:
  @classmethod
  def criar_solicitacao(cls, session, responsavel: str, id_cliente: int, assinatura: str=None):
    solicitacao = Solicitacao(responsavel=responsavel, assinatura=assinatura, id_cliente=id_cliente)
    session.add(solicitacao)
    return solicitacao      
  
      
  @classmethod
  def obter_solicitacao(cls, id):
    session = create_session()
    try:
      Solicitacoes = session.query(Solicitacao).filter(Solicitacao.id == id).first()
      return Solicitacoes
    except Exception as e:
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
      solicitacao = session.query(Solicitacao).filter(Solicitacao.id == id). first()
      session.delete(solicitacao)
      session.commit()
    except Exception as e:
      print(f'Erro gerado: {e}')
    finally:
      session.close()
  
      