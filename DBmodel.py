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


# owner related models

class Owner(User):
    __tablename__ = 'owner'
    id = Column(Integer, ForeignKey('user.id'), primary_key=True)
    money_amount = Column(Integer, default=0)
    store_id = Column(Integer, ForeignKey('store.id'),
                      nullable=False)
    service_type_id = Column(Integer, ForeignKey('service.id'),
                             nullable=False)
    store = relationship('Store')
    service = relationship('Service')

    __mapper_args__ = {
        'polymorphic_identity': 'owner',
    }


class Store(Base):
    __tablename__ = 'store'
    id = Column(Integer, primary_key=True)
    name = Column(String(32), nullable=False)
    location_id = Column(Integer, ForeignKey('location.id'),
                         nullable=False)
    location = relationship('Location')


class Location(Base):
    __tablename__ = 'location'
    id = Column(Integer, primary_key=True)
    lat = Column(Float(10), nullable=False)
    lang = Column(Float(10), nullable=False)


class Service(Base):
    __tablename__ = 'service'
    id = Column(Integer, primary_key=True)
    type = Column(String, nullable=False)


# Customer related models

class Customer(User):
    __tablename__ = 'customer'
    id = Column(Integer, ForeignKey('user.id'), primary_key=True)

    __mapper_args__ = {
        'polymorphic_identity': 'customer',
    }

    @property
    def serialize(self):
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'identity': self.identity,
            'rate': self.rate,
            'phone': self.phone,
            'activate': self.activated
        }


engine = create_engine('sqlite:///transportation.db')
Base.metadata.create_all(engine)
