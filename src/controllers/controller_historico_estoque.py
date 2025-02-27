from src.dao.dao_historico_estoque import DaoHistoricoEstoque
from src.database.db import create_session  
# # Transações para o cliente
    # EMPRESTIMO = 'Empréstimo'
    # DEVOLUÇÃO = 'Devolução'
    # CANCELAMENTO = 'Cancelamento'

    # # Transações para a QualyLab
    # REPOSICAO = "Reposição"
    # AJUSTE_POSITIVO = 'Ajuste Positivo'
    # AJUSTE_NEGATIVO = "Ajuste Negativo"

class ControllerHistoricoEstoque:
    @classmethod
    def obter_tipos_transacoes(cls):
        session = create_session()
        try:
            tipos_transacoes = DaoHistoricoEstoque.obter_tipo_transacoes(session)
            lista_tipos_transacoes = [tipo[0].value for tipo in tipos_transacoes]
            return lista_tipos_transacoes
        except Exception as e:
            print(f'Erro: {e}')
            return []
        finally:
            session.close()

