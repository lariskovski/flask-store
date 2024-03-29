from flask_jwt_extended import jwt_required
from flask_restful import Resource, reqparse

from models.item import ItemModel


class Item(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument(
        'price',
        type=float,
        required=True,
        help="This filed cannot be left blank"
    )

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {'message': 'item not found'}, 404

    def post(self, name):
        # Makes sure there are no duplicate items
        if ItemModel.find_by_name(name):
            return {"message": f"Item {name} already exists"}, 422

        data = Item.parser.parse_args()
        item = ItemModel(name, data['price'])

        try:
            item.save_to_db()
        except Exception as e:
            print(e)
            return {"message": "An error occurred inserting the item"}, 500

        return item.json(), 201

    def delete(self, name):
        item = ItemModel.find_by_name(name)

        if not item:
            return {"message": f"Item {name} does not exists"}, 400

        item.delete_from_db()
        return {'message': 'Item deleted'}, 200

    def put(self, name):
        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)

        if not item:
            item = ItemModel(name, data['price'])
        else:
            item.price = data['price']

        item.save_to_db()
        return item.json(), 200


class ItemList(Resource):
    def get(self):
        return {"item": [item.json() for item in ItemModel.get_all()]}
