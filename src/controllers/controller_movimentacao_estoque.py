from src.dao.dao_frasco import DaoFrasco
from src.dao.dao_movimentacao import DaoMovimentacao
from src.dao.dao_estoque_cliente import DaoEstoqueCliente
from src.dao.dao_item_frasco import DaoItemFrasco
from src.dao.dao_historico_estoque import DaoHistoricoEstoque
from src.dao.dao_movimentacao import DaoMovimentacao
from src.dao.dao_estoque_empresa import DaoEstoqueEmpresa
import io
from PIL import Image


from src.models.movimentacao import TipoMovimentacaoEnum, DetalheMovimentacaoEnum

from src.database.db import create_session

import pandas as pd

class ControllerMovimentacaoEstoque:   
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

                # dados do estoque da empresa
                estoque_empresa = DaoEstoqueEmpresa.obter_estoque_empresa_pelo_id_frasco(session, id_frasco)
                if estoque_empresa:
                    etq_antes_emp = estoque_empresa.estoque_real # definindo o estoque que será registrado na função
                    etq_depois_emp = etq_antes_emp

                # dados do estoque do cliente
                estoque_cliente = DaoEstoqueCliente.obter_estoque_cliente_frasco_pelo_id(session, id_cliente, id_frasco)           
                
                if estoque_cliente:
                    etq_antes_cliente = estoque_cliente.quantidade
                else:
                    etq_antes_cliente = None
                    etq_depois_cliente = None                
                
                # Definindo se será somado ou diminuido
                # tipo empréstimo
                if detalhe_movimentacao == DetalheMovimentacaoEnum.EMPRESTIMO:
                    if not estoque_cliente:
                        DaoEstoqueCliente.criar_frasco_estoque_cliente(session, id_frasco, id_cliente, quantidade)
                        etq_antes_cliente = 0
                    else:
                        etq_antes_cliente = estoque_cliente.quantidade
                    etq_depois_cliente = etq_antes_cliente + quantidade
                # tipo devolução
                elif detalhe_movimentacao == DetalheMovimentacaoEnum.DEVOLUCAO:
                    if not estoque_cliente:
                        DaoEstoqueCliente.criar_frasco_estoque_cliente(session, id_frasco, id_cliente, quantidade)
                        etq_antes_cliente = 0
                    etq_depois_cliente = etq_antes_cliente - quantidade
                    if etq_depois_cliente < 0:
                        etq_depois_cliente = 0
                # tipo solicitação
                elif detalhe_movimentacao == DetalheMovimentacaoEnum.SOLICITACAO:
                    etq_depois_emp = etq_antes_emp - quantidade
                # tipo ajuste
                elif detalhe_movimentacao == DetalheMovimentacaoEnum.AJUSTE:
                    etq_depois_emp = quantidade                       
                
                
                # gerar histórico da movimentação
                historico_estoque = DaoHistoricoEstoque.criar_historico_estoque(session, item_frasco.id, etq_antes_emp, etq_depois_emp, etq_antes_cliente, etq_depois_cliente)
                session.flush()
                             

                # ajustando os novos valores do estoque_empresa
                DaoEstoqueEmpresa.editar_estoque_real(session, id_frasco, etq_depois_emp)
                
                
                if etq_depois_cliente or etq_depois_cliente == 0:
                    # ajustando os novos valores do estoque_cliente
                    DaoEstoqueCliente.atualizar_estoque_cliente(session, id_frasco, id_cliente, etq_depois_cliente)         

                # efetivando as atualizações
                session.flush()
            # obtendo o id da movimentacao inserida
            id_movimentacao = movimentacao.id
            # commitando as operações
            session.commit()    
            return id_movimentacao
        except Exception as e:
            print(f'Erro: {e}')
            return False
        finally:
            session.close()
    
    @classmethod
    def obter_movimentacao_pelo_id(cls, id_movimentacao: int):
        session = create_session()
        try:
            movimentacao = DaoMovimentacao.obter_movimentacao(session, id_movimentacao)
            if not movimentacao:
                return None
            return movimentacao
        except Exception as e:
            print(f'Erro: {e}')
        finally:
            session.close()
    
    @classmethod
    def obter_assinatura_pelo_id(cls, id_movimentacao: int):
        session = create_session()
        try:
            movimentacao = DaoMovimentacao.obter_movimentacao(session, id_movimentacao)
            if not movimentacao:
                return None
            imagem = Image.open(io.BytesIO(movimentacao.assinatura))
            return imagem
        except Exception as e:
            print(f'Erro: {e}')
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
        historico_movimentacao = cls.obter_detalhes_movimentacao()
        dataframe = pd.DataFrame(historico_movimentacao)
        # dataframe = pd.DataFrame(historico_movimentacao, columns=['Id', 'Data', 'Frasco', 'Cliente', 'Usuario', 'Quantidade movimentada', 'Tipo de Transação', 'Descrição', 'Id Solicitação', 'Estoque antes empresa', 'Estoque depois empresa', 'Estoque antes cliente', 'Estoque depois cliente'])
        # dataframe['Selecionado'] = False
        # dataframe = dataframe.reindex(['Selecionado', 'Id', 'Data', 'Frasco', 'Cliente', 'Usuario', 'Quantidade movimentada', 'Tipo de Transação', 'Descrição', 'Id Solicitação', 'Estoque antes empresa', 'Estoque depois empresa', 'Estoque antes cliente', 'Estoque depois cliente'], axis=1)
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
            devolucao_mais_recente = DaoMovimentacao.obter_devolucao_mais_recente_id_cliente(session, id_cliente)
            # verificando se existe uma solicitação mais recente do cliente
            if not devolucao_mais_recente:
                return None
            return devolucao_mais_recente.data.strftime('%d/%m/%Y')
        except Exception as e:
            print(f'Erro: {e}')
            return None
        finally:
            session.close()

    @classmethod
    def obter_detalhes_movimentacao(cls):
        session = create_session()
        try:
            detalhes = DaoMovimentacao.obter_detalhes_movimentacao(session)
            if not detalhes:
                return []
            detalhes_valores = [valor[0].value for valor in detalhes]
            return detalhes_valores
        except Exception as e:
            print(f'Erro: {e}')
        finally:
            session.close()