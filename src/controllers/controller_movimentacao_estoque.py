from src.dao.dao_frasco import DaoFrasco
from src.dao.dao_movimentacao import DaoMovimentacao
from src.dao.dao_estoque_cliente import DaoEstoqueCliente
from src.dao.dao_item_frasco import DaoItemFrasco
from src.dao.dao_historico_estoque import DaoHistoricoEstoque
from src.dao.dao_movimentacao import DaoMovimentacao
from src.dao.dao_estoque_empresa import DaoEstoqueEmpresa

from src.models.movimentacao import TipoMovimentacaoEnum, DetalheMovimentacaoEnum

from src.database.db import create_session

import pandas as pd

class ControllerMovimentacaoEstoque:
    @classmethod
    def configurar_historico_estoque(cls, session, id_cliente, id_frasco, tipo_movimentacao, detalhe_movimentacao, quantidade):
        estoque_empresa = DaoEstoqueEmpresa.obter_estoque_empresa_pelo_id_frasco(session, id_frasco)
        estoque_real_empresa = estoque_empresa.estoque_real
        if tipo_movimentacao == TipoMovimentacaoEnum.EXTERNO:
            if detalhe_movimentacao == DetalheMovimentacaoEnum.EMPRESTIMO:
                estoque_cliente = DaoEstoqueCliente.obter_estoque_cliente_frasco_pelo_id(session, id_cliente, id_frasco)
                # verificando se existe estoque do cliente
                if not estoque_cliente:
                    DaoEstoqueCliente.criar_frasco_estoque_cliente(session, id_frasco, id_cliente, 0)
                    etq_antes_cliente = 0                
                else:
                    etq_antes_cliente = estoque_cliente.quantidade
                estoque_real_cliente = quantidade + etq_antes_cliente
        
            elif detalhe_movimentacao == DetalheMovimentacaoEnum.DEVOLUCAO:
                estoque_real_cliente -= quantidade
        else:
            estoque_real_cliente == None
            if detalhe_movimentacao == DetalheMovimentacaoEnum.REPOSICAO:
                estoque_real_empresa += quantidade
        
        return estoque_empresa.estoque_real, estoque_real_empresa, etq_antes_cliente, estoque_real_cliente
        
    
    @classmethod
    def criar_movimentacao_com_itens(cls, responsavel: str, id_usuario: int, tipo:TipoMovimentacaoEnum, detalhe_movimentacao:DetalheMovimentacaoEnum, dados_frascos: list, assinatura: str=None, id_cliente: int=None, descricao: str=None, status=None):        
        session = create_session()
        try:
            # 1 - criando a solicitação
            movimentacao = DaoMovimentacao.criar_movimentacao(session,
                                                               responsavel=responsavel,
                                                                 id_usuario=id_usuario,
                                                                   tipo=tipo,
                                                                     detalhe_movimentacao=detalhe_movimentacao,
                                                                       id_cliente=id_cliente,
                                                                         descricao=descricao, 
                                                                          assinatura=assinatura,
                                                                           status=status)
            session.flush() # gerando o id da movimentacao
            # percorrendo pela lista de frascos
            for (id_frasco, quantidade) in dados_frascos:
                # criando item frasco associado à solicitação
                item_frasco = DaoItemFrasco.criar_item_frasco(session, quantidade=quantidade, id_frasco=id_frasco, id_movimentacao=movimentacao.id)
                session.flush() # gerando o id do item_frasco

                # configurando os valores do histórico
                etq_antes_emp, etq_depois_emp, etq_antes_cliente, etq_depois_cliente = cls.configurar_historico_estoque(session, id_cliente, id_frasco, tipo, detalhe_movimentacao, quantidade)                        
                
                # gerar histórico da movimentação
                historico_estoque = DaoHistoricoEstoque.criar_historico_estoque(session, item_frasco.id, etq_antes_emp, etq_depois_emp, etq_antes_cliente, etq_depois_cliente)
                session.flush()
                  

                # ajustando os novos valores do estoque_empresa
                DaoEstoqueEmpresa.editar_estoque_real(session, id_frasco, etq_depois_emp)
                
                print(etq_depois_cliente)
                # ajustando os novos valores do estoque_cliente
                DaoEstoqueCliente.atualizar_estoque_cliente(session, id_frasco, id_cliente, etq_depois_cliente)                

                # efetivando as atualizações
                session.flush()
                       
            session.commit()    
            return True
        except Exception as e:
            print(f'Erro: {e}')
            return False
        finally:
            session.close()
    
    @classmethod
    def devolver_frascos(cls, id_usuario: int, id_cliente: int, frascos: list):
        session = create_session()
        try:
            for (id_frasco, quantidade) in frascos:
                historico_estoque = DaoHistoricoEstoque.criar_historico_estoque(session, id_frasco, id_cliente, id_usuario, quantidade, TipoTransacao.DEVOLUCAO, None, None)
                session.flush() # gerando o id do historico estoque
                # obtendo os dados do estoque da empresa
                frasco_empresa = DaoFrasco.obter_frasco(session, id_frasco)
                estoque_antes_empresa = frasco_empresa.estoque
                estoque_depois_empresa = estoque_antes_empresa + quantidade
                # obtendo os dados do estoque do cliente
                frasco_cliente = DaoEstoqueCliente.obter_estoque_cliente_pelo_id(session, id_cliente, id_frasco)
                estoque_antes_cliente = frasco_cliente.quantidade
                estoque_depois_cliente = estoque_antes_cliente - quantidade
                # registrando a movimentação
                estoque_movimentacao = DaoEstoqueMovimentacao.criar_movimentacao_estoque(session,
                                                                                          historico_estoque.id,
                                                                                            estoque_antes_empresa,
                                                                                              estoque_depois_empresa,
                                                                                                estoque_antes_cliente,
                                                                                                  estoque_depois_cliente)
                # registrando a mudança no estoque da empresa
                DaoFrasco.adicionar_quantidade_frascos(session, id_frasco, quantidade)
                # registrando a mudança no estoque do cliente
                DaoEstoqueCliente.reduzir_estoque_cliente(session, id_frasco, id_cliente, quantidade)
            session.commit()
            return True
        except Exception as e:
            session.rollback()
            print(f'Erro {e}')
            return False
        finally:
            session.close()
    
    @classmethod
    def obter_todo_historico(cls):
        session = create_session()
        try:
            historico = DaoHistoricoEstoque.obter_todo_historico(session)
            return historico
        except Exception as e:
            print(f'Erro: {e}')
            return []
        finally:
            session.close()
    
    @classmethod
    def obter_historico_com_movimentacao(cls):
        session = create_session()
        try:
            resultados = DaoHistoricoEstoque.obter_historico_movimentacao(session)
            lista_historico = [(resul[0], resul[1], resul[2], resul[3], resul[4], resul[5], resul[6].value, resul[7], resul[8], resul[9], resul[10], resul[11], resul[12]) for resul in resultados]
            return lista_historico
        except Exception as e:
            print(f'Erro: {e}')
            return []
        finally:
            session.close()
    
    @classmethod
    def carregar_dataframe_historico_movimentacao(cls):
        historico_movimentacao = cls.obter_historico_com_movimentacao()
        dataframe = pd.DataFrame(historico_movimentacao, columns=['Id', 'Data', 'Frasco', 'Cliente', 'Usuario', 'Quantidade movimentada', 'Tipo de Transação', 'Descrição', 'Id Solicitação', 'Estoque antes empresa', 'Estoque depois empresa', 'Estoque antes cliente', 'Estoque depois cliente'])
        dataframe['Selecionado'] = False
        dataframe = dataframe.reindex(['Selecionado', 'Id', 'Data', 'Frasco', 'Cliente', 'Usuario', 'Quantidade movimentada', 'Tipo de Transação', 'Descrição', 'Id Solicitação', 'Estoque antes empresa', 'Estoque depois empresa', 'Estoque antes cliente', 'Estoque depois cliente'], axis=1)
        return dataframe
    
    @classmethod
    def obter_emprestimo_mais_recente_id_cliente(cls, id_cliente):
        session = create_session()
        try:
            emprestimo_mais_recente = DaoMovimentacao.obter_emprestimo_mais_recente_id_cliente(session, id_cliente)
            # verificando se existe uma solicitação mais recente do cliente
            if not emprestimo_mais_recente:
                return None
            return emprestimo_mais_recente.data.strftime('%d/%m/%Y')
        except Exception as e:
            print(f'Erro: {e}')
            return None
        finally:
            session.close()
    
    @classmethod
    def obter_devolucao_mais_recente_id_cliente(cls, id_cliente):
        session = create_session()
        try:
            devolucao_mais_recente = DaoHistoricoEstoque.obter_devolucao_mais_recente_id_cliente(session, id_cliente)
            # verificando se existe uma solicitação mais recente do cliente
            if not devolucao_mais_recente:
                return None
            return devolucao_mais_recente.data_movimentacao.strftime('%d/%m/%Y')
        except Exception as e:
            print(f'Erro: {e}')
            return None
        finally:
            session.close()