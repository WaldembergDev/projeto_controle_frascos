from src.dao.dao_cliente import DaoCliente
from src.models.cliente import Cliente
import pandas as pd

class ControllerCliente:
    @classmethod
    def cadastrar_cliente(cls, nome, identificacao, telefone, email):
        result = DaoCliente.criar_cliente(identificacao=identificacao,
                                 nome=nome,
                                 telefone=telefone,
                                 email=email)
        return result

    @classmethod
    def listar_clientes(cls):
        clientes = DaoCliente.obter_todos_clientes()
        lista_clientes = [(cliente.id, cliente.nome, cliente.identificacao, cliente.email, cliente.telefone, cliente.status) for cliente in clientes]
        return lista_clientes
    
    @classmethod
    def obter_cliente_pelo_id(cls, id):
        cliente = DaoCliente.obter_cliente_pelo_id(id)
        dados_cliente = [cliente.id, cliente.nome, cliente.identificacao, cliente.email]
        return dados_cliente
    

    @classmethod
    def carregar_dataframe_clientes(cls):
        clientes = cls.listar_clientes()
        dataframe = pd.DataFrame(clientes, columns=['Id', 'Nome', 'Identificação', 'Email', 'Telefone', 'Status'])
        dataframe['Selecionado'] = False
        dataframe = dataframe.reindex(['Selecionado', 'Id', 'Nome', 'Identificação', 'Email', 'Telefone', 'Status'], axis=1)
        return dataframe
    
    @classmethod
    def atualizar_cliente_pelo_id(cls, id, novo_nome, nova_identificacao, novo_email, novo_telefone):
        resultado = DaoCliente.atualizar_cliente_pelo_id(id, novo_nome, nova_identificacao, novo_email, novo_telefone)
        if resultado:
            return True
        else:
            return False