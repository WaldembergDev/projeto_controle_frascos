from src.database.db import create_session
from src.models.historico_estoque import HistoricoEstoque, TipoTransacao
from src.models.frasco import Frasco
from src.models.cliente import Cliente
from src.models.usuario import Usuario
from src.models.solicitacao import Solicitacao
from models.historico_estoque import EstoqueMovimentacao
from sqlalchemy.sql import func

class DaoHistoricoEstoque:
    @classmethod
    def criar_historico_estoque(cls, session, id_frasco, id_cliente, id_usuario, quantidade, tipo_transacao, descricao, id_solicitacao):
        historico_estoque = HistoricoEstoque(id_frasco = id_frasco,
                                              id_cliente = id_cliente,
                                                id_usuario=id_usuario,
                                                  quantidade=quantidade,
                                                    tipo_transacao=tipo_transacao,
                                                      descricao=descricao,
                                                        id_solicitacao=id_solicitacao)
        session.add(historico_estoque)
        return historico_estoque
    
    @classmethod
    def obter_todo_historico(cls, session):
        historico = session.query(HistoricoEstoque).all()
        return historico

    @classmethod
    def obter_historico_movimentacao(cls, session):
        resultados = session.query(HistoricoEstoque.id,
                                    HistoricoEstoque.data_movimentacao,
                                      Frasco.identificacao,
                                        Cliente.nome,
                                          Usuario.login,
                                              HistoricoEstoque.quantidade,
                                                HistoricoEstoque.tipo_transacao,
                                                  HistoricoEstoque.descricao, Solicitacao.id,
                                                    EstoqueMovimentacao.estoque_antes_empresa,
                                                      EstoqueMovimentacao.estoque_depois_empresa,
                                                        EstoqueMovimentacao.estoque_antes_cliente,
                                                          EstoqueMovimentacao.estoque_depois_cliente)\
          .join(Frasco, isouter=True)\
            .join(Cliente, isouter=True)\
              .join(Usuario, isouter=True)\
                .join(Solicitacao, HistoricoEstoque.id_solicitacao == Solicitacao.id, isouter=True)\
                  .join(EstoqueMovimentacao, HistoricoEstoque.id == EstoqueMovimentacao.id_historico_estoque, isouter=True)\
                    .all()
        return resultados
    
    @classmethod
    def obter_tipo_transacoes(cls, session):
        tipos_transacoes = session.query(HistoricoEstoque.tipo_transacao).distinct().all()
        return tipos_transacoes
    
    @classmethod
    def obter_devolucao_mais_recente_id_cliente(cls, session, id_cliente):
      devolucao_mais_recente = session.query(HistoricoEstoque).filter(HistoricoEstoque.id_cliente == id_cliente).filter(HistoricoEstoque.tipo_transacao==TipoTransacao.DEVOLUCAO).order_by(HistoricoEstoque.data_movimentacao.desc()).first()
      return devolucao_mais_recente
