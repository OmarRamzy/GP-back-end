from flask import Flask


# app configuration

app = Flask(__name__)


if __name__ == '__main__':
    app.secret_key = 'MUCMCJUMDPQKBHJOTFWKOKZVNZYQDFPJ'
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
