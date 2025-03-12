from src.database.db import create_session
from src.models.frasco import Frasco, StatusEnum
from src.models.historico_estoque import HistoricoEstoque

class DaoFrasco:
  @classmethod
  def criar_frasco(cls, session, identificacao, capacidade, descricao):
    frasco = Frasco(identificacao = identificacao, capacidade=capacidade, descricao = descricao)
    session.add(frasco)
    return frasco
  
  @classmethod
  def obter_todos_frascos(cls, session):
    frascos = session.query(Frasco).all()
    return frascos
  
  @classmethod
  def obter_frascos_ativos(cls, session):
    frascos_ativos = session.query(Frasco).filter(Frasco.status == StatusEnum.ATIVO.value).order_by(Frasco.identificacao).all()
    return frascos_ativos
  
  @classmethod
  def obter_frasco(cls, session, id):
    frasco = session.query(Frasco).filter(Frasco.id == id).first()
    return frasco
      
  @classmethod
  def editar_frasco_pelo_id(cls, session, id_frasco, nova_identificacao, nova_capacidade, novo_status):
    frasco = session.query(Frasco).filter(Frasco.id == id_frasco).first()
    frasco.identificacao = nova_identificacao
    frasco.capacidade = nova_capacidade
    frasco.status = novo_status
    return frasco
      
  @classmethod
  def excluir_frasco(cls, session, id):
    frasco = session.query(frasco).filter(Frasco.id == id). first()
    session.delete(frasco)