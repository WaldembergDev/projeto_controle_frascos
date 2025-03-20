import streamlit as st
from src.controllers.controller_cliente import ControllerCliente
from src.controllers.controller_frasco import ControllerFrasco

st.header('Relatório de Frascos', divider=True)

tab1, tab2 = st.tabs(['Frascos em posse dos clientes', 'Frascos com estoque baixo'])

# dataframes
dataframe_clientes = ControllerCliente.gerar_dataframe_clientes_ativos_com_frascos()
dataframe_frascos = ControllerFrasco.gerar_dataframe_estoque_baixo_empresa()


with tab1:
  st.data_editor(dataframe_clientes)
  
with tab2:
  if len(dataframe_frascos) < 1:
    st.text('Não existem frascos com estoque abaixo do mínimo')
  else:
    st.data_editor(dataframe_frascos)




