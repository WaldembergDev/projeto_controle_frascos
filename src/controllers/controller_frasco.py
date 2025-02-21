from src.dao.dao_frasco import DaoFrasco
from src.models.frasco import Frasco
import pandas as pd

class ControllerFrasco:
    @classmethod
    def criar_frasco(cls, nome, capacidade, descricao):
        frasco_criado = DaoFrasco.adicionar_frasco(nome, capacidade, descricao)
        return True if frasco_criado else False
    
    @classmethod
    def listar_frascos(cls):
        frascos = DaoFrasco.obter_todos_frascos()
        lista_frascos = [(frasco.id, frasco.nome, frasco.capacidade, frasco.descricao) for frasco in frascos]
        return lista_frascos
    
    @classmethod
    def carregar_dataframe_frascos(cls):
        frascos = cls.listar_frascos()
        dataframe = pd.DataFrame(frascos, columns=['Id', 'Nome', 'Capacidade', 'Descrição'])
        dataframe['Selecionado'] = False
        dataframe = dataframe.reindex(['Selecionado', 'Id', 'Nome', 'Identificação', 'Email', 'Telefone', 'Status'], axis=1)
        return dataframe
    

        
    