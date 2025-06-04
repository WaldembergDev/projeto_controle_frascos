from sqlalchemy import Column, Integer, String, Boolean, Enum
from sqlalchemy.orm import relationship
from src.database.db import Base
import enum

class StatusEnum(str, enum.Enum):
    ATIVO = 'ativo'
    INATIVO = 'inativo'

class PermissaoEnum(str, enum.Enum):
    ADMINISTRADOR = 'administrador'
    OPERADOR_ADMINISTRADOR = 'operador_administrador'
    OPERADOR_ESTOQUE = 'operador_estoque'


class Usuario(Base):
    __tablename__ = 'usuarios'

    id = Column(Integer, primary_key=True)
    login = Column(String(100), nullable=False, unique=True)
    senha = Column(String(255), nullable=False)
    nome = Column(String(255), nullable=False)
    permissao = Column(Enum(PermissaoEnum), default=PermissaoEnum.OPERADOR_ADMINISTRADOR)
    status = Column(Enum(StatusEnum), default=StatusEnum.ATIVO)