from src.models.lembrete import Lembrete, StatusEnum
from src.database.db import create_session

class DaoLembrete:
    @classmethod
    def criar_lembrete(cls, session, id_estoque_empresa: int):
        lembrete = Lembrete(id_estoque_empresa = id_estoque_empresa)
        session.add(lembrete)