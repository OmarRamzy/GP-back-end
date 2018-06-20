from flask import Flask
from customer_auth.customer_auth_view import cust_auth as cust_auth_module

# app configuration
app = Flask(__name__)
app.register_blueprint(cust_auth_module)

