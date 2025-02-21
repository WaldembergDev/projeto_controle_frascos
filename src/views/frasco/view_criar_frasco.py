import streamlit as st
from src.controllers.controller_frasco import ControllerFrasco

st.header('Criar frasco', divider=True)

nome = st.text_input('Nome do frasco')
capacidade = st.number_input('Capacidade do frasco')
descricao = st.text_input('Descricao do frasco')
botao_salvar = st.button('Salvar frasco')

if botao_salvar:
    frasco_salvo = ControllerFrasco.criar_frasco(nome=nome,
                                                 capacidade=capacidade,
                                                 descricao=descricao)
    if frasco_salvo:
        st.success('Frasco foi salvo com sucesso!')
    else:
        st.error('Erro ao cadastrar o frasco. Verifique os dados e tente novamente!')