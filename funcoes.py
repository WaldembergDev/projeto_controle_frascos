from datetime import datetime

from src.models.cliente import Cliente, StatusEnum
from src.models.estoque_cliente import EstoqueCliente
from src.models.frasco import Frasco
from src.models.item_frasco import ItemFrasco
from src.models.usuario import Usuario, PermissaoEnum
from src.models.historico_estoque import HistoricoEstoque
from src.models.movimentacao import Movimentacao, TipoMovimentacaoEnum, DetalheMovimentacaoEnum

from src.database.db import create_tables, drop_tables, create_session

from src.dao.dao_cliente import DaoCliente
from src.dao.dao_frasco import DaoFrasco
from src.dao.dao_lembrete import DaoLembrete
from src.dao.dao_usuario import DaoUsuario
from src.dao.dao_movimentacao import DaoMovimentacao
from src.dao.dao_historico_estoque import DaoHistoricoEstoque
from src.dao.dao_estoque_empresa import DaoEstoqueEmpresa
from src.dao.dao_estoque_cliente import DaoEstoqueCliente
from src.dao.dao_historico_estoque import HistoricoEstoque
# from dao.dao_movimentacao import DaoSolicitacao
# from src.dao.dao_frasco import DaoFrasco
# from src.dao.dao_estoque_cliente import DaoEstoqueCliente
# from src.dao.dao_historico_estoque import DaoHistoricoEstoque
# from src.dao.dao_estoque_movimentacao import DaoEstoqueMovimentacao

from src.controllers.controller_frasco import ControllerFrasco
from src.controllers.controller_movimentacao_estoque import ControllerMovimentacaoEstoque
from src.controllers.controller_cliente import ControllerCliente
from src.controllers.controller_historico_estoque import ControllerHistoricoEstoque
# from src.controllers.controller_estoque_cliente import ControllerEstoqueCliente

# Pendências
# Gerar relatório com todos os clintes que possuem frascos
# Gerar visualização da movimentaão

import streamlit as st
from PIL import Image
import time

# lista de e-mails permitidos
allowed_users = ["waldemberg.pereirac@gmail.com"]

# Função para verificar o login
def check_user():
    if not st.experimental_user.is_logged_in:
        with st.form('Logar'):
            col1, col2, col3 = st.columns(3)
            with col2:
                st.image('img\pos.jpg')
            if st.form_submit_button('Logar', use_container_width=True):
                st.login()
    else:
        user_email = st.experimental_user.email  # Obtendo o e-mail do usuário
        if user_email not in allowed_users:
            st.error("Acesso negado. Seu e-mail não está autorizado.")
            time.sleep(3)
            st.logout()
    return st.experimental_user.is_logged_in

check_user()