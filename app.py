from security import authenticate, identity
from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required

from security import authenticate, identity
from user import UserRegister


app = Flask(__name__)
app.secret_key = 'onetwothree'
api = Api(app)

# Creates /auth
# Returns access token
jwt = JWT(app, authenticate, identity)

items = []

class Item(Resource):

    @jwt_required()
    def get(self, name):
        try:
            item = [i for i in items if i['name'] == name][0]
            return {'item': item}, 200
        except IndexError:
            return {'message': f'Item {name} not found'}, 404

    def post(self, name):
        # Makes sure there are no duplicate items
        if [i for i in items if i['name'] == name]:
            return {'message': f'Item with name {name} already exists'}, 400

        data = request.get_json()
        item = {'name': name, 'price': data['price']}
        items.append(item)
        return item, 201

    def delete(self, name):
        global items
        items = [i for i in items if i['name'] != name]
        return {'message': 'Item deleted'}, 200

    def put(self, name):
        parser = reqparse.RequestParser()
        parser.add_argument(
                'price',
                type=float,
                required=True,
                help="This filed cannot be left blank"
        )

        data = parser.parse_args()

        try:
            # If item exists, it's updated
            item = [i for i in items if i['name'] == name][0]
            items.update(data)
        except IndexError:
            # If item does not exist, it's created
            item = {'name': name, 'price': data['price']}
            items.append(item)
        finally:
            return item, 200




class ItemList(Resource):
    def get(self):
        return {'items': items}


api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')


app.run(port=5000, debug=True)