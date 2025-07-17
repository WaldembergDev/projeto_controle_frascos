from src.controllers.controller_usuario import ControllerUsuario
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

# configurações de login e barra de navegação
if not 'login' in st.session_state:
    ViewPrincipal.tela_login()
else:
    ViewPrincipal.menu_principal()







