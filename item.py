from flask_jwt import jwt_required
from flask_restful import Resource, reqparse
import sqlite3


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
        item = self.find_by_name(name)
        if item:
            return item
        return {'message': 'item not found'}, 404

    @classmethod
    def find_by_name(cls, name):
        conn = sqlite3.connect('data.db')
        cursor = conn.cursor()
        
        query = "SELECT * FROM items WHERE name=?"

        result = cursor.execute(query, (name,))
        row = result.fetchone()

        conn.close()

        if row:
            return {'item': {'name': row[0], 'price': row[1]}}, 200
        return None

    @classmethod
    def create_item(cls, name, price):
        conn = sqlite3.connect('data.db')
        cursor = conn.cursor()
        insert_query = "INSERT INTO items VALUES (?,?)"
        cursor.execute(insert_query, (name, price))
        conn.commit()
        conn.close()


    def post(self, name):
        # Makes sure there are no duplicate items
        if Item.find_by_name(name):
            return {"message": f"Item {name} already exists"}, 400

        data = Item.parser.parse_args()
        item = {'name': name, 'price': data['price']}
        Item.create_item(item['name'], item['price'])

        return {'item': item}, 201


    def delete(self, name):
        
        if not Item.find_by_name(name):
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

