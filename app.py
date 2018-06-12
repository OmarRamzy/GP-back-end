import sqlite3
from flask import Flask , redirect,render_template ,request ,url_for , jsonify
from DBmodel import Base , Customer , Owner
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from ExceptionHandler import InvalidUsage

#create session and connect to DB
engine = create_engine("sqlite:///transportation.db")
Base.metadata.bind = engine
DBSession = sessionmaker (bind=engine)
session = DBSession()
conn = sqlite3.connect('transportation.db' , check_same_thread=False)

# app configuration
app = Flask(__name__)


#Function Test Current Users in System
@app.route('/')
@app.route('/users' , methods =['GET'])
def get_all_users():
    Users = session.query(Customer).all()
    return jsonify(Current=[i.serialize for i in Users])


# add new Customer to Database
@app.route('/signup/customer', methods =['POST'])
def add_customer():

    if check_email(request.json['email']) == False:
        return jsonify({"message": "Email is Already Exist!"})

    if check_phone(request.json['phone']) == False:
        return jsonify({"message": "phone is Already Exist!"})

    customer = Customer(first_name=request.json['first_name'],
                      last_name=request.json['last_name'],
                      email=request.json['email'],
                      password=request.json['password'],
                      identity=request.json['identity'],
                      rate=0.0,
                      phone=request.json['phone']
                      )
    session.add(customer)
    session.commit()
    return jsonify({"message":"Customer Added Successfully"})


def check_email(email):
    customer = session.query(Customer).filter_by(email=email).all()
    if customer==[]:
        return True
    else:
        print(customer)
        return False


def check_phone(phone):
    customer = session.query(Customer).filter_by(phone=phone).all()
    if customer== []:
        return True
    else:
        return False


@app.route('/signup/owner', methods =['POST'])
def add_owner():

    owner = Owner(first_name=request.json['first_name'],
                      last_name=request.json['last_name'],
                      email=request.json['email'],
                      password=request.json['password'],
                      identity=request.json['identity'],
                      rate=0.0,
                      phone=request.json['phone'],
                      )
    session.add(owner)
    session.commit()





if __name__ == '__main__':
    app.secret_key = 'MUCMCJUMDPQKBHJOTFWKOKZVNZYQDFPJ'
    app.debug = True
    app.run(host='0.0.0.0', port=8000)