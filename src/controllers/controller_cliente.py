from src.dao.dao_cliente import DaoCliente
from src.models.cliente import Cliente
from src.database.db import create_session
import pandas as pd

class ControllerCliente:
    @classmethod
    def validar_campos_cliente(cls, nome, identificacao, telefone, email):
        if not nome:
            return 'Nome não pode estar vazio!'
        if not identificacao:
            return 'Identificação não pode estar vazia!'
        if not telefone:
            return 'Telefone não pode estar vazio!'
        if not email:
            return 'Email não pode estar vazio!'
        return True

    @classmethod
    def cadastrar_cliente(cls, nome, identificacao, telefone, email):
        # validando os campos
        campos_validados = cls.validar_campos_cliente(nome, identificacao, telefone, email)
        if campos_validados != True:
            return campos_validados
        
        # criando a sessão se os campos forem validados
        session = create_session()
        try:
            DaoCliente.criar_cliente(session=session,
                                                identificacao=identificacao,
                                                nome=nome,
                                                telefone=telefone,
                                                email=email)
            session.commit()
            return True
        except Exception as e:
            session.rollback()
            print(f'Erro gerado: {e}')
            return False
        finally:
            session.close()

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
    def atualizar_cliente_pelo_id(cls, id, novo_nome, nova_identificacao, novo_email, novo_telefone, novo_status):
        resultado = DaoCliente.atualizar_cliente_pelo_id(id, novo_nome, nova_identificacao, novo_email, novo_telefone, novo_status)
        if resultado:
            return True
        else:
            return False
    
    @classmethod
    def excluir_cliente_pelo_id(cls, id):
        resultado = DaoCliente.excluir_cliente(id)
        if resultado is not None:
            return True
        else:
            return False