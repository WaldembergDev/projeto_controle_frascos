from src.models.cliente import Cliente
from src.models.estoque_cliente import EstoqueCliente
from src.models.frasco import Frasco
from src.models.historico_estoque import HistoricoEstoque
from src.models.item_frasco import ItemFrasco
from src.models.movimentacao import Movimentacao
from src.models.usuario import Usuario
from src.database.db import create_tables
from src.views.principal.view_principal import ViewPrincipal

import streamlit as st

import time

allowed_users = ['waldemberg.pereirac@gmail.com']

# Configuração da página
st.set_page_config(page_title="Controle de Frascos", layout="wide")

# Gerando a tela de login
if not st.experimental_user.is_logged_in:
        with st.form('Logar'):
            # col1, col2, col3 = st.columns(3)
            # with col2:
            #     st.image('img\logo.jpg')
            if st.form_submit_button('Logar', use_container_width=True):
                st.login()
else:
    # Obtendo o e-mail do usuário. Criar uma função que compare o email utilizado no google com o e-mail do banco de dados
    user_email = st.experimental_user.email  
    if user_email not in allowed_users:
        st.error("Acesso negado. Seu e-mail não está autorizado.")
        time.sleep(3)
        st.logout()
    else:
        # chamando o menu principal estiver logado
        ViewPrincipal.menu_principal()







