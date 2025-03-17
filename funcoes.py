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
# from dao.dao_movimentacao import DaoSolicitacao
# from src.dao.dao_frasco import DaoFrasco
# from src.dao.dao_estoque_cliente import DaoEstoqueCliente
# from src.dao.dao_historico_estoque import DaoHistoricoEstoque
# from src.dao.dao_estoque_movimentacao import DaoEstoqueMovimentacao

from src.controllers.controller_frasco import ControllerFrasco
from src.controllers.controller_movimentacao_estoque import ControllerMovimentacaoEstoque
# from src.controllers.controller_cliente import ControllerCliente
# from src.controllers.controller_estoque_cliente import ControllerEstoqueCliente