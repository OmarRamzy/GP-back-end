# importing sqlAlchemy
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Float, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.sql import func
from passlib.apps import custom_app_context as pwd_context

# importing itsdangrous
from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer,
                          BadSignature,
                          SignatureExpired)
import random, string

Base = declarative_base()
secret_key = ''.join(
    random.choice(string.ascii_uppercase+string.digits)
    for x in range(32))


class User(Base):
    """
    class User maps basic user info
    """
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    first_name = Column(String(32), nullable=False)
    last_name = Column(String(32), nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String(64), nullable=True)
    identity = Column(String(14), nullable=False , unique=True)
    rate = Column(Float)
    phone = Column(String(11), nullable=False , unique=True)
    activated = Column(Boolean, default=False)
    type = Column(String(50))

    __mapper_args__ = {
        'polymorphic_identity':'user',
        'polymorphic_on':type
    }

    def hash_password(self, password):
        self.password = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password)

    def generate_auth_token(self, expiration=600):
        s = Serializer(secret_key, expires_in=expiration)
        return s.dumps({'id': self.id})

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(secret_key)
        try:
            data = s.loads(token)
        except SignatureExpired:
            # Valid Token, but expired
            return None
        except BadSignature:
            # Invalid Token
            return None
        user_id = data['id']
        return user_id


# owner related models
class Owner(User):
    __tablename__ = 'owner'
    id = Column(Integer, ForeignKey('user.id'), primary_key=True)
    money_amount = Column(Integer, default=0)

   # service_type_id = Column(Integer, ForeignKey('service.id'),
   #                          nullable=False)
   # service = relationship('Service')

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
            'activate': self.activated,
            'money_amount': self.money_amount
          #  'service_type_id': self.service_type_id
        }

    __mapper_args__ = {
        'polymorphic_identity': 'owner',
    }


class Store(Base):
    __tablename__ = 'store'
    id = Column(Integer, primary_key=True)
    name = Column(String(32), nullable=False)
    type = Column(String(32), nullable=False)
    status= Column(Boolean , default=False)
    location_id = Column(Integer, ForeignKey('location.id'), nullable=False)
    owner_id = Column(Integer , ForeignKey('owner.id'),nullable=False )
    location = relationship('Location')
    owner = relationship('Owner')

    @property
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'type':self.type,
            'owner': self.owner.serialize,
            'status': self.status,
            'location':self.location.serialize
        }


class Location(Base):
    __tablename__ = 'location'
    id = Column(Integer, primary_key=True)
    lat = Column(Float(10), nullable=False)
    lang = Column(Float(10), nullable=False)

    @property
    def serialize(self):
        return {
                'id': self.id,
                'lat': self.lat,
                'lang': self.lang
                }


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


class Car(Base):
    __tablename__= 'car'
    id = Column(Integer, primary_key=True)
    model = Column(String(25))
    type = Column(String(10))
    number = Column(String(20) , unique=True)
    active = Column(Boolean, default=True)
 #   licence = Column(String(25) , nullable=True)  # Don't Know type of licence

    __mapper_args__ = {
        'polymorphic_identity': 'car',
        'polymorphic_on': type
    }


class PrivateCar(Car):
    __tablename__ = 'privateCar'
    id = Column(Integer, ForeignKey('car.id') , primary_key=True)
    store_id = Column(Integer, ForeignKey('store.id'), nullable=False )
    store = relationship('Store')

    __mapper_args__ = {
        'polymorphic_identity': 'privateCar',
    }


class HeavyCar(Car):
    __tablename__ = 'heavyCar'
    id = Column(Integer, ForeignKey('car.id'), primary_key=True)
    location_id = Column(Integer, ForeignKey('location.id'), nullable=False)
    location = relationship('Location')
    image= Column(String(100), nullable=False)
    owner_id = Column(Integer, ForeignKey('owner.id'), nullable=False)
    owner = relationship('Owner')

    __mapper_args__ = {
        'polymorphic_identity': 'heavyCar',
    }


engine = create_engine('sqlite:///transportation.db')
Base.metadata.create_all(engine)

print "Database Created!"