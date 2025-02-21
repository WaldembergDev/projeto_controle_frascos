import streamlit as st
from src.controllers.controller_cliente import ControllerCliente

st.header('Cadastro de Clientes', divider=True)

nome = st.text_input('Nome do cliente')

identificacao = st.text_input('CPF/CNPJ')

telefone = st.text_input('Telefone')

email = st.text_input('Email')

botao_salvar = st.button('Cadastrar Cliente')

if botao_salvar:
    cliente_salvo = ControllerCliente.cadastrar_cliente(nome=nome,
                                                        identificacao=identificacao,
                                                        telefone=telefone,
                                                        email=email)
    if cliente_salvo:
        st.success('Cliente cadastrado com sucesso!')
    else:
        st.error('Erro ao cadastrar o cliente. Verifique os dados e tente novamente!')
