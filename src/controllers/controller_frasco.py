from src.dao.dao_frasco import DaoFrasco
from src.models.frasco import Frasco
from src.database.db import create_session
import pandas as pd

class ControllerFrasco:
    @classmethod
    def criar_frasco(cls, identificacao, capacidade, estoque, estoque_minimo, descricao):
        session = create_session()
        try:
            DaoFrasco.criar_frasco(session, identificacao, capacidade, estoque, estoque_minimo, descricao)
            session.commit()
            return True
        except Exception as e:
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
    def obter_todos_frascos(cls):
        session = create_session()
        try:
            frascos = DaoFrasco.obter_todos_frascos(session)
            return frascos
        except Exception as e:
            print(f'Erro: {e}')
            return None
        finally:
            session.close()
    
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
    

        
    