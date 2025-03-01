from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from repository.conexao import get_conexao
from repository.base import Base


def get_session():
    """Retorna a Sessão para realizar os trâmites no Banco de Dados

    Returns:
        Session: Sessão do Banco de Dados
    """
    engine = create_engine(get_conexao(), echo=False)
    Session = sessionmaker(bind=engine)
    return Session()


def create_table():
    """Cria a tabela de usuários no Bnco de Dados"""
    
    engine = create_engine(get_conexao(), echo=False)
    Base.metadata.create_all(engine)
