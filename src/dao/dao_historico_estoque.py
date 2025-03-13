from src.models.historico_estoque import HistoricoEstoque

class DaoHistoricoEstoque:
  @classmethod
  def criar_historico_estoque(cls, session, id_item_frasco, estoque_antes_empresa,estoque_depois_empresa, estoque_antes_cliente, estoque_depois_cliente):
    historico_estoque = HistoricoEstoque(id_item_frasco = id_item_frasco,
                                         estoque_antes_empresa=estoque_antes_empresa,
                                         estoque_depois_empresa=estoque_depois_empresa,
                                         estoque_antes_cliente=estoque_antes_cliente,
                                         estoque_depois_cliente=estoque_depois_cliente)
    session.add(historico_estoque)
    return historico_estoque