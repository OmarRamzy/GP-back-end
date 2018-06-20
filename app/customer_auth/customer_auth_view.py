from flask import (Flask,
                   jsonify,
                   request,
                   abort,
                   url_for,
                   g,
                   Blueprint)

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

cust_auth = Blueprint('customer', __name__, url_prefix='/api/v1/customer')


# Function Test Current Users in System
@cust_auth.route('/')
def get_all_users():
    # Users = session.query(Customer).all()
    users = session.query(Customer).all()
    return jsonify(CurrentUsers=[i.serialize for i in users])


@cust_auth.route('/login', methods=['PUT'])
def customer_login():
    email_or_token = request.json.get('email')
    password = request.json.get('password')
    user_id = Customer.verify_auth_token(email_or_token)
    if user_id:
        user = session.query(Customer).filter_by(id=user_id).one()
        return jsonify({'token': email_or_token})
    else:
        user = session.query(Customer).filter_by(email=email_or_token).first()
        if not user or not user.verify_password(password):
            return jsonify({'message': False})
    g.user = user
    token = user.generate_auth_token()
    return jsonify({'token': token.decode('ascii')})
