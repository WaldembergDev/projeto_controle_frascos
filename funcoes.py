from datetime import datetime

from src.models.cliente import Cliente
from src.models.estoque_cliente import EstoqueCliente
from src.models.frasco import Frasco
from src.models.historico_estoque import HistoricoEstoque
from src.models.item_frasco import ItemFrasco
from src.models.solicitacao import Solicitacao
from src.models.usuario import Usuario
from src.models.estoque_movimentacao import EstoqueMovimentacao

from src.database.db import create_tables, drop_tables, create_session

from src.dao.dao_frasco import DaoFrasco
from src.dao.dao_solicitacao import DaoSolicitacao
from src.dao.dao_cliente import DaoCliente
from src.dao.dao_frasco import DaoFrasco
from src.dao.dao_estoque_cliente import DaoEstoqueCliente
from src.dao.dao_historico_estoque import DaoHistoricoEstoque
from src.dao.dao_usuario import DaoUsuario
from src.dao.dao_estoque_movimentacao import DaoEstoqueMovimentacao

from src.controllers.controller_frasco import ControllerFrasco
from src.controllers.controller_cliente import ControllerCliente
from src.controllers.controller_solicitacao_estoque import ControllerSolicitacaoEstoque

# falta fazer:
# ----------------------------------------
# validação para impedir que um estoque fique negativo
# Função que ajuste a quantidade de frasco 
# Liberação de frasco X
# dashboard
# histórico dos frascos
# exportar histórico para excel - usuário deve escolher cliente, data e frascos
# botão para enviar email