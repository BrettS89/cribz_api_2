import os

from flask import Flask, jsonify
from flask_restful import Resource, Api
from flask_jwt_extended import JWTManager
from flask_cors import CORS

from security import authenticate, identity
from resources.user import UserRegister, User, UserLogin, TokenRefresh
from resources.crib import Crib, Cribs

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPOGATE_EXCEPTIONS'] = True
CORS(app)
app.secret_key = 'darthvader21'
api = Api(app)

@app.before_first_request
def create_tables():
    db.create_all()

jwt = JWTManager(app)

@jwt.user_claims_loader
def add_claims_to_jwt(identity):
    if identity == 1:
        return { 'is_admin': True }
    return { 'is_admin': False }


@jwt.expired_token_loader
def expired_token_callback():
    return jsonify({
        'message': 'Token expired',
        'error': 'token expired'
    }), 401

@jwt.invalid_token_loader
def invalid_token_callback(error):
    return jsonify({
        'message': 'Signature verification failed',
        'error': 'invalid token'
    }), 401


api.add_resource(UserRegister, '/register')
api.add_resource(Crib, '/crib')
api.add_resource(Cribs, '/cribs')
api.add_resource(User, '/user/<int:user_id>')
api.add_resource(UserLogin, '/auth')
api.add_resource(TokenRefresh, '/refresh')


@app.route('/')
def home():
    return 'Baller Cribz'

if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(port=5000)
