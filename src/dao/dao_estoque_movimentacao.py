from src.models.estoque_movimentacao import EstoqueMovimentacao
from src.database.db import create_session

class DaoEstoqueMovimentacao:
    @classmethod
    def criar_movimentacao_estoque_apagar(cls, session, tipo_movimentacao: str, id_historico_estoque: int, estoque_antes_empresa: int, quantidade: int, estoque_antes_cliente: int = None):
        if tipo_movimentacao == "Saída" or tipo_movimentacao == 'Ajuste Negativo':
            quantidade *= (-1)
        estoque_depois_empresa = estoque_antes_empresa + quantidade
        # verificando se existe um estoque anterior do cliente
        if estoque_antes_cliente:
            estoque_depois_cliente = estoque_antes_cliente + quantidade
        else:
            estoque_depois_cliente = None
        movimentacao_estoque = EstoqueMovimentacao(id_historico_estoque = id_historico_estoque,
                                       estoque_antes_empresa=estoque_antes_empresa,
                                       estoque_depois_empresa=estoque_depois_empresa,
                                        estoque_antes_cliente=estoque_antes_cliente,
                                         estoque_depois_cliente=estoque_depois_cliente)
        session.add(movimentacao_estoque)
        return movimentacao_estoque
    
    @classmethod
    def criar_movimentacao_estoque(cls, session, id_historico_estoque: int, estoque_antes_empresa: int, estoque_depois_empresa: int, estoque_antes_cliente: int, estoque_depois_cliente: int):
        estoque_movimentacao = EstoqueMovimentacao(id_historico_estoque = id_historico_estoque,
                                                   estoque_antes_empresa = estoque_antes_empresa,
                                                   estoque_depois_empresa = estoque_depois_empresa,
                                                   estoque_antes_cliente = estoque_antes_cliente,
                                                   estoque_depois_cliente = estoque_depois_cliente)
        session.add(estoque_movimentacao)
        return estoque_movimentacao
                    