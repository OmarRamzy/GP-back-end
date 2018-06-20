# impot sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.DBmodel import (Base,
                         Customer)

# create session and connect to DB
engine = create_engine("sqlite:///app/transportation.db")
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


def verify_customer_token(token):
    user_id = Customer.verify_auth_token(token)
    if user_id:
        return True
    return False
