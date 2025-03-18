from src.dao.dao_historico_estoque import DaoHistoricoEstoque
from src.database.db import create_session
import pandas as pd

class ControllerHistoricoEstoque:    
    @classmethod
    def obter_lista_historico_estoque(cls):
        session = create_session()
        try:
            resultado = DaoHistoricoEstoque.obter_lista_historico_estoque(session)
            if not resultado:
                return []
            return resultado
        except Exception as e:
            print(f'Erro: {e}')
            return []
        finally:
            session.close()
    
    @classmethod
    def carregar_dataframe_historico_movimentacao(cls):
        historico_movimentacao = cls.obter_lista_historico_estoque()
        dataframe = pd.DataFrame(historico_movimentacao, columns=['Id', 'Data', 'Frasco', 'Cliente', 'Usuario', 'Quantidade movimentada', 'Tipo de Transação', 'Descrição', 'Id Solicitação', 'Estoque antes empresa', 'Estoque depois empresa', 'Estoque antes cliente', 'Estoque depois cliente'])
        # ajustando o formato da data
        # dataframe['Data'] = dataframe['Data'].dt.strftime('%d/%m/%Y %H:%M')
        dataframe['Selecionado'] = False
        
        dataframe = dataframe.reindex(['Selecionado', 'Id', 'Data', 'Frasco', 'Cliente', 'Usuario', 'Quantidade movimentada', 'Tipo de Transação', 'Descrição', 'Id Solicitação', 'Estoque antes empresa', 'Estoque depois empresa', 'Estoque antes cliente', 'Estoque depois cliente'], axis=1)
        return dataframe