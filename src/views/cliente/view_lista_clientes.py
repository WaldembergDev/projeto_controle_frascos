import streamlit as st
from src.controllers.controller_cliente import ControllerCliente
import pandas as pd
import time

@st.dialog(title='Editar Cliente')
def editar_cliente(dados_cliente):
    st.text(f'Id: {dados_cliente['id']}')
    nome_cliente = st.text_input('Nome do Cliente', value=dados_cliente['nome'])
    identificacao = st.text_input('Identificação', value=dados_cliente['identificacao'])
    email = st.text_input('Email', value=dados_cliente['email'])
    telefone = st.text_input('Telefone', value=dados_cliente['telefone'])
    status = st.text_input('Status', value=dados_cliente['status'])
    # botão atualizar dados
    atualizar_dados = st.button('Atualizar Dados')

    if atualizar_dados:
        cliente_atualizado = ControllerCliente.atualizar_cliente_pelo_id(int(dados_cliente['id']), nome_cliente, identificacao, email, telefone)
        if cliente_atualizado == True:
            st.success('Cliente atualizado com sucesso!')
            time.sleep(3)
            st.rerun()

# inicio da tela
st.header('Lista de Clientes', divider=True)

dataframe = ControllerCliente.carregar_dataframe_clientes()

col1, col2 = st.columns(2)

with col1:
    linhas = st.data_editor(dataframe, num_rows='dynamic')

    # Obtendo o índices das linhas selecionadas
    linhas_selecionadas = linhas[linhas["Selecionado"] == True]

with col2:
    if len(linhas_selecionadas == 1):
        botao_editar = st.button('Editar')
        if botao_editar:
            dados_cliente = {
                'id': linhas_selecionadas.iloc[0, 1],
                'nome': linhas_selecionadas.iloc[0, 2],
                'identificacao': linhas_selecionadas.iloc[0, 3],
                'email': linhas_selecionadas.iloc[0,4],
                'telefone': linhas_selecionadas.iloc[0,5],
                'status': linhas_selecionadas.iloc[0,6].value
            }
            editar_cliente(dados_cliente)
            






    