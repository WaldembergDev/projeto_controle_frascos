import streamlit as st

from src.controllers.controller_cliente import ControllerCliente
from src.controllers.controller_frasco import ControllerFrasco
from src.controllers.controller_movimentacao_estoque import ControllerSolicitacaoEstoque

import time

# carregando os dados de clientes ativos
clientes = ControllerCliente.gerar_dicionario_clientes_ativos()

# carregando os dados dos frascos ativos
frascos = ControllerFrasco.gerar_dicionario_frascos_ativos()

# -- Inicio da tela principal -- 
st.header('Liberação de Frascos', divider=True)

responsavel = st.text_input('Responsável')


cliente = st.selectbox('Selecione um cliente', options=clientes)

# obtendo o id do cliente selecionado se existir cliente
if cliente:
    id_cliente = clientes[cliente]

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
        valor_maximo = ControllerFrasco.obter_frasco_pelo_id(int(frascos[frasco])).estoque
        quantidade_frasco = st.number_input('Selecione a quantidade', min_value=1, step=1, key=f'quantidade_frasco_{i}', max_value=valor_maximo)


assinatura = st.text_input('Assinatura')

botao_salvar_dados = st.button('Salvar dados')

if botao_salvar_dados:
    dados_frascos = []
    for i in range(st.session_state.botoes):
        dados_frascos.append((frascos[st.session_state[f'frasco_{i}']], int(st.session_state[f'quantidade_frasco_{i}'])))
    solicitacao_salva = ControllerSolicitacaoEstoque.criar_solicitacao_com_itens(id_usuario=1,
                                                             responsavel=responsavel,
                                                               id_cliente=id_cliente,
                                                                 dados_frascos=dados_frascos)
    if solicitacao_salva == True:
        st.success('Solicitação realizada com sucesso!')
        time.sleep(3)
        st.rerun()
        