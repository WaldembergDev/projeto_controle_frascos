import streamlit as st
from src.controllers.controller_cliente import ControllerCliente
from src.controllers.controller_movimentacao_estoque import ControllerSolicitacaoEstoque
from src.controllers.controller_estoque_cliente import ControllerEstoqueCliente

import time

st.header('Registro de devolução')

# carregando os clientes ativos
clientes = ControllerCliente.gerar_dicionario_clientes_ativos()

# seleção de clientes
cliente = st.selectbox('Selecione o cliente', options=clientes)

# carregando os frascos com o cliente
if clientes:
    frascos = ControllerCliente.gerar_dicionario_frascos_pelo_id_cliente(clientes[cliente])

# selecionando os frascos
if not 'tipo_frascos' in st.session_state:
    st.session_state.tipo_frascos = 1

# definindo as colunas
col1, col2 = st.columns(2)

with col1:
    botao_adicionar_tipo_frasco = st.button('Adicionar frasco')

with col2:
    botao_remover_tipo_frasco = st.button('Remover frasco')

if botao_adicionar_tipo_frasco:
    st.session_state.tipo_frascos += 1

if botao_remover_tipo_frasco:
    if st.session_state.tipo_frascos == 1:
        pass
    else:
        st.session_state.tipo_frascos -= 1

for i in range(st.session_state.tipo_frascos):
    # seleção de frascos que estão com o cliente
    with col1:
        frasco = st.selectbox('Selecione o frasco', options=frascos, key=f'frasco_{i}')
    with col2:
        if cliente and frasco:
            valor_maximo = ControllerEstoqueCliente.obter_estoque_do_cliente_pelo_id(clientes[cliente], frascos[frasco])
        quantidade = st.number_input('Selecione a quantidade', key=f'quantidade_{i}', step=1, min_value=1)

botao_registrar_devolucao = st.button('Registrar devolução')

if botao_registrar_devolucao and cliente and frasco:
    # criando uma lista de tuplas com os dados dos frascos a serem devolvidos
    dados_frascos = [(frascos[st.session_state[f'frasco_{i}']], st.session_state[f'quantidade_{i}']) for i in range(st.session_state.tipo_frascos)]
    registro_salvo = ControllerSolicitacaoEstoque.devolver_frascos(1, clientes[cliente], dados_frascos)
    if registro_salvo == True:
        st.success('Registro salvo com sucesso!')
        time.sleep(2)
        st.rerun()
    else:
        st.error('Erro ao registrar os dados')

elif botao_registrar_devolucao and (not cliente or not frasco):
    st.error('Preencha todos os campos!')


