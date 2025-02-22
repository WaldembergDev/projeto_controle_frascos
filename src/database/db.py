from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

engine = create_engine(r'sqlite:///data\banco_de_dados.db', echo=True)

Base = declarative_base()

def create_session():
    Session = sessionmaker(bind=engine)
    return Session()

def create_tables():
    Base.metadata.create_all(engine)

def drop_tables():
    Base.metadata.drop_all(engine)