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
    def insert(cls, item):
        conn = sqlite3.connect('data.db')
        cursor = conn.cursor()
        insert_query = "INSERT INTO items VALUES (?,?)"
        cursor.execute(insert_query, (item['name'], item['price']))
        conn.commit()
        conn.close()


    def post(self, name):
        # Makes sure there are no duplicate items
        if Item.find_by_name(name):
            return {"message": f"Item {name} already exists"}, 400

        data = Item.parser.parse_args()
        item = {'name': name, 'price': data['price']}
        Item.insert(item)

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
        item = {'name': name, 'price': data['price']}

        if Item.find_by_name(name):
            conn = sqlite3.connect('data.db')
            cursor = conn.cursor()
            
            query = "UPDATE items SET price=? WHERE name=?"
            cursor.execute(query, (item['price'], item['name']))

            conn.commit()
            conn.close()
            return item, 200
        
        else:
            Item.insert(item)
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
