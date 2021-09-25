import sqlite3
from flask_jwt import jwt_required
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
            return item
        return {'message': 'item not found'}, 404


    def post(self, name):
        # Makes sure there are no duplicate items
        if ItemModel.find_by_name(name):
            return {"message": f"Item {name} already exists"}, 400

        data = Item.parser.parse_args()
        item = {'name': name, 'price': data['price']}

        try:
            ItemModel.insert(item)
        except:
            return {"message": "An error occurred inserting the item"}, 500

        return {'item': item}, 201


    def delete(self, name):
        
        if not ItemModel.find_by_name(name):
            return {"message": f"Item {name} does not exists"}, 400

        conn = sqlite3.connect('data.db')
        cursor = conn.cursor()
        
        query = "DELETE FROM items WHERE name=?"

        cursor.execute(query, (name,))

        conn.commit()
        conn.close()

        return {'message': 'Item deleted'}, 200


    def put(self, name):

        data = Item.parser.parse_args()
        item = {'name': name, 'price': data['price']}

        if ItemModel.find_by_name(name):
            conn = sqlite3.connect('data.db')
            cursor = conn.cursor()
            
            query = "UPDATE items SET price=? WHERE name=?"
            cursor.execute(query, (item['price'], item['name']))

            conn.commit()
            conn.close()
            return item, 200
        
        else:
            ItemModel.insert(item)
            return item, 201


class ItemList(Resource):
    def get(self):
        conn = sqlite3.connect('data.db')
        cursor = conn.cursor()
        
        query = "SELECT * FROM items"
        result = cursor.execute(query)
        items = []

        for row in result:
            items.append({"name": row[0], "price": row[1]})

        conn.close()
        return {'items': items}
