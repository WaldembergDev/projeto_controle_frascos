from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from src.database.db import Base

class Tipo(Base):
  __tablename__ = 'tipos'
  
  id = Column(Integer, primary_key=True)
  nome = Column(String(10), unique=True)
  