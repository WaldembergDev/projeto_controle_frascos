from src.database.db import create_session
from src.models.item_frasco import ItemFrasco

class DaoItemFrasco:
    @classmethod
    def criar_item_frasco(cls, session, quantidade: int, id_frasco: int, id_solicitacao: int):
        item_frasco = ItemFrasco(quantidade=quantidade, id_frasco=id_frasco, id_solicitacao=id_solicitacao)
        session.add(item_frasco)
        return item_frasco