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

## Pendências que serão resolvidas dia 24/03
# Trocar o e-mail para compras@qualylab.com.br
# Mostrar comercial responsável pelo cliente e enviar e-mail para o comercial quando houver retirada e devolução
# Carregar o usuário responsável pela movimentação
# Melhorar o e-mail enviado (destacar pontos importantes)
# Mostrar uma tela de confirmação ao liberar, devolver e solicitar frascos
# Cadastrar usuários
# Ajustar horário do banco de dados

from src.controllers.controller_usuario import ControllerUsuario
