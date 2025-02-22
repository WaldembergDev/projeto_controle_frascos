from src.database.db import create_session
from src.models.solicitacao import Solicitacao
from src.models.item_frasco import ItemFrasco
from datetime import datetime

class DaoSolicitacao:
  @classmethod
  def criar_solicitacaoc_com_itens(cls, data_solicitacao: datetime, responsavel: str, assinatura: str, id_cliente: int, dados_frascos: list):
    session = create_session()
    try:
      solicitacao = Solicitacao(data_solicitacao=data_solicitacao, responsavel=responsavel, assinatura=assinatura, id_cliente=id_cliente)
      session.add(solicitacao)
      session.flush()

      for (frasco, quantidade) in dados_frascos:
        item = ItemFrasco(quantidade=quantidade, id_frasco=frasco.id, id_solicitacao = solicitacao.id)
        session.add(item)
      
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
  
      