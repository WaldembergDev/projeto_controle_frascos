import streamlit as st
from src.controllers.controller_frasco import ControllerFrasco
from src.controllers.controller_movimentacao_estoque import ControllerMovimentacaoEstoque, DetalheMovimentacaoEnum, TipoMovimentacaoEnum
import time

# carregando os dados dos frascos ativos
frascos = ControllerFrasco.gerar_dicionario_frascos_ativos()

# -- Inicio da tela principal -- 
st.header('Solicitação de Frascos', divider=True)

if not 'botoes' in st.session_state:
    st.session_state['botoes'] = 1

col_adicionar, col_remover = st.columns(2)

with col_adicionar:
    botao_adicionar_frasco = st.button('Adicionar Frasco')

with col_remover:
    botao_remover_frasco = st.button('Remover Frasco')

if botao_adicionar_frasco:
    st.session_state.botoes += 1

if botao_remover_frasco:
    if st.session_state.botoes == 1:
        pass
    else:
        st.session_state.botoes -= 1
  
col1, col2 = st.columns(2)

for i in range(st.session_state.botoes):
    with col1:
        frasco = st.selectbox('Selecione um frasco', options=frascos, key=f'frasco_{i}')

    with col2:
        quantidade_frasco = st.number_input('Selecione a quantidade', min_value=0, step=1, key=f'quantidade_frasco_{i}')

btn_solicitar = st.button('Solicitar frascos')

if btn_solicitar:
    dados_frascos = []
    detalhes_frascos = []
    for i in range(st.session_state.botoes):
        dados_frascos.append((frascos[st.session_state[f'frasco_{i}']], int(st.session_state[f'quantidade_frasco_{i}'])))
        detalhes_frascos.append((st.session_state[f'frasco_{i}'], int(st.session_state[f'quantidade_frasco_{i}'])))
    movimentacao = ControllerMovimentacaoEstoque.criar_movimentacao_com_itens(id_usuario=1,
                                                             responsavel=None,
                                                             tipo=TipoMovimentacaoEnum.INTERNO,
                                                             detalhe_movimentacao=DetalheMovimentacaoEnum.SOLICITACAO,
                                                               id_cliente=None,
                                                                 dados_frascos=dados_frascos,
                                                                 assinatura=None)
    if movimentacao:
        # exibindo a mensagem ao usuário
        st.success('Solicitação realizada com sucesso!') 
        time.sleep(3)
        st.rerun()# recarregando a página
    elif movimentacao == False:
        st.error('Erro ao salvar movimentação')