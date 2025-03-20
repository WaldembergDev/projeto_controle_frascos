from src.models.estoque_empresa import EstoqueEmpresa
from src.models.frasco import Frasco, StatusEnum
from src.database.db import create_session

class DaoEstoqueEmpresa:
  @classmethod
  def criar_estoque_empresa(cls, session, id_frasco, estoque_real, estoque_minimo):
    estoque_empresa = EstoqueEmpresa(id_frasco = id_frasco,
                                     estoque_real = estoque_real,
                                     estoque_minimo = estoque_minimo)
    session.add(estoque_empresa)
    return estoque_empresa
  
  @classmethod
  def editar_estoque_minimo(cls, session, id_frasco, novo_estoque_minimo):
    estoque_empresa = session\
      .query(EstoqueEmpresa)\
        .filter(EstoqueEmpresa.id_frasco == id_frasco)\
          .first()
    estoque_empresa.estoque_minimo = novo_estoque_minimo
    return estoque_empresa
  
  @classmethod
  def editar_estoque_real(cls, session, id_frasco, novo_estoque_real):
    estoque_empresa = session.query(EstoqueEmpresa).filter(EstoqueEmpresa.id_frasco == id_frasco).first()
    estoque_empresa.estoque_real = novo_estoque_real
    return estoque_empresa
  
  @classmethod
  def obter_estoque_empresa_pelo_id_frasco(cls, session, id_frasco):
    estoque_empresa = session.query(EstoqueEmpresa).filter(EstoqueEmpresa.id_frasco == id_frasco).first()
    return estoque_empresa
  
  @classmethod
  def obter_estoque_baixo_frascos(cls, session):
    estoque_real = session.query(Frasco.identificacao, EstoqueEmpresa.estoque_real)\
      .join(EstoqueEmpresa, EstoqueEmpresa.id_frasco == Frasco.id)\
        .filter(EstoqueEmpresa.estoque_real <= EstoqueEmpresa.estoque_minimo)\
          .filter(Frasco.status == StatusEnum.ATIVO)\
            .all()
    return estoque_real