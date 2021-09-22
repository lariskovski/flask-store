from flask import Flask, request
from flask_restful import Resource, Api

app = Flask(__name__)

api = Api(app)

items = []

class Item(Resource):

    def get(self, name):
        # The filter method acts like a list comprehention
        # The next method gets the first element from the filter list
        # The second parameter on next is what is returned if there are no elements
        item = next(filter(lambda x: x['name'] == name, items), None)
        return {'item': item}, 200 if item else 404

    def post(self, name):
        # makes sure there is no duplicate items
        if next(filter(lambda x: x['name'] == name, items), None) is not None:
            return {'message': f'Item with name {name} already exists'}, 400

        data = request.get_json()
        item = {'name': name, 'price': data['price']}
        items.append(item)
        return item, 201


class ItemList(Resource):
    def get(self):
        return {'items': items}


api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')


app.run(port=5000, debug=True)