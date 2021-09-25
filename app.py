from security import authenticate, identity
from flask_restful import Api
from flask_jwt import JWT
from flask import Flask

from security import authenticate, identity
from item import Item, ItemList
from user import UserRegister

app = Flask(__name__)
app.secret_key = 'onetwothree'
api = Api(app)

# Creates /auth
# Returns access token
jwt = JWT(app, authenticate, identity)


api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')


app.run(port=5000, debug=True)