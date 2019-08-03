import sqlite3
import time
from flask_restful import Resource, reqparse
from models.crib import CribModel
from flask_jwt_extended import jwt_required, jwt_optional, get_jwt_identity


class Cribs(Resource):
    @jwt_required
    @jwt_optional
    def get(self):
        user_id = get_jwt_identity()
        return {
            'cribs': [crib.json() for crib in CribModel.query.filter_by(user_id=user_id)]
        }, 200

class Crib(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('url',
                        type=str,
                        )

    parser.add_argument('_id',
                        type=int,
                        )

    @jwt_optional
    @jwt_required
    def post(self):
        user_id = get_jwt_identity()
        data = Crib.parser.parse_args()

        try:
            crib = CribModel.from_url(data['url'], user_id)
            crib.save_to_db()
            print(crib.json())
            return {'crib': crib.json()}, 201
        except Exception as err:
            print(err)
            return {'message': 'an error occured'}, 500

    @jwt_optional
    @jwt_required
    def delete(self):
        data = Crib.parser.parse_args()
        try:
            user_id = get_jwt_identity()
            crib = CribModel.get_by_id(data['_id'])
            
            if crib.user.id != user_id:
                return {
                    'message': 'you do not have authorization to delete this crib'
                }, 401

            crib.delete_from_db()
            return {'message': 'crib deleted'}, 200

        except Exception as err:
            print(err)
            return {'message': 'an error occured'}, 500
