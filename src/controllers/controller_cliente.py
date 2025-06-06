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
    def obter_clientes(cls):
        session = create_session()
        try:
            clientes = DaoCliente.obter_todos_clientes(session)
            return clientes
        except Exception as e:
            return []
        finally:
            session.close()
    
    @classmethod
    def obter_clientes_sem_movimentacao(cls, verificar_pendencia: bool):
        session = create_session()
        try:
            clientes = DaoCliente.obter_clientes_sem_movimentacao(session, verificar_pendencia)
            return clientes
        except Exception as e:
            return []
        finally:
            session.close()
        

    @classmethod
    def obter_clientes_ativos(cls):
        session = create_session()
        try:
            clientes_ativos = DaoCliente.obter_clientes_ativos(session)
            return clientes_ativos
        except Exception as e:
            print(f'Erro: {e}')
            return []
        finally:
            session.close()
    
    @classmethod
    def gerar_dicionario_frascos_pelo_id_cliente(cls, id_cliente):
        session = create_session()
        try:
            cliente = session.query(Cliente).filter(Cliente.id == id_cliente).first()
            estoque_frascos = cliente.estoque_cliente
            dicionario_estoque = {estoque_frasco.frasco.identificacao: estoque_frasco.id_frasco for estoque_frasco in estoque_frascos}
            return dicionario_estoque
        except Exception as e:
            print(f'Erro: {e}')
            return False
        finally:
            session.close()
    
    @classmethod
    def obter_detalhes_frascos_pelo_id_cliente(cls, id_cliente):
        session = create_session()
        try:
            cliente = session.query(Cliente).filter(Cliente.id == id_cliente).first()
            estoque_frascos = cliente.estoque_cliente
            detalhes_frascos = [(estoque_frasco.id, estoque_frasco.frasco.identificacao, estoque_frasco.quantidade) for estoque_frasco in estoque_frascos]
            return detalhes_frascos
        except Exception as e:
            print(f'Erro: {e}')
            return False
        finally:
            session.close()
    
    @classmethod
    def criar_dataframe_frascos_cliente(cls, id_cliente: int):
        detalhes_frascos = cls.obter_detalhes_frascos_pelo_id_cliente(id_cliente)
        dataframe = pd.DataFrame(detalhes_frascos, columns=['Id Frasco', 'Identifição do Frasco', 'Quantidade'])
        dataframe = dataframe.drop(columns=['Id Frasco'])
        return dataframe


    @classmethod
    def listar_clientes(cls):
        clientes = cls.obter_clientes()
        lista_clientes = [(cliente.id, cliente.nome, cliente.identificacao, cliente.email, cliente.telefone, cliente.status) for cliente in clientes]
        return lista_clientes
    
    @classmethod
    def listar_clientes_sem_movimentacao(cls, verificar_pendencia: bool):
        clientes = cls.obter_clientes_sem_movimentacao(verificar_pendencia)
        lista_clientes = [(cliente.id, cliente.nome, cliente.identificacao, cliente.email, cliente.telefone, cliente.status) for cliente in clientes]
        return lista_clientes
    
    @classmethod
    def gerar_dicionario_clientes_ativos(cls):
        clientes_ativos = cls.obter_clientes_ativos()
        dicionario_clientes_ativos = {cliente.nome: cliente.id for cliente in clientes_ativos}
        return dicionario_clientes_ativos
        
    
    @classmethod
    def obter_cliente_pelo_id(cls, id):
        session = create_session()
        try:
            cliente = DaoCliente.obter_cliente_pelo_id(id)
            dados_cliente = [cliente.id, cliente.nome, cliente.identificacao, cliente.email]
            return dados_cliente
        except Exception as e:
            print(f'Erro gerado: {e}')
            return None
        finally:
            session.close()

    @classmethod
    def carregar_dataframe_clientes(cls):
        clientes = cls.listar_clientes()
        dataframe = pd.DataFrame(clientes, columns=['Id', 'Nome', 'Identificação', 'Email', 'Telefone', 'Status'])
        dataframe['Selecionado'] = False
        dataframe = dataframe.reindex(['Selecionado', 'Id', 'Nome', 'Identificação', 'Email', 'Telefone', 'Status'], axis=1)
        return dataframe
    
    @classmethod
    def carregar_dataframe_clientes_sem_movimentacao(cls, verificar_pendencia: bool):
        clientes = cls.listar_clientes_sem_movimentacao(verificar_pendencia)
        dataframe = pd.DataFrame(clientes, columns=['Id', 'Nome', 'Identificação', 'Email', 'Telefone', 'Status'])
        dataframe['Selecionado'] = False
        dataframe = dataframe.reindex(['Selecionado', 'Id', 'Nome', 'Identificação', 'Email', 'Telefone', 'Status'], axis=1)
        return dataframe
    
    @classmethod
    def transformar_linha_dicionario(cls, linha):
        dados_cliente = {
                'id': linha.loc[linha.index[0], 'Id'],
                'nome': linha.loc[linha.index[0], 'Nome'],
                'identificacao': linha.loc[linha.index[0], 'Identificação'],
                'email': linha.loc[linha.index[0], 'Email'],
                'telefone': linha.loc[linha.index[0], 'Telefone'],
                'status': linha.loc[linha.index[0], 'Status'].value
            }
        return dados_cliente
    
    @classmethod
    def atualizar_cliente_pelo_id(cls, id, novo_nome, nova_identificacao, novo_email, novo_telefone, novo_status):
        session = create_session()
        try:
            DaoCliente.atualizar_cliente_pelo_id(session, id, novo_nome, nova_identificacao, novo_email, novo_telefone, novo_status)
            session.commit()
            return True
        except Exception as e:
            print(f'Erro gerado: {e}')
            session.rollback()
            return None
        finally:
            session.close()
    
    @classmethod
    def excluir_cliente_pelo_id(cls, id):
        session = create_session()
        try:
            DaoCliente.excluir_cliente(session, id)
            session.commit()
            return True
        except Exception as e:
            session.rollback()
            return False
        finally:
            session.close()
    
    @classmethod
    def obter_email_cliente_pelo_id(cls, id):
        session = create_session()
        try:
            cliente = DaoCliente.obter_cliente_pelo_id(session, id)
            if not cliente:
                return False
            return cliente.email
        except Exception as e:
            print(f'Erro: {e}')
        finally:
            session.close()
    
    @classmethod
    def obter_clientes_ativos_com_frasco(cls):
        session = create_session()
        try:
            resultados = DaoCliente.obter_clientes_ativos_com_frascos(session)
            if not resultados:
                return []
            return resultados
        except Exception as e:
            print(f'Erro: {e}')
        finally:
            session.close()
    
    @classmethod
    def gerar_dataframe_clientes_ativos_com_frascos(cls):
        resultados = cls.obter_clientes_ativos_com_frasco()
        dataframe = pd.DataFrame(resultados, columns=['Nome', 'Frasco', 'Quantidade'])
        return dataframe
    
    @classmethod
    def obter_frascos_cliente(cls, id_cliente):
        session = create_session()
        try:
            cliente = session.query(Cliente).filter(Cliente.id == id_cliente).first()
            estoque_frascos = cliente.estoque_cliente
            if not estoque_frascos:
                return []
            detalhes_frascos = [(estoque_frasco.frasco.identificacao, estoque_frasco.quantidade) for estoque_frasco in estoque_frascos]
            return detalhes_frascos
        except Exception as e:
            print(f'Erro: {e}')
            return False
        finally:
            session.close()