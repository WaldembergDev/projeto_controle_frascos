from src.dao.dao_frasco import DaoFrasco
from src.models.frasco import Frasco
import pandas as pd

class ControllerFrasco:
    @classmethod
    def criar_frasco(cls, identificacao, capacidade, descricao):
        frasco_criado = DaoFrasco.adicionar_frasco(identificacao, capacidade, descricao)
        return True if frasco_criado else False
    
    @classmethod
    def listar_frascos(cls):
        frascos = DaoFrasco.obter_todos_frascos()
        lista_frascos = [(frasco.id, frasco.identificacao, frasco.capacidade, frasco.descricao, frasco.status) for frasco in frascos]
        return lista_frascos
    
    @classmethod
    def carregar_dataframe_frascos(cls):
        frascos = cls.listar_frascos()
        dataframe = pd.DataFrame(frascos, columns=['Id', 'identificacao', 'Capacidade', 'Descrição', 'status'])
        dataframe['Selecionado'] = False
        dataframe = dataframe.reindex(['Selecionado', 'Id', 'identificacao', 'Capacidade', 'Descrição', 'status'], axis=1)
        return dataframe
    

        
    