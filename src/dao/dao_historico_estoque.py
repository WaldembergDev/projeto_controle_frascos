from src.models.historico_estoque import HistoricoEstoque
from src.models.item_frasco import ItemFrasco
from src.models.movimentacao import Movimentacao
from src.models.frasco import Frasco
from src.models.estoque_empresa import EstoqueEmpresa
from src.models.cliente import Cliente
from src.models.usuario import Usuario

from src.database.db import create_session

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
  
  @classmethod
  def obter_lista_historico_estoque(cls, session):
    resultado = session\
      .query(HistoricoEstoque.id,
              Movimentacao.data,
              Frasco.identificacao,
              Cliente.nome,
              Usuario.nome,
              ItemFrasco.quantidade,
              Movimentacao.detalhe_movimentacao,
              Movimentacao.descricao,
              Movimentacao.id,
              HistoricoEstoque.estoque_antes_empresa,
              HistoricoEstoque.estoque_depois_empresa,
              HistoricoEstoque.estoque_antes_cliente,
              HistoricoEstoque.estoque_depois_cliente)\
        .join(ItemFrasco, HistoricoEstoque.id_item_frasco == ItemFrasco.id, isouter=True)\
            .join(Movimentacao, Movimentacao.id == ItemFrasco.id_movimentacao, isouter=True)\
              .join(Frasco, ItemFrasco.id_frasco == Frasco.id, isouter=True)\
                .join(Cliente, Movimentacao.id_cliente == Cliente.id, isouter=True)\
                  .join(Usuario, Movimentacao.id_usuario == Usuario.id, isouter=True)\
                    .all()
    return resultado