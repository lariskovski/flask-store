import sqlite3
from flask_restful import Resource, reqparse


class User:
    def __init__(self, _id, username, password) -> None:
        self.id = _id
        self.username = username
        self.password = password
    
    @classmethod
    def find_by_username(cls, username):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM users WHERE username=?"
        result = cursor.execute(query, (username,))
        row = result.fetchone()

        if row:
            user = cls(*row)
        else:
            user = None
        
        connection.close()
        return user
    
    @classmethod
    def find_by_id(cls, _id):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM users WHERE id=?"
        result = cursor.execute(query, (_id,))
        row = result.fetchone()

        if row:
            user = cls(*row)
        else:
            user = None
        
        connection.close()
        return user


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
        if User.find_by_username(data['username']):
            return {"message": f"User {data['username']} already exists"}, 400

        # Create connection
        conn = sqlite3.connect('data.db')
        cursor = conn.cursor()
        
        insert_query = "INSERT INTO users VALUES (NULL,?,?)"

        cursor.execute(insert_query, (data['username'], data['password']))

        # Commit and close connection
        conn.commit()
        conn.close()

        return {"message": "User created successfully." }, 201
