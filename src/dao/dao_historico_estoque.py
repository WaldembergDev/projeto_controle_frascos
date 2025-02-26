from src.database.db import create_session
from src.models.historico_estoque import HistoricoEstoque

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