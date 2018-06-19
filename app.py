from flask import (Flask,
                   jsonify,
                   request,
                   abort,
                   url_for,
                   g)
# flask login
from flask_login import (LoginManager,
                         UserMixin,
                         login_required,
                         login_user,
                         logout_user,
                         current_user)
import sqlite3
# impot sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from DBmodel import (Base,
                     Customer,
                     Owner,
                     Location ,
                     Store)


engine = create_engine('sqlite:///transportation.db')
Base.metadata.bind = engine
DBsession = sessionmaker(bind=engine)
session = DBsession()
# create session and connect to DB
engine = create_engine("sqlite:///transportation.db")
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()
conn = sqlite3.connect('transportation.db', check_same_thread=False)

# app configuration
app = Flask(__name__)



@app.route('/api/v1/customer/login', methods=['PUT'])
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


def verify_customer_token(token):
    user_id = Customer.verify_auth_token(token)
    if user_id:
        return True
    return False



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
                  location_id= request.json['location_id'],
                  type = request.json['type'])
    session.add(store)
    session.commit()
    return jsonify({"Message": "Store Created!"})
   # return jsonify({store.serialize})     Return Error Message typeerror unhashable type dict flask


# Get Active Stores in System
@app.route('/store/actives', methods=['GET'])
def get_active_stores():
    stores = session.query(Store).filter_by(status=True).all()
    return jsonify(ActiveStores =[i.serialize for i in stores])
   # return jsonify({"Message": "Get Active Store!"})


# Set store Active to be visible on the map
@app.route('/store/active', methods=['PUT'])
def active_store():
    store = session.query(Store).filter_by(id= request.json['store_id']).one()
    store.status = True
    session.add(store)
    session.commit()
  #  return jsonify({store.serialize})
    return jsonify({"Message": "Store Active now!"})


# Set store Inactive to be Invisible on the map ( Need locationID )
@app.route('/store/inactive', methods = ['PUT'])
def inactive_store():
    store = session.query(Store).filter_by(id=request.json['store_id']).one()
    store.status = False
    session.add(store)
    session.commit()
    return jsonify({"Message": "Store is Inactive Now!"})


#Delete Store
@app.route('/store/delete', methods =['DELETE'])
def delete_store():
    store = session.query(Store).filter_by(id= request.json['store_id']).one()
    session.delete(store)
    session.commit()
    return jsonify({"Message": "Store Deleted!"})


# ***************Test Method*****************
#Get Stores
@app.route('/stores', methods=['GET'])
def get_all_stores():
    stores = session.query(Store).all()
    return jsonify([i.serialize for i in stores])


#Add Location to DataBase
@app.route('/location/new', methods=['POST' , 'GET'])
def set_location():
    location = Location(lat = request.json['lat'], lang = request.json['lang'])
#    location = Location(lat = request.args.get['lat'], lang = request.agrs.get['lang'])
    session.add(location)
    session.commit()
    return jsonify(location.serialize)


#get Locations  **** Test Method***********
@app.route('/locations', methods=['GET'])
def get_all_locations():
    locations = session.query(Location).all()
    return jsonify([i.serialize for i in locations])


if __name__ == '__main__':
    app.secret_key = 'MUCMCJUMDPQKBHJOTFWKOKZVNZYQDFPJ'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
