import streamlit as st
from src.controllers.controller_frasco import ControllerFrasco
from src.controllers.controller_movimentacao_estoque import ControllerMovimentacaoEstoque, TipoMovimentacaoEnum, DetalheMovimentacaoEnum
from src.models.frasco import StatusEnum
import time

# caixas de diálogo
# cadastrar frasco
@st.dialog(title='Cadastrar frasco')
def cadastrar_frasco():
    identificacao = st.text_input('Identificação do Frasco')
    capacidade = st.number_input('Capacidade do frasco em mL', step=1, min_value=1)
    descricao = st.text_input('Descrição do frasco')
    estoque_real = st.number_input('Estoque real do frasco', step=1, min_value=0)
    estoque_minimo = st.number_input('Estoque mínimo do frasco', step=1, min_value=0)

    botao_cadastrar = st.button('Cadastrar frasco')
    
    if botao_cadastrar:
        frasco_cadastrado = ControllerFrasco.criar_frasco(1,
                                                          identificacao,
                                                          capacidade,
                                                          estoque_real,
                                                          estoque_minimo,
                                                          descricao)
        if frasco_cadastrado:
            st.success('Frasco cadastrado com sucesso!')
            time.sleep(3)
            st.rerun()
        elif not frasco_cadastrado:
            st.error('Erro ao cadastrar o frasco! Reveja os dados!')            
    
# editar frasco
@st.dialog(title='Editar frasco')
def editar_frasco(dados_frasco):
    id = int(dados_frasco['id']) 
    st.text(f'Id: {id}')
    st.text(f'Estoque real do frasco: {dados_frasco['estoque_real']}')
    identificacao = st.text_input('Identificação do Frasco', value=dados_frasco['identificacao'])
    capacidade = st.number_input('Capacidade do frasco em mL', step=1, min_value=1, value=dados_frasco['capacidade'])
    estoque_minimo = st.number_input('Estoque mínimo do frasco', step=1, min_value=0, value=dados_frasco['estoque_minimo'])
    descricao = st.text_input('Descrição do frasco', value=dados_frasco['descricao'])
    valor_status = 0 if dados_frasco['status'] == 'ativo' else 1
    status = st.selectbox('Status', options=['ativo', 'inativo'], index=valor_status)
    status = StatusEnum.ATIVO if status=='ativo' else StatusEnum.INATIVO
    
    botao_alterar = st.button('Salvar alterações')

    if botao_alterar:
        frasco_editado = ControllerFrasco.editar_frasco_estoque_pelo_id(id, identificacao, capacidade, estoque_minimo, descricao, status)
        if frasco_editado == True:
            st.success('Frasco editado com sucesso!')
            time.sleep(3)
            st.rerun()
        elif frasco_editado == False:
            st.error('Erro ao editar o frasco. Revise os dados digitados!')

# editar quantidade de frasco
@st.dialog(title='Editar quantidade de frasco')
def editar_estoque_real(dados_frasco):
    id = int(dados_frasco['id'])
    quantidade = st.number_input('Digite o novo valor real da quantidade de frascos: ', step=1, value=dados_frasco['estoque_real'])
    justificativa = st.text_input('Justifique a mudança da alteração: ')
    btn_atualizar = st.button('Atualizar quantidade')
    if not justificativa and btn_atualizar:
        st.error('Preencha a justificativa')
    if btn_atualizar and justificativa:
        ControllerMovimentacaoEstoque.criar_movimentacao_com_itens(responsavel=None,
                                                                    id_usuario=1,
                                                                      tipo = TipoMovimentacaoEnum.INTERNO,
                                                                        detalhe_movimentacao=DetalheMovimentacaoEnum.AJUSTE,
                                                                          dados_frascos=[(id, quantidade)],
                                                                            assinatura=None,
                                                                              id_cliente=None,
                                                                                descricao=justificativa)
        st.success('Frascos atualizados com sucesso!')
        time.sleep(3)
        st.rerun()
            

# -- Tela principal -- 
st.header('Lista de Frascos', divider=True)
### nova tela
dataframe = ControllerFrasco.carregar_dataframe_frascos()

col1, col2 = st.columns(2)

with col1:
    # Exibindo o dataframe
    linhas = st.data_editor(dataframe)
    
    # Obtendo os indíces das linhas selecionadas
    linhas_selecionadas = linhas[linhas['Seleção'] == True]

with col2:
    # Botão para criar um novo frasco
    btn_novo_frasco = st.button('Novo Frasco', on_click=cadastrar_frasco)
    # verificando se uma linha foi selecionada
    if len(linhas_selecionadas)==1:
        btn_editar_frasco = st.button('Editar Frasco')
        btn_editar_estoque_real = st.button('Editar estoque real')
        dados_frasco = {
            'id': linhas_selecionadas.iloc[0,1],
            'identificacao': linhas_selecionadas.iloc[0,2],
            'capacidade': linhas_selecionadas.iloc[0,3],
            'descricao': linhas_selecionadas.iloc[0,4],
            'estoque_real': linhas_selecionadas.iloc[0,5],
            'estoque_minimo': linhas_selecionadas.iloc[0,6],
            'status': linhas_selecionadas.iloc[0,7]
        }
        if btn_editar_frasco:
            editar_frasco(dados_frasco)
        
        if btn_editar_estoque_real:
            editar_estoque_real(dados_frasco)
        