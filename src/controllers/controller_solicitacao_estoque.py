from src.dao.dao_frasco import DaoFrasco
from src.dao.dao_solicitacao import DaoSolicitacao
from src.dao.dao_estoque_cliente import DaoEstoqueCliente
from src.dao.dao_item_frasco import DaoItemFrasco
from src.dao.dao_historico_estoque import DaoHistoricoEstoque
from src.dao.dao_estoque_movimentacao import DaoEstoque

from src.database.db import create_session

class ControllerSolicitacaoEstoque:
    @classmethod
    def criar_solicitacao_com_itens(cls, id_usuario: int, responsavel: str, id_cliente: int, dados_frascos: list, assinatura: str=None):
        # 1 - Criar uma solicitação
        # 2 - Percorrer por cada um dos frascos
        # 3 - Criar um itemFrasco associado à solicitação
        # 4 - Para cada frasco da solicitação deve-se:
        #   3.1 - reduzir a quantidade de frascos do estoque da empresa referente ao frasco
        #   3.2 - reduzir a quantidade de frascos do estoque do cliente referente ao frasco
        #   3.3 - Gerar um histórico da movimentação 
        session = create_session()
        try:
            # 1 - criando a solicitação
            solicitacao = DaoSolicitacao.criar_solicitacao(session, responsavel=responsavel, id_cliente=id_cliente, assinatura=assinatura) 
            session.flush() # gerando o id da solicitação
            # percorrendo pela lista de frascos
            for (id_frasco, quantidade) in dados_frascos:
                item_frasco = DaoItemFrasco.criar_item_frasco(session, quantidade=quantidade, id_frasco=id_frasco, id_solicitacao=solicitacao.id)
                DaoFrasco.ajustar_quantidade_frascos(session, id_frasco=id_frasco, quantidade=quantidade, tipo_movimentacao='Saída')
                historico_estoque = DaoHistoricoEstoque.criar_historico_estoque(session, id_frasco, id_cliente, id_usuario, quantidade, tipo_transacao='Saída', descricao=None, id_solicitacao=solicitacao.id)
                session.flush()
                estoque_empresa = DaoFrasco.obter_frasco(session, id_frasco)
                estoque_antes_empresa = estoque_empresa.estoque
                estoque_cliente = DaoEstoqueCliente.obter_estoque_cliente_pelo_id(session, id_cliente=id_cliente, id_frasco=id_frasco)
                estoque_antes_cliente = estoque_cliente.quantidade
                DaoEstoque.criar_movimentacao_estoque(session, tipo_movimentacao='Saída', id_historico_estoque=historico_estoque.id, estoque_antes_cliente=estoque_antes_empresa, quantidade=quantidade, estoque_antes_empresa = estoque_antes_cliente)
            session.commit()             

        except Exception as e:
            print(f'Erro: {e}')
            return False
        finally:
            session.close()
