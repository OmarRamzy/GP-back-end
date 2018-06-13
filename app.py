import sqlite3
from flask import Flask,request, jsonify
from DBmodel import Base, Customer, Owner, Location , Store
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from ExceptionHandler import InvalidUsage

# create session and connect to DB
engine = create_engine("sqlite:///transportation.db")
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()
conn = sqlite3.connect('transportation.db', check_same_thread=False)

# app configuration
app = Flask(__name__)


# Function Test Current Users in System
@app.route('/')
@app.route('/users', methods=['GET'])
def get_all_users():
    # Users = session.query(Customer).all()
    Users = session.query(Owner).all()
    return jsonify(CurrentUsers=[i.serialize for i in Users])


# add new Customer to Database
@app.route('/signup/customer', methods=['POST'])
def add_customer():
    if not check_email(request.json['email'], 'Customer'):
        return jsonify({"message": "Email is Already Exist!"})

    if not check_phone(request.json['phone'], 'Customer'):
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
    #  return jsonify({"message":"Customer Added Successfully"})
    return jsonify(customer.serialize)


def check_email(email, type):
    if type == 'Customer':
        customer = session.query(Customer).filter_by(email=email).all()
        if not customer:
            return True
        else:
            return False
    elif type == 'Owner':
        owner = session.query(Owner).filter_by(email=email).all()
        if not owner:
            return True
        else:
            return False


def check_phone(phone, type):
    if type == 'Customer':
        customer = session.query(Customer).filter_by(phone=phone).all()
        if not customer:
            return True
        else:
            return False

    elif type == 'Owner':
        owner = session.query(Owner).filter_by(phone=phone).all()
        if owner == []:
            return True
        else:
            return False


# ACreate Owner Account.
@app.route('/signup/owner', methods=['POST'])
def add_owner():
    if not check_email(request.json['email'], 'Owner'):
        return jsonify({"message": "Email is Already Exist!"})

    if not check_phone(request.json['phone'], 'Owner'):
        return jsonify({"message": "phone is Already Exist!"})

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
    # return jsonify ({"Message":"Owner Added Secessfully "})
    return jsonify(owner.serialize)


# Create new Store
#@app.route('/store/<int:owner_id>/<int:location_id>/new', methods=['POST'])
@app.route('/store/new', methods=['POST'])
def create_store():
    store = Store(name=request.json['name'],
                  owner_id=request.json['owner_id'],
                  location_id= request.json['location_id'])
    session.add(store)
    session.commit()
    return jsonify({"Message": "Store Created!"})
   # return jsonify({store.serialize})     Return Error Message typeerror unhashable type dict flask


# Get Active Stores in System
@app.route('/store/actives', methods=['GET'])
def get_active_stores():
    return jsonify({"Message": "Get Active Store!"})


# Set store Active to be visible on the map
@app.route('/store/<int:store_id>/active', methods = ['PUT'])
def active_store(store_id):
    store = session.query(Store).filter_by(id=store_id).one()
    store.status = True
    session.add(store)
    session.commit()
  #  return jsonify({store.serialize})
    return jsonify({"Message": "Store Active now!"})


# Set store Inactive to be Invisible on the map
@app.route('/store/<int:store_id>/inactive')
def inactive_store(store_id):
    return jsonify(All=[{"Message": "Store is Inactive Now!"},{"Location":"Heey"}])


#Delete Store
@app.route('/store/<int:store_id>/delete')
def delete_store(store_id):
    return jsonify({"Message": "Store Deleted!"})


#Get Stores
@app.route('/stores' , methods=['GET'])
def get_all_stores():
    stores = session.query(Store).all()
    return jsonify([i.serialize for i in stores])

#Add Location to DataBase
@app.route('/location/new' , methods=['POST' , 'GET'])
def set_location():
    location = Location(lat = request.json['lat'], lang = request.json['lang'])
#    location = Location(lat = request.args.get['lat'], lang = request.agrs.get['lang'])
    session.add(location)
    session.commit()
    return jsonify(location.serialize)

#get Locations
@app.route('/locations' , methods=['GET'])
def get_all_locations():
    locations = session.query(Location).all()
    return jsonify([i.serialize for i in locations])

if __name__ == '__main__':
    app.secret_key = 'MUCMCJUMDPQKBHJOTFWKOKZVNZYQDFPJ'
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
