import streamlit as st
from src.controllers.controller_cliente import ControllerCliente

st.header('Registro de devolução')

# carregando os clientes ativos
clientes = ControllerCliente.gerar_dicionario_clientes_ativos()

# carregando os frascos com o cliente


cliente = st.selectbox('Selecione o cliente', options=clientes)

# selecionando os frascos
if not 'tipo_frascos' in st.session_state:
    st.session_state.tipo_frascos = 1

botao_tipo_frasco = st.button('Adicionar frasco')

for i in range(st.session_state.tipo_frascos):
    pass

