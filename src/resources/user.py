import sqlite3
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
            return {"message": f"UserModel {data['username']} already exists"}, 400

        # Create connection
        conn = sqlite3.connect('data.db')
        cursor = conn.cursor()
        
        insert_query = "INSERT INTO users VALUES (NULL,?,?)"

        cursor.execute(insert_query, (data['username'], data['password']))

        # Commit and close connection
        conn.commit()
        conn.close()

        return {"message": "UserModel created successfully." }, 201
