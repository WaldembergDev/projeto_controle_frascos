from src.dao.dao_estoque_cliente import DaoEstoqueCliente
from src.database.db import create_session

class ControllerEstoqueCliente:
    @classmethod
    def obter_estoque_do_cliente_pelo_id(cls, id_cliente: int):
        session = create_session()
        try:
            estoque_cliente = DaoEstoqueCliente.obter_estoque_cliente_pelo_id(session, id_cliente)
            if estoque_cliente:
                return estoque_cliente
            else:
                return []
        except Exception as e:
            print(f'Erro: {e}')
            return None
        finally:
            session.close()