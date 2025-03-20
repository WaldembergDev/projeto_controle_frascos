from src.models.movimentacao import Movimentacao, TipoMovimentacaoEnum, DetalheMovimentacaoEnum

from src.dao.dao_frasco import DaoFrasco
from src.dao.dao_item_frasco import DaoItemFrasco
from src.dao.dao_movimentacao import DaoMovimentacao
from src.dao.dao_historico_estoque import DaoHistoricoEstoque
from src.dao.dao_estoque_empresa import DaoEstoqueEmpresa
from src.models.frasco import Frasco
from src.database.db import create_session
import pandas as pd

class ControllerFrasco:
    @classmethod
    def criar_frasco(cls, id_usuario, identificacao, capacidade, estoque_real, estoque_minimo, descricao):
        # 1 - Criar o frasco - Feito
        # 2 - Gerar o histórico referente e a quantidade criada - Feito
        # 3 - Gerar a movimentação do estoque - Feito 
        session = create_session()
        try:
            # criando o frasco
            frasco = DaoFrasco.criar_frasco(session, identificacao, capacidade, descricao)
            session.flush()
            # cria um histórico da movimentação no banco de dados
            movimentacao = DaoMovimentacao\
                .criar_movimentacao(session = session,
                                    responsavel=None,
                                    id_usuario=id_usuario,
                                    tipo=TipoMovimentacaoEnum.INTERNO.value,
                                    detalhe_movimentacao=DetalheMovimentacaoEnum.COMPRA.value,
                                    id_cliente=None,
                                    descricao='Compra de novos frascos',
                                    assinatura=None)
            session.flush()
            # gerando o item_frasco
            item_frasco = DaoItemFrasco.criar_item_frasco(session,
                                            quantidade=estoque_real,
                                            id_frasco=frasco.id,
                                            id_movimentacao=movimentacao.id)
            session.flush()
            # gera a movimentação no estoque
            DaoHistoricoEstoque.criar_historico_estoque(session=session,
                                                        id_item_frasco=item_frasco.id,
                                                        estoque_antes_empresa=0,
                                                        estoque_depois_empresa=estoque_real,
                                                        estoque_antes_cliente=None,
                                                        estoque_depois_cliente=None)
            # Gerando os dados referente ao estoque do frasco
            DaoEstoqueEmpresa.criar_estoque_empresa(session,
                                                    frasco.id,
                                                    estoque_real=estoque_real,
                                                    estoque_minimo=estoque_minimo)
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
    def obter_frascos_com_estoque(cls):
        session = create_session()
        try:
            resultados = DaoFrasco.obter_frasco_com_estoque(session)
            return resultados
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
    def editar_frasco_estoque_pelo_id(cls, id_frasco, nova_identificacao, nova_capacidade, novo_estoque_minimo, nova_descricao, novo_status):
        session = create_session()
        try:
            DaoFrasco.editar_frasco_pelo_id(session,
                                            id_frasco,
                                            nova_identificacao,
                                            nova_capacidade,
                                            nova_descricao,
                                            novo_status)
            DaoEstoqueEmpresa.editar_estoque_minimo(session,
                                                    id_frasco,
                                                    novo_estoque_minimo)
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
        # obtendo todos os frascos com seus respectivos estoques
        frascos = cls.obter_frascos_com_estoque()
        # gerando o dataframe e nomeando as colunas
        dataframe = pd.DataFrame(frascos, columns=['Id',
                                                   'Identificação',
                                                   'Capacidade',
                                                   'Descrição',
                                                   'Estoque real',
                                                   'Estoque mínimo',
                                                   'Status'])
        # criando uma coluna chamada seleção
        dataframe['Seleção'] = False
        # reorganizando as colunas do dataframe
        dataframe = dataframe.reindex(['Seleção',
                                       'Id',
                                       'Identificação',
                                       'Capacidade',
                                       'Descrição',
                                       'Estoque real',
                                       'Estoque mínimo',
                                       'Status'],
                                      axis=1)
        return dataframe
    
    @classmethod
    def obter_estoque_baixo_empresa(cls):
        session = create_session()
        try:
            frasco_estoque = DaoEstoqueEmpresa.obter_estoque_baixo_frascos(session)
            if not frasco_estoque:
                return []
            return frasco_estoque
        except Exception as e:
            print(f'Erro: {e}')
        finally:
            session.close()
    
    @classmethod
    def gerar_dataframe_estoque_baixo_empresa(cls):
        frascos = cls.obter_estoque_baixo_empresa()
        dataframe = pd.DataFrame(frascos)
        return dataframe
    