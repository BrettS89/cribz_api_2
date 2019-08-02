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
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = 'SELECT * FROM cribs WHERE user=? ORDER BY created_date DESC'
        results = cursor.execute(query, (user_id,))
        crib_list = list(results)
        formatted_cribs = []

        for c in crib_list:
            formatted_crib = {
                'id': c[0],
                'url': c[1],
                'name': c[2],
                'price': c[3],
                'pictures': c[4].split('|'),
                'user': c[5],
                'created_date': c[6]
            }
            formatted_cribs.append(formatted_crib)

        return {'cribs': formatted_cribs}, 200


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
            
            if crib.user != user_id:
                return {
                    'message': 'you do not have authorization to delete this crib'
                }, 401

            crib.delete_from_db()
            return {'message': 'crib deleted'}, 200

        except Exception as err:
            print(err)
            return {'message': 'an error occured'}, 500
