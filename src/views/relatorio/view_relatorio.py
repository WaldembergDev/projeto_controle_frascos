import streamlit as st
from src.controllers.controller_cliente import ControllerCliente

st.header('Relatório de Frascos', divider=True)

dataframe = ControllerCliente.gerar_dataframe_clientes_ativos_com_frascos()

st.data_editor(dataframe)


