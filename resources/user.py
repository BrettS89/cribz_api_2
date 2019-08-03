import sqlite3
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_refresh_token_required, get_jwt_identity
from flask_restful import Resource, reqparse
from models.user import UserModel


class UserRegister(Resource):
    parser = reqparse.RequestParser()

    parser.add_argument('email',
                        type=str,
                        required=True,
                        help='This field cannot be left blank'
                        )
    parser.add_argument('password',
                        type=str,
                        required=True,
                        help='This field cannot be left blank'
                        )

    def post(self):
        data = UserRegister.parser.parse_args()
        
        try:
            user = UserModel(**data)
            user.add_to_db()

        except Exception as err:
            print(err)
            return { 'message': 'an error occured' }, 500

        return {'message': 'user created successfully'}, 201


class User(Resource):
    @classmethod
    def get(cls, user_id):
        user = UserModel(None, None)
        user.find_by_id(user_id)
        if not user:
            return { 'message': 'user not found' }, 404
        return user.json()

    @classmethod
    def delete(cls, user_id):
        user = UserModel.find_by_id(user_id)
        if not user:
            return { 'message': 'could not find user' }, 404
        
        user.delete_from_db()


class UserLogin(Resource):
    parser = reqparse.RequestParser()

    parser.add_argument('email',
                        type=str,
                        required=True,
                        help='This field cannot be left blank'
                        )
    parser.add_argument('password',
                        type=str,
                        required=True,
                        help='This field cannot be left blank'
                        )

    @classmethod
    def post(cls):
        try:
            data = cls.parser.parse_args()
            user = UserModel.find_by_email(data['email'])

            if user and data['password'] == user.password:
                access_token = create_access_token(identity=user.id, fresh=True)
                refresh_token = create_refresh_token(user.id)
                return {
                    'access_token': access_token,
                    'refresh_token': refresh_token
                }, 200

            return { 'message': 'invalid credentials' }, 401
            
        except Exception as err:
            print(err)
            return { 'message': 'an error occured' }, 500


class TokenRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        try: 
            current_user = get_jwt_identity()
            new_token = create_access_token(identity=current_user, fresh=False)
            return { 'access_token': new_token }, 200
            
        except Exception as err:
            print(err)
            return { 'message': 'an error occured' }, 500