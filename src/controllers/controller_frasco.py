from src.dao.dao_frasco import DaoFrasco
from src.dao.dao_historico_estoque import DaoHistoricoEstoque
from src.dao.dao_estoque_movimentacao import DaoEstoqueMovimentacao

from src.models.frasco import Frasco
from src.models.historico_estoque import TipoTransacao
from src.database.db import create_session
import pandas as pd

class ControllerFrasco:
    @classmethod
    def criar_frasco(cls, id_usuario, identificacao, capacidade, estoque, estoque_minimo, descricao):
        # 1 - Criar o frasco - Feito
        # 2 - Gerar o histórico referente e a quantidade criada - Feito
        # 3 - Gerar a movimentação do estoque - Feito 
        session = create_session()
        try:
            frasco = DaoFrasco.criar_frasco(session, identificacao, capacidade, estoque, estoque_minimo, descricao)
            session.flush()
            # cria um histórico da movimentação no banco de dados
            historico_estoque = DaoHistoricoEstoque.criar_historico_estoque(session=session,
                                                         id_frasco=frasco.id,
                                                           id_cliente=None,
                                                             id_usuario=id_usuario,
                                                               quantidade=estoque,
                                                                 tipo_transacao=TipoTransacao.REPOSICAO,
                                                                   descricao="Reposição de Frascos",
                                                                     id_solicitacao=None)
            session.flush()
            # gera a movimentação no estoque
            DaoEstoqueMovimentacao.criar_movimentacao_estoque(session=session,
                                                              id_historico_estoque=historico_estoque.id,
                                                              estoque_antes_empresa=0,
                                                              estoque_depois_empresa=estoque,
                                                              estoque_antes_cliente=None,
                                                              estoque_depois_cliente=None)
            session.commit()
            return True
        except Exception as e:
            print(f'Erro {e}')
            session.rollback()
            return False
        finally:
            session.close()
            
    @classmethod
    def obter_frasco_pelo_id(cls, id):
        session = create_session()
        try:
            frasco = DaoFrasco.obter_frasco(session, id)
            return frasco
        except Exception as e:
            print(f'Erro {e}')
            return None
        finally:
            session.close()
    
    @classmethod
    def obter_quantidade_frascos_pelo_id(cls, id):
        frasco = cls.obter_frasco_pelo_id(cls, id)
        quantidade_frasco = frasco.estoque
        return quantidade_frasco
        
    
    @classmethod
    def obter_todos_frascos(cls):
        session = create_session()
        try:
            frascos = DaoFrasco.obter_todos_frascos(session)
            return frascos
        except Exception as e:
            print(f'Erro: {e}')
            return []
        finally:
            session.close()
    
    @classmethod
    def obter_frascos_ativos(cls):
        session = create_session()
        try:
            frascos_ativos = DaoFrasco.obter_frascos_ativos(session)
            return frascos_ativos
        except Exception as e:
            print(f'Erro gerado: {e}')
            return None
        finally:
            session.close()
    
    @classmethod
    def gerar_dicionario_frascos_ativos(cls):
        frascos_ativos = cls.obter_frascos_ativos()
        dicionario_frascos_ativos = {frasco.identificacao: frasco.id for frasco in frascos_ativos}
        return dicionario_frascos_ativos
    
    @classmethod
    def editar_frasco_pelo_id(cls, id_frasco, nova_identificacao, nova_capacidade, novo_estoque_minimo, nova_descricao, novo_status):
        session = create_session()
        try:
            DaoFrasco.editar_frasco_pelo_id(session, id_frasco, nova_identificacao, nova_capacidade, novo_estoque_minimo, nova_descricao, novo_status)
            session.commit()
            return True
        except Exception as e:
            print(f'Erro: {e}')
            return False
        finally:
            session.close()
    
    @classmethod
    def excluir_frasco_pelo_id(cls, id_frasco):
        session = create_session()
        try:
            DaoFrasco.excluir_frasco(session, id_frasco)
            session.commit()
            return True
        except Exception as e:
            session.rollback()
            print(f'Erro gerado: {e}')
            return False
        finally:
            session.close()

        
    @classmethod
    def listar_frascos(cls):
        frascos = cls.obter_todos_frascos()
        lista_frascos = [(frasco.id, frasco.identificacao, frasco.capacidade, frasco.estoque, frasco.estoque_minimo, frasco.descricao, frasco.status) for frasco in frascos]
        return lista_frascos
    
    @classmethod
    def carregar_dataframe_frascos(cls):
        frascos = cls.listar_frascos()
        dataframe = pd.DataFrame(frascos, columns=['Id', 'identificacao', 'Capacidade', 'Estoque', 'Estoque Mínimo', 'Descrição', 'status'])
        dataframe['Selecionado'] = False
        dataframe = dataframe.reindex(['Selecionado', 'Id', 'identificacao', 'Capacidade', 'Estoque', 'Estoque Mínimo', 'Descrição', 'status'], axis=1)
        return dataframe
    
    # # @classmethod
    # def atualizar_estoque_id_frasco(cls, id_usuario: int, id_frasco: int, nova_quantidade: int, justificativa: int):
    #     session = create_session()
    #     try:
    #         historico_estoque = DaoHistoricoEstoque.criar_historico_estoque(session=session,
    #                                                                         id_frasco=id_frasco,
    #                                                                         id_cliente=None,
    #                                                                         id_usuario=id_usuario,
    #                                                                         quantidade=nova_quantidade,
    #                                                                         )
    #         frasco = DaoFrasco.atualizar_quantidade_frascos(session, id_frasco, nova_quantidade)
            
            