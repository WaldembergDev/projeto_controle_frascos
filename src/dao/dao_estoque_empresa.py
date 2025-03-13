from src.models.estoque_empresa import EstoqueEmpresa

class DaoEstoqueEmpresa:
  @classmethod
  def criar_estoque_empresa(cls, session, id_frasco, estoque_real, estoque_minimo):
    estoque_empresa = EstoqueEmpresa(id_frasco = id_frasco,
                                     estoque_real = estoque_real,
                                     estoque_minimo = estoque_minimo)
    session.add(estoque_empresa)
    return estoque_empresa