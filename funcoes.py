from datetime import datetime

from src.models.cliente import Cliente
from src.models.estoque_cliente import EstoqueCliente
from src.models.frasco import Frasco
from src.models.historico_estoque import HistoricoEstoque
from src.models.item_frasco import ItemFrasco
from src.models.solicitacao import Solicitacao
from src.models.usuario import Usuario

from src.database.db import create_tables, drop_tables, create_session

from src.dao.dao_frasco import DaoFrasco
from src.dao.dao_solicitacao import DaoSolicitacao
from src.dao.dao_cliente import DaoCliente
from src.dao.dao_frasco import DaoFrasco

from src.controllers.controller_frasco import ControllerFrasco
from src.controllers.controller_cliente import ControllerCliente

# frasco = Frasco(identificacao = 'Ambar-500', capacidade = 500, descricao = 'Ambar 500 ml de vidro')
# session = create_session()
# DaoFrasco.criar_frasco(session, identificacao='Ambar-500', capacidade=500, estoque=100, estoque_minimo=50, descricao='Ambar 500 ml de vidro')
# session.commit()
# frascos = DaoFrasco.obter_todos_frascos()

# data = datetime.now()
# responsavel = 'Waldemberg Pereira'
# assinatura = 'Waldemberg'.encode('utf-8')
# frasco = DaoFrasco.obter_frasco(1)
# frascos = [(frasco, 20)]
# DaoSolicitacao.criar_solicitacaoc_com_itens(data_solicitacao=data, responsavel=responsavel, assinatura=assinatura, id_cliente=1, dados_frascos=frascos)

# testando a função dao cliente
# resultado = ControllerCliente.cadastrar_cliente('Anderson', '25485696320', '2125416396', 'anderson@gmail.com') - Deu certo
# ControllerCliente.excluir_cliente_pelo_id(11) - Deu certo

create_tables()

