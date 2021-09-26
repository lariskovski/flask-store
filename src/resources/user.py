from flask_restful import Resource, reqparse

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
