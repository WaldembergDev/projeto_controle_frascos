import streamlit as st
from src.controllers.controller_frasco import ControllerFrasco
import time

# caixas de diálogo
# cadastrar frasco
@st.dialog(title='Cadastrar frasco')
def cadastrar_frasco():
    identificacao = st.text_input('Identificação do Frasco')
    capacidade = st.number_input('Capacidade do frasco em mL', step=1, min_value=1)
    descricao = st.text_input('Descrição do frasco')

    botao_cadastrar = st.button('Cadastrar frasco')
    
    if botao_cadastrar:
        frasco_cadastrado = ControllerFrasco.criar_frasco(identificacao, capacidade, descricao)
        if frasco_cadastrado:
            st.success('Frasco cadastrado com sucesso!')
            time.sleep(3)
            st.rerun()
        elif not frasco_cadastrado:
            st.error('Erro ao cadastrar o frasco! Reveja os dados!')            
    
# editar frasco
@st.dialog(title='Editar frasco')
def editar_frasco(dados_frasco):
    identificacao = st.text_input('Identificação do Frasco', value=dados_frasco['identificacao'])
    capacidade = st.number_input('Capacidade do frasco em mL', step=1, min_value=1, value=dados_frasco['capacidade'])
    descricao = st.text_input('Descrição do frasco', value=dados_frasco['descricao'])
    
    botao_alterar = st.button('Salvar alterações')

    if botao_alterar:
        pass


# -- Tela principal -- 
st.header('Lista de Frascos', divider=True)

dataframe = ControllerFrasco.carregar_dataframe_frascos()

col1, col2 = st.columns(2)

with col1:
    linhas = st.data_editor(dataframe)

    # Obtendo o índices das linhas selecionadas
    linhas_selecionadas = linhas[linhas["Selecionado"] == True]

with col2:
    cadastro_frasco = st.button('Criar frasco')
    if cadastro_frasco:
        cadastrar_frasco()
    if len(linhas_selecionadas) == 1:
        botao_editar = st.button('Editar')
        if botao_editar:
            dados_frasco = {
                'id': linhas_selecionadas.iloc[0, 1],
                'identificacao': linhas_selecionadas.iloc[0, 2],
                'capacidade': linhas_selecionadas.iloc[0, 3],
                'descricao': linhas_selecionadas.iloc[0,4],
                'status': linhas_selecionadas.iloc[0,5],
            }
            editar_frasco(dados_frasco)