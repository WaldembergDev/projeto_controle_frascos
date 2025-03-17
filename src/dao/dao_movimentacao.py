from src.database.db import create_session
from src.models.movimentacao import Movimentacao, TipoMovimentacaoEnum, DetalheMovimentacaoEnum, StatusEnum
from datetime import datetime

class DaoMovimentacao:
  @classmethod
  def criar_movimentacao(cls, session,
                         responsavel: str,
                         id_usuario: int,
                         tipo: TipoMovimentacaoEnum,
                         detalhe_movimentacao: DetalheMovimentacaoEnum,
                         id_cliente: int=None,
                         descricao=None,
                         assinatura: str=None,
                         status: StatusEnum=None):
    movimentacao = Movimentacao(responsavel=responsavel,
                                assinatura=assinatura,
                                id_usuario=id_usuario,
                                id_cliente=id_cliente,
                                tipo=tipo,
                                detalhe_movimentacao=detalhe_movimentacao,
                                descricao=descricao,
                                status=status)  
    session.add(movimentacao)
    return movimentacao
  
    
  @classmethod
  def obter_movimentacao(cls, session, id):
    movimentacao = session.query(movimentacao).filter(movimentacao.id == id).first()
    return movimentacao
  
  @classmethod
  def obter_emprestimo_mais_recente_id_cliente(cls, session, id_cliente):
    movimentacao_mais_recente = session\
      .query(Movimentacao)\
        .filter(Movimentacao.id_cliente == id_cliente)\
          .filter(Movimentacao.detalhe_movimentacao == DetalheMovimentacaoEnum.EMPRESTIMO)\
            .order_by(Movimentacao.data.desc())\
              .first()
    return movimentacao_mais_recente


  @classmethod
  def atualizar_status_movimentacao(cls, session, id_movimentacao, novo_status):
    movimentacao = session.query(movimentacao).filter(movimentacao.id == id_movimentacao).first()
    movimentacao.status = novo_status
  
  @classmethod
  def excluir_movimentacao(cls, session, id_movimentacao):
    movimentacao = session.query(movimentacao).filter(movimentacao.id == id_movimentacao).first()
    session.delete(movimentacao)