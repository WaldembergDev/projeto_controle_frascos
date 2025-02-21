import streamlit as st
from src.controllers.controller_frasco import ControllerFrasco

st.header('Frascos', divider=True)

dataframe = ControllerFrasco.carregar_dataframe_frascos()

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