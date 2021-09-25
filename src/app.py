from security import authenticate, identity
from flask_restful import Api
from flask_jwt import JWT
from flask import Flask

from security import authenticate, identity
from resources.item import Item, ItemList
from resources.user import UserRegister

app = Flask(__name__)
app.secret_key = 'onetwothree'
api = Api(app)

# Creates /auth
# Returns access token
jwt = JWT(app, authenticate, identity)


api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True, threaded=True)