from src.database.db import create_session
from src.models.frasco import Frasco, StatusEnum
from src.models.historico_estoque import HistoricoEstoque

class DaoFrasco:
  @classmethod
  def criar_frasco(cls, session, identificacao, capacidade, estoque, estoque_minimo, descricao): # (cls, frasco: Frasco)
    frasco = Frasco(identificacao = identificacao, capacidade=capacidade, estoque = estoque, estoque_minimo=estoque_minimo, descricao = descricao)
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
  def editar_frasco_pelo_id(cls, session, id_frasco, nova_identificacao, nova_capacidade, novo_estoque_minimo, nova_descricao, novo_status):
    frasco = session.query(Frasco).filter(Frasco.id == id_frasco).first()
    frasco.identificacao = nova_identificacao
    frasco.capacidade = nova_capacidade
    frasco.estoque_minimo = novo_estoque_minimo
    frasco.descricao = nova_descricao
    frasco.status = novo_status
    return frasco
      
  @classmethod
  def excluir_frasco(cls, session, id):
    frasco = session.query(frasco).filter(Frasco.id == id). first()
    session.delete(frasco)
  
  @classmethod
  def ajustar_quantidade_frascos(cls, session, id_frasco, quantidade, tipo_movimentacao):
    session = create_session()
    frasco = session.query(Frasco).filter(Frasco.id == id_frasco).first()
    if tipo_movimentacao == 'Entrada' or tipo_movimentacao == 'Ajuste Positivo':
      frasco.estoque += quantidade
      return frasco
    elif tipo_movimentacao == 'Saída' or tipo_movimentacao == 'Ajuste Negativo':
      frasco.estoque -= quantidade
      return frasco
    else:
      print('Tipo de movimentação incorreta!')
      return None 