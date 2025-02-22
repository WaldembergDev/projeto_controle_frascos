from datetime import datetime

from src.models.cliente import Cliente
from src.models.estoque_cliente import EstoqueCliente
from src.models.estoque_empresa import EstoqueEmpresa
from src.models.frasco import Frasco
from src.models.historico_estoque import HistoricoEstoque
from src.models.item_frasco import ItemFrasco
from src.models.solicitacao import Solicitacao

from src.database.db import create_tables, drop_tables

from src.dao.dao_frasco import DaoFrasco
from src.dao.dao_solicitacao import DaoSolicitacao
from src.dao.dao_cliente import DaoCliente
from src.dao.dao_frasco import DaoFrasco

from src.controllers.controller_frasco import ControllerFrasco

# frasco = Frasco(identificacao = 'Ambar-500', capacidade = 500, descricao = 'Ambar 500 ml de vidro')
# DaoFrasco.adicionar_frasco(identificacao='Ambar-500', capacidade=500, descricao='Ambar 500 ml de vidro')
# frascos = DaoFrasco.obter_todos_frascos()
data = datetime.now()
responsavel = 'Waldemberg Pereira'
assinatura = 'Waldemberg'.encode('utf-8')
frasco = DaoFrasco.obter_frasco(1)
frascos = [(frasco, 20)]
DaoSolicitacao.criar_solicitacaoc_com_itens(data_solicitacao=data, responsavel=responsavel, assinatura=assinatura, id_cliente=1, dados_frascos=frascos)