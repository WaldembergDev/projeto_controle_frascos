from src.database.db import create_session
from src.models.estoque_cliente import EstoqueCliente

class DaoEstoqueCliente:
    @classmethod
    def criar_frasco_estoque_cliente(cls, session, id_frasco, id_cliente, quantidade):
        estoque_cliente = EstoqueCliente(id_cliente=id_cliente, id_frasco=id_frasco, quantidade=quantidade)
        session.add(estoque_cliente)
        return estoque_cliente
        
    @classmethod
    def movimentar_estoque_cliente_apagar(cls, session, id_frasco, id_cliente, quantidade, tipo_movimentacao):
        estoque_cliente = session.query(EstoqueCliente).filter(EstoqueCliente.id_cliente==id_cliente).filter(EstoqueCliente.id_frasco==id_frasco).first()
        if not estoque_cliente:
            print('Estoque não encontrado')
            return None
        if tipo_movimentacao == 'Devolução':
            estoque_cliente.quantidade -= quantidade
        elif tipo_movimentacao == 'Saída':
            estoque_cliente.quantidade += quantidade
        else:
            print('Movimentação inválida!')
            return None
        return estoque_cliente
    
    @classmethod
    def atualizar_estoque_cliente(cls, session, id_frasco, id_cliente, nova_quantidade):
        estoque_cliente = session.query(EstoqueCliente).filter(EstoqueCliente.id_frasco == id_frasco).filter(EstoqueCliente.id_cliente == id_cliente).first()
        estoque_cliente.quantidade = nova_quantidade
        return estoque_cliente

    @classmethod
    def reduzir_estoque_cliente(cls, session, id_frasco, id_cliente, quantidade):
        estoque_cliente = session.query(EstoqueCliente).filter(EstoqueCliente.id_frasco == id_frasco).filter(EstoqueCliente.id_cliente == id_cliente).first()
        estoque_cliente.quantidade -= quantidade
        return estoque_cliente
    
    @classmethod
    def obter_estoque_cliente_pelo_id(cls, session, id_cliente, id_frasco):
        estoque = session.query(EstoqueCliente).filter(EstoqueCliente.id_cliente == id_cliente).filter(EstoqueCliente.id_frasco == id_frasco).first()
        return estoque
    

    

        



