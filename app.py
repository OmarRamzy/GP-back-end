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

# impot sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from DBmodel import (Base,
                     Customer
                     )


engine = create_engine('sqlite:///transportation.db')
Base.metadata.bind = engine
DBsession = sessionmaker(bind=engine)
session = DBsession()

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


if __name__ == '__main__':
    app.secret_key = 'MUCMCJUMDPQKBHJOTFWKOKZVNZYQDFPJ'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
