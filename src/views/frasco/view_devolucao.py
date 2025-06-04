import streamlit as st
from src.controllers.controller_cliente import ControllerCliente
from src.controllers.controller_estoque_cliente import ControllerEstoqueCliente
from src.controllers.controller_movimentacao_estoque import ControllerMovimentacaoEstoque
from src.controllers.controller_frasco import ControllerFrasco
from src.models.movimentacao import DetalheMovimentacaoEnum, TipoMovimentacaoEnum

from src.services.enviar_email import send_email

import time

st.header('Registro de devolução')

responsavel = st.text_input('Responsável pela devolução')

# carregando os clientes ativos
clientes = ControllerCliente.gerar_dicionario_clientes_ativos()

# seleção de clientes
cliente = st.selectbox('Selecione o cliente', options=clientes)

# carregando os frascos com o cliente
if clientes:
    frascos = ControllerFrasco.gerar_dicionario_frascos_ativos()

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
        quantidade = st.number_input('Selecione a quantidade', key=f'quantidade_{i}', step=1, min_value=1)

botao_registrar_devolucao = st.button('Registrar devolução')

if botao_registrar_devolucao and cliente and frasco:
    # criando uma lista de tuplas com os dados dos frascos a serem devolvidos
    dados_frascos = [(frascos[st.session_state[f'frasco_{i}']], st.session_state[f'quantidade_{i}']) for i in range(st.session_state.tipo_frascos)]
    detalhes_frascos = [(st.session_state[f'frasco_{i}'], st.session_state[f'quantidade_{i}']) for i in range(st.session_state.tipo_frascos)]
    registro_salvo = ControllerMovimentacaoEstoque.criar_movimentacao_com_itens(None, 1, TipoMovimentacaoEnum.EXTERNO, DetalheMovimentacaoEnum.DEVOLUCAO, dados_frascos, None, clientes[cliente])
    if registro_salvo:
        # obtendo o email do cliente
        destinatario = ControllerCliente.obter_email_cliente_pelo_id(clientes[cliente])
        # obtendo o saldo dos frascos em posso do cliente
        lista_saldo = ControllerCliente.obter_frascos_cliente(clientes[cliente])
        send_email(cliente, destinatario, DetalheMovimentacaoEnum.DEVOLUCAO, responsavel, detalhes_frascos, lista_saldo)
        st.success('Registro salvo com sucesso!')
        time.sleep(2)
        st.rerun()
    else:
        st.error('Erro ao registrar os dados')

elif botao_registrar_devolucao and (not cliente or not frasco):
    st.error('Preencha todos os campos!')


