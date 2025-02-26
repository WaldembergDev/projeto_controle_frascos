from src.dao.dao_frasco import DaoFrasco
from src.dao.dao_solicitacao import DaoSolicitacao
from src.dao.dao_estoque_cliente import DaoEstoqueCliente
from src.dao.dao_item_frasco import DaoItemFrasco
from src.dao.dao_historico_estoque import DaoHistoricoEstoque
from src.dao.dao_estoque_movimentacao import DaoEstoqueMovimentacao

from src.models.historico_estoque import TipoTransacao

from src.database.db import create_session

class ControllerSolicitacaoEstoque:
    @classmethod
    def criar_solicitacao_com_itens(cls, id_usuario: int, responsavel: str, id_cliente: int, dados_frascos: list, assinatura: str=None):
        # 1 - Criar uma solicitação
        # 2 - Percorrer por cada um dos frascos
        # 3 - Criar um itemFrasco associado à solicitação
        # 4 - Para cada frasco da solicitação deve-se:
        #   3.1 - Gerar um histórico da movimentação 
        #   3.2 - reduzir a quantidade de frascos do estoque da empresa referente ao frasco
        #   3.3 - aumentar a quantidade de frascos do estoque do cliente referente ao frasco
        
        session = create_session()
        try:
            # 1 - criando a solicitação
            solicitacao = DaoSolicitacao.criar_solicitacao(session, responsavel=responsavel, id_cliente=id_cliente, assinatura=assinatura) 
            session.flush() # gerando o id da solicitação
            # percorrendo pela lista de frascos
            for (id_frasco, quantidade) in dados_frascos:
                # criando item frasco associado à solicitação
                DaoItemFrasco.criar_item_frasco(session, quantidade=quantidade, id_frasco=id_frasco, id_solicitacao=solicitacao.id)
                # gerar histórico da movimentação
                historico_estoque = DaoHistoricoEstoque.criar_historico_estoque(session,
                                                                                 id_frasco,
                                                                                   id_cliente,
                                                                                     id_usuario,
                                                                                       quantidade,
                                                                                         TipoTransacao.EMPRESTIMO.value,
                                                                                           None,
                                                                                            solicitacao.id)
                session.flush()
                # descobrir quantidade de frascos que a empresa tem
                estoque_empresa = DaoFrasco.obter_frasco(session, id_frasco)
                estoque_antes_empresa = estoque_empresa.estoque 
                estoque_depois_empresa = estoque_antes_empresa - quantidade
                # obter o estoque do frasco do cliente
                estoque_cliente = DaoEstoqueCliente.obter_estoque_cliente_pelo_id(session, id_cliente=id_cliente, id_frasco=id_frasco)
                if not estoque_cliente:
                    estoque_antes_cliente = 0
                else:
                    estoque_antes_cliente = estoque_cliente.quantidade
                estoque_depois_cliente = estoque_antes_cliente + quantidade
                # criando a movimentação
                DaoEstoqueMovimentacao.criar_movimentacao_estoque(session,
                                                                   id_historico_estoque=historico_estoque.id,
                                                                   estoque_antes_empresa = estoque_antes_empresa,
                                                                     estoque_depois_empresa=estoque_depois_empresa,
                                                                     estoque_antes_cliente=estoque_antes_cliente,
                                                                      estoque_depois_cliente=estoque_depois_cliente)
                # atualizar a quantidade de frascos que a empresa tem
                DaoFrasco.subtrair_quantidade_frascos(session, id_frasco=id_frasco, quantidade=quantidade)
                # atualizar a quantidade de frascos que estão em posse do cliente
                estoque_cliente = DaoEstoqueCliente.obter_estoque_cliente_pelo_id(session, id_cliente, id_frasco)
                if not estoque_cliente:
                    DaoEstoqueCliente.criar_frasco_estoque_cliente(session, id_frasco, id_cliente, quantidade)
                else:
                    DaoEstoqueCliente.atualizar_estoque_cliente(session, id_frasco, id_cliente, quantidade)          
            session.commit()    
            return True
        except Exception as e:
            print(f'Erro: {e}')
            return False
        finally:
            session.close()
    
    @classmethod
    def devolver_frascos(cls, id_usuario: int, id_cliente: int, frascos: list):
        session = create_session()
        try:
            for (id_frasco, quantidade) in frascos:
                historico_estoque = DaoHistoricoEstoque.criar_historico_estoque(session, id_frasco, id_cliente, id_usuario, quantidade, TipoTransacao.DEVOLUÇÃO.value, None, None)
                session.flush() # gerando o id do historico estoque
                # obtendo os dados do estoque da empresa
                frasco_empresa = DaoFrasco.obter_frasco(session, id_frasco)
                estoque_antes_empresa = frasco_empresa.estoque
                estoque_depois_empresa = estoque_antes_empresa + quantidade
                # obtendo os dados do estoque do cliente
                frasco_cliente = DaoEstoqueCliente.obter_estoque_cliente_pelo_id(session, id_cliente, id_frasco)
                estoque_antes_cliente = frasco_cliente.quantidade
                estoque_depois_cliente = estoque_antes_cliente - quantidade
                # registrando a movimentação
                estoque_movimentacao = DaoEstoqueMovimentacao.criar_movimentacao_estoque(session,
                                                                                          historico_estoque.id,
                                                                                            estoque_antes_empresa,
                                                                                              estoque_depois_empresa,
                                                                                                estoque_antes_cliente,
                                                                                                  estoque_depois_cliente)
                # registrando a mudança no estoque da empresa
                DaoFrasco.adicionar_quantidade_frascos(session, id_frasco, quantidade)
                # registrando a mudança no estoque do cliente
                DaoEstoqueCliente.reduzir_estoque_cliente(session, id_frasco, id_cliente, quantidade)
            session.commit()
            return True
        except Exception as e:
            session.rollback()
            print(f'Erro {e}')
            return False
        finally:
            session.close()
    
    @classmethod
    def obter_todo_historico(cls):
        session = create_session()
        try:
            historico = DaoHistoricoEstoque.obter_todo_historico(session)
            return historico
        except Exception as e:
            print(f'Erro: {e}')
            return None
        finally:
            session.close()