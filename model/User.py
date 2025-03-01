from sqlalchemy import Column, Integer, String, Boolean
from repository.base import Base

class User(Base):
    __tablename__ = 'sl_user'
    id = Column(Integer, primary_key=True)
    nome = Column(String(50), nullable=False)
    email = Column(String(50), unique=True, nullable=False)
    senha = Column(String(60), nullable=False)
    is_logado = Column(Boolean, default=0, nullable=False)