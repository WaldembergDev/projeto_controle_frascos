from src.models.cliente import Cliente
from src.models.estoque_cliente import EstoqueCliente
from src.models.estoque_empresa import EstoqueEmpresa
from src.models.frasco import Frasco
from src.models.historico_estoque import HistoricoEstoque
from src.models.item_frasco import ItemFrasco
from src.models.solicitacao import Solicitacao
from src.models.tipo import Tipo

from src.database.db import create_tables

from src.dao.dao_frasco import DaoFrasco

from src.controllers.controller_frasco import ControllerFrasco

# frasco = Frasco(identificacao = 'Ambar-500', capacidade = 500, descricao = 'Ambar 500 ml de vidro')
# DaoFrasco.adicionar_frasco(identificacao='Ambar-500', capacidade=500, descricao='Ambar 500 ml de vidro')
# frascos = DaoFrasco.obter_todos_frascos()