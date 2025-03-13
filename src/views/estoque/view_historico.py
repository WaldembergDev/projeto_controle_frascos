import streamlit as st
from src.controllers.controller_movimentacao_estoque import ControllerSolicitacaoEstoque
from src.controllers.controller_frasco import ControllerFrasco
from src.controllers.controller_cliente import ControllerCliente
from src.controllers.controller_historico_estoque import ControllerHistoricoEstoque
import pandas as pd

@st.dialog('Detalhes')
def visualizar_detalhes(dados):
    id_solicitacao = dados['id_solicitacao']
    ControllerSolicitacaoEstoque.obter_historico_com_movimentacao()

# carregamento dos dados
dataframe = ControllerSolicitacaoEstoque.carregar_dataframe_historico_movimentacao()
frascos_ativos = ControllerFrasco.gerar_dicionario_frascos_ativos()
clientes_ativos = ControllerCliente.gerar_dicionario_clientes_ativos()
tipos_transacoes = ControllerHistoricoEstoque.obter_tipos_transacoes()

st.header('Histórico', divider=True)

with st.sidebar:
    # aplicação dos filtros
    st.header('Aplicação de Filtros')
    data_inicial = st.date_input('Data inicial', format='DD/MM/YYYY', value='2025-02-26')
    data_final = st.date_input('Data final', format='DD/MM/YYYY', value='today')
    frascos_selecionados = st.multiselect('Frascos', options=frascos_ativos, default=frascos_ativos)
    clientes_selecionados = st.multiselect('Clientes', options=clientes_ativos, default=clientes_ativos)
    tipos_transacoes_selecionadas = st.multiselect('Tipos de Transações', options=tipos_transacoes, default=tipos_transacoes)
    botao_visualizar_dados = st.button('Visualizar Detalhes')

# Convertendo as datas para o mesmo formato da data do dataframe as datas para o mesmo formato
data_inicial = pd.to_datetime(data_inicial)
data_final = pd.to_datetime(data_final)
data_final = data_final.replace(hour=23, minute=59)

dataframe_filtrado = dataframe[(dataframe['Data']>=data_inicial) \
                               & (dataframe['Data']<=data_final) \
                                & (dataframe['Frasco'].isin(frascos_selecionados)) \
                                    & dataframe['Cliente'].isin(clientes_selecionados) \
                                        & dataframe['Tipo de Transação'].isin(tipos_transacoes_selecionadas)].copy()

st.data_editor(dataframe_filtrado)