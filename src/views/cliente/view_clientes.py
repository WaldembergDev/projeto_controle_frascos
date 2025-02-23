import streamlit as st
from src.controllers.controller_cliente import ControllerCliente
import pandas as pd
import time

# --- caixas de diálogo ---
# editar o cliente selecionado
@st.dialog(title='Editar Cliente')
def editar_cliente(dados_cliente):
    st.text(f'Id: {dados_cliente['id']}')
    nome_cliente = st.text_input('Nome do Cliente', value=dados_cliente['nome'])
    identificacao = st.text_input('Identificação', value=dados_cliente['identificacao'])
    email = st.text_input('Email', value=dados_cliente['email'])
    telefone = st.text_input('Telefone', value=dados_cliente['telefone'])
    valor_status = 0 if dados_cliente['status'] == 'ativo' else 1
    
    status = st.selectbox('Status', options=['ativo', 'inativo'], index=valor_status)
    # botão atualizar dados
    atualizar_dados = st.button('Atualizar Dados')

    if atualizar_dados:
        cliente_atualizado = ControllerCliente.atualizar_cliente_pelo_id(int(dados_cliente['id']), nome_cliente, identificacao, email, telefone, status)
        if cliente_atualizado == True:
            st.success('Cliente atualizado com sucesso!')
            time.sleep(3)
            st.rerun()

# criar um cliente
@st.dialog(title='Criar Cliente')
def criar_cliente():
    nome = st.text_input('Nome do cliente')
    identificacao = st.text_input('CPF/CNPJ')
    telefone = st.text_input('Telefone')
    email = st.text_input('Email')
    botao_cadastrar_cliente = st.button('Cadastrar Cliente', key='')

    if botao_cadastrar_cliente:
        cliente_salvo = ControllerCliente.cadastrar_cliente(nome=nome,
                                                            identificacao=identificacao,
                                                            telefone=telefone,
                                                            email=email)
        if cliente_salvo == True:
            st.success('Cliente cadastrado com sucesso!')
            time.sleep(3)
            st.rerun()
        else:
            st.error(f'Erro ao cadastrar o cliente. {cliente_salvo}')


# --- Interface Principal ---
st.header('Lista de Clientes', divider=True)

dataframe = ControllerCliente.carregar_dataframe_clientes()

col1, col2 = st.columns(2)

with col1:
    # exibe a tabela de clientes
    linhas = st.data_editor(dataframe, use_container_width=True)

    # Obtendo o índices das linhas selecionadas
    linhas_selecionadas = linhas[linhas["Selecionado"] == True]

with col2:
    cadastrar_cliente = st.button('Cadastrar Cliente')
    if cadastrar_cliente:
        criar_cliente()
    if len(linhas_selecionadas) == 1:
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
            






    