import sqlite3
from flask_restful import Resource
from flask import request

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
        data = request.get_json()
        # Create connection
        conn = sqlite3.connect('data.db')
        cursor = conn.cursor()
        
        insert_query = "INSERT INTO users VALUES (?,?,?)"

        cursor.execute(insert_query, (data['username'], data['password']))

        # Commit and close connection
        conn.commit()
        conn.close()
