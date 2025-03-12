# from src.database.db import create_session
# from src.models.movimentacao import Movimentacao
# from datetime import datetime

# class DaoSolicitacao:
#   @classmethod
#   def criar_solicitacao(cls, session, responsavel: str, id_cliente: int, assinatura: str=None):
#     solicitacao = Solicitacao(responsavel=responsavel, assinatura=assinatura, id_cliente=id_cliente)
#     session.add(solicitacao)
#     return solicitacao      
  
      
#   @classmethod
#   def obter_solicitacao(cls, session, id):
#     solicitacao = session.query(Solicitacao).filter(Solicitacao.id == id).first()
#     return solicitacao
  
#   @classmethod
#   def obter_solicitacao_mais_recente_id_cliente(cls, session, id_cliente):
#     solicitacao_mais_recente = session.query(Solicitacao).filter(Solicitacao.id_cliente == id_cliente).order_by(Solicitacao.data_solicitacao.desc()).first()
#     return solicitacao_mais_recente


#   @classmethod
#   def atualizar_status_solicitacao(cls, session, id_solicitacao, novo_status):
#     solicitacao = session.query(Solicitacao).filter(Solicitacao.id == id_solicitacao).first()
#     solicitacao.status = novo_status
  
#   @classmethod
#   def excluir_solicitacao(cls, session, id_solicitacao):
#     solicitacao = session.query(Solicitacao).filter(Solicitacao.id == id_solicitacao).first()
#     session.delete(solicitacao)
  
      