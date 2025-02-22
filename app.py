from src.models.cliente import Cliente
from src.models.estoque_cliente import EstoqueCliente
from src.models.estoque_empresa import EstoqueEmpresa
from src.models.frasco import Frasco
from src.models.historico_estoque import HistoricoEstoque
from src.models.item_frasco import ItemFrasco
from src.models.solicitacao import Solicitacao
from src.database.db import create_tables

import streamlit as st

# Configuração da página
st.set_page_config(page_title="Controle de Frascos", layout="wide")

# paginas
view_dashboard = st.Page(r'src\views\dashboard\view_dashboard.py', title='Dashboard')

# Clientes
# view_cadastro_cliente = st.Page(r'src\views\cliente\view_cadastro_cliente.py', title='Cadastro de Clientes')
view_clientes = st.Page(r'src\views\cliente\view_clientes.py', title='Lista de Clientes')

# frascos
view_frascos = st.Page(r'src\views\frasco\view_frascos.py', title='Lista de Frascos')
view_solicitacao_frascos = st.Page(r'src\views\frasco\solicitacao_frasco.py', title='Solicitação de Frascos')
view_estoque_frascos = st.Page(r'src\views\estoque\estoque_frascos.py', title='Estoque de Frascos')
view_relatorios = st.Page(r'src\views\relatorio\view_relatorio.py', title='Relatório de Frascos')

pagina = st.navigation({
    'Menu Principal': [view_dashboard],
    'Cliente': [view_clientes],
    'Frasco': [view_frascos, view_solicitacao_frascos, view_estoque_frascos],
    'Relatórios': [view_relatorios]
    
})

# pagina = st.navigation([view_dashboard, view_cadastro_cliente, view_solicitacao_frascos, view_estoque_frascos, view_relatorios])

pagina.run()






