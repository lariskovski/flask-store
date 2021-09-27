from flask_restful import Resource, reqparse
from werkzeug.security import safe_str_cmp
from flask_jwt_extended import create_access_token, create_refresh_token
from models.user import UserModel


class UserRegister(Resource):

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument(
            'username',
            type=str,
            required=True,
            help="This filed cannot be left blank"
        )
        parser.add_argument(
            'password',
            type=str,
            required=True,
            help="This filed cannot be left blank"
        )

        data = parser.parse_args()

        # Makes sure usernames are unique
        if UserModel.find_by_username(data['username']):
            return {"message": "User already exists"}, 400

        user = UserModel(**data)
        user.save_to_db()

        return {"message": "User created successfully"}, 201


class User(Resource):
    @classmethod
    def get(clas, user_id):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {'message': 'user not found'}, 404
        return user.json()

    @classmethod
    def delete(clas, user_id):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {'message': 'user not found'}, 404
        user.delete_from_db()
        return {"message": 'user deleted'}, 200


class UserList(Resource):
    def get(self):
        return {"item": [item.json() for item in UserModel.get_all()]}


class UserLogin(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        'username',
        type=str,
        required=True,
        help="This filed cannot be left blank"
    )
    parser.add_argument(
        'password',
        type=str,
        required=True,
        help="This filed cannot be left blank"
    )

    @classmethod
    def post(cls):
        data = cls.parser.parse_args()

        user = UserModel.find_by_username(data['username'])
        if user and safe_str_cmp(user.password, data['password']):
            access_token = create_access_token(identity=user.id)
            refresh_token = create_refresh_token(user.id)
            return {
                'access_token': access_token,
                'refresh_token': refresh_token
            }, 200

        return {'message': 'invalid credentials'}, 401
