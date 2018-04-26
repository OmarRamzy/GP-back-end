# importing sqlAlchemy

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Float, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.sql import func
from passlib.apps import custom_app_context as pwd_context


Base = declarative_base()


class User(Base):
    """
    class User maps basic user info
    """
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    first_name = Column(String(32), nullable=False)
    last_name = Column(String(32), nullable=False)
    email = Column(String, nullable=False)
    password = Column(String(64), nullable=False)
    identity = Column(String(14), nullable=False)
    rate = Column(Float)
    phone = Column(String(11), nullable=False)
    activated = Column(Boolean, default=False)
    type = Column(String(50))

    __mapper_args__ = {
        'polymorphic_identity': 'user',
        'polymorphic_on': type
    }
