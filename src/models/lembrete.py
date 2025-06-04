from sqlalchemy import Column, Integer, String, Boolean, Enum, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from src.database.db import Base
from datetime import datetime, timezone
import enum

class StatusEnum(str, enum.Enum):
  PENDENTE = 'Pendente'
  CONCLUIDO = 'Concluído'
  

class Lembrete(Base):
  __tablename__ = 'lembretes'
  
  id = Column(Integer, primary_key=True)
  data = Column(DateTime, default=lambda: datetime.now(timezone.utc))
  id_estoque_empresa = Column(Integer, ForeignKey('estoque_empresa.id'), nullable=False)
  status = Column(Enum(StatusEnum), default=StatusEnum.PENDENTE, nullable=False)